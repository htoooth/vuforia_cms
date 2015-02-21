from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout, \
                                update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models.query import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

# CustomFileInput用に。
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_text
from django.forms.widgets import FileInput, Input, CheckboxInput

from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser, \
                       Content
from vws import vuforia

import os, json, logging, base64

# TODO: 本来はメタデータは、JSONファイルのURL
def create_metadata_dict(contractno, title,
                         open_from, open_to, mapping_url):
    """
    メタデータのPythonディクショナリーを生成する関数
    """
    json_dict = {}
    json_dict['CONTRACT_NO'] = contractno
    json_dict['TITLE'] = title
    json_dict['OPEN_FROM'] = open_from.strftime('%Y-%m-%d')
    if open_to:
        json_dict['OPEN_TO'] = open_to.strftime('%Y-%m-%d')
    else:
        json_dict['OPEN_TO'] = None
    json_dict['TYPE'] = 'url'
    json_dict['URL'] = mapping_url
    return json_dict

def create_metadata(contractno, title, open_from, open_to, mapping_url):
    """
    メタデータを作成する関数
    """
    metadata_dict = create_metadata_dict(contractno, title,
                                         open_from, open_to, mapping_url)
    metadata_json = json.dumps(metadata_dict, ensure_ascii=False)
    return base64.b64encode(metadata_json.encode()).decode()

def create_json(contractno, title, open_from, open_to, mapping_url):
    """
    メタデータのJSONファイルを作成・保存する関数
    """
    metadata_dict = create_metadata_dict(contractno, title,
                                         open_from, open_to, mapping_url)
    p = os.path.join(settings.BASE_DIR, 'cms/static/json',
                     contractno + '.json')
    with open(p, "w", encoding="utf-8") as json_fp:
        json.dump(metadata_dict, json_fp, ensure_ascii=False)

@login_required
@permission_required('cms.running', raise_exception=True)
def list(request):
    # ログインしているユーザー所有のアカウントの持つ全コンテンツを渡す。
    if request.user.acc_type_id == 1:
        content_list = Content.objects.filter(
            company__acc_type_id__exact=3,
            company__parent_admin_id__exact=request.user.user_id
        )
    elif request.user.acc_type_id == 2:
        content_list = Content.objects.filter(
            company__acc_type_id__exact=3,
            company__parent_agency_id__exact=request.user.user_id
        )
    elif request.user.acc_type_id == 3:
        content_list = Content.objects.filter(
            company__user_id__exact=request.user.user_id
        )

    paginator = Paginator(content_list, 2)
    page = request.GET.get('page')
    try:
        contents = paginator.page(page)
    except PageNotAnInteger:
        contents = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contents = paginator.page(paginator.num_pages)

    # テンプレートでは回数（int型）でイテレートできない？
    loop = [x for x in range(paginator.num_pages)]
    return render(request, 'content_list.html',
                  {'loop': loop, 'contents': contents})

@transaction.atomic
@login_required
@permission_required('cms.running', raise_exception=True)
def new(request, contractno):
    error_message = ''
    # 既存のコンテンツインスタンス(契約)
    i = Content.objects.get(contract_no__exact=contractno)
    # その画像ファイルの名前
    old_file_name = i.image.name
    # その画像ファイルのパス
    old_file_path = os.path.join(settings.MEDIA_ROOT, i.image.name)

    company = i.company
    if request.POST:
        form = ContentForm(request.POST, request.FILES, instance=i)
        if form.is_valid():
            open_from   = form.cleaned_data['open_from']
            open_to     = form.cleaned_data['open_to']
            title       = form.cleaned_data['title']
            mapping_url = form.cleaned_data['mapping_url']

            # Vuforiaへの登録処理
            key_path = os.path.join(settings.BASE_DIR, '../accesskey.json')
            with open(key_path, "r", encoding="utf-8") as key_fp:
                key_dict = json.load(key_fp)
            v = vuforia.Vuforia(access_key=key_dict["ACCESS_KEY"],
                                secret_key=key_dict["SECRET_KEY"])
            if request.FILES:
                image = base64.b64encode(
                        request.FILES['image'].read()).decode('utf-8')
            metadata = create_metadata(i.contract_no, title, open_from,
                                       open_to, mapping_url)

            # JSONファイルを作る。
            create_json(contractno, title, open_from, open_to,
                        mapping_url)

            # 画像サムネイルを作る。

            # フォームのデータをDBに仮保存する。
            new_content = form.save(commit=False)

            res = v.add_target(
                    {"name": title, "width": 320, "image": image,
                     "application_metadata": metadata, "active_flag": 0})

            # Vuforia APIで登録処理が成功したら続きの処理を行う。
            if res['result_code'] == "TargetCreated":
                new_content.target_id = res['target_id']

                # TODO: ここでエラーとなると、
                # Vuforiaには登録されていて、自DBには無い状態になる。
                new_content.save()
                return redirect('/content/list')

            # Vuforiaのレスポンスが成功でない場合
            else:
                # エラーメッセージを出力して戻る。
                error_message = res['result_code']
        else:
            return render(request, 'content_new.html',
                {'form': form, 'contractno': contractno,
                 'company': company, 'error_message': error_message})
    else:
        form = ContentForm(instance=i)
    return render(request, 'content_new.html',
            {'form': form, 'contractno': contractno,
             'company': company, 'error_message': error_message})

@transaction.atomic
@login_required
@permission_required('cms.running', raise_exception=True)
def edit(request, contractno):
    error_message = ''
    # 既存のコンテンツインスタンス(契約)
    i = Content.objects.get(contract_no__exact=contractno)
    # その画像ファイルの名前
    old_file_name = i.image.name
    # その画像ファイルのパス
    old_file_path = os.path.join(settings.MEDIA_ROOT, i.image.name)

    company = i.company
    if request.POST:
        form = ContentForm(request.POST, request.FILES, instance=i)
        if form.is_valid():
            open_from   = form.cleaned_data['open_from']
            open_to     = form.cleaned_data['open_to']
            title       = form.cleaned_data['title']
            mapping_url = form.cleaned_data['mapping_url']

            metadata = create_metadata(i.contract_no, title, open_from,
                                       open_to, mapping_url)
            print(metadata)

            # Vuforiaへの登録処理
            key_path = os.path.join(settings.BASE_DIR, '../accesskey.json')
            with open(key_path, "r", encoding="utf-8") as key_fp:
                key_dict = json.load(key_fp)
            v = vuforia.Vuforia(access_key=key_dict["ACCESS_KEY"],
                                secret_key=key_dict["SECRET_KEY"])
            if not request.FILES:
                data = {"name": title, "width": 320,
                        "application_metadata": metadata}
            else:
                # Python3では、byte型で扱うので、decode()する。
                image = base64.b64encode(
                        request.FILES['image'].read()).decode('utf-8')
                data = {"name": title, "width": 320, "image": image,
                        "application_metadata": metadata}

            # JSONファイルを作る。
            create_json(contractno, title, open_from, open_to,
                        mapping_url)

            # 画像サムネイルを作る。

            # フォームのデータをDBに保存する。
            new_content = form.save(commit=False)

            res = v.update_target(i.target_id, data)

            # Vuforia APIで登録処理が成功したら続きの処理を行う。
            if res['result_code'] == "Success":
                new_content.save()

                # 新たな画像が送られてきたとき、
                # 若しくはクリアが選択されたときは既存のファイルは削除する。
                if old_file_name and (i.image.name != old_file_name):
                    os.remove(old_file_path)

                    #logging.basicConfig(
                    #        filename='/Users/js/Desktop/django.log',
                    #        level=logging.INFO)
                    logging.info('ファイル削除\n')
                    #logger = logging.getLogger(__name__)
                    #logger.debug('ファイル削除？')

                return redirect('/content/list')

            # Vuforiaのレスポンスが成功でない場合
            else:
                # エラーメッセージを出力して戻る。
                error_message = res['result_code']
        else:
            return render(request, 'content_edit.html',
                {'form': form, 'contractno': contractno,
                 'company': company, 'error_message': error_message})
    else:
        form = ContentForm(instance=i)
    return render(request, 'content_edit.html',
            {'form': form, 'contractno': contractno,
             'company': company, 'error_message': error_message})


@transaction.atomic
@login_required
@permission_required('cms.running', raise_exception=True)
def edit_open(request, contractno):
    i = Content.objects.get(contract_no__exact=contractno)
    if   i.is_open == 1: new_is_open = 0
    elif i.is_open == 0: new_is_open = 1

    # Vuforiaへの登録処理
    key_path = os.path.join(settings.BASE_DIR, '../accesskey.json')
    with open(key_path, "r", encoding="utf-8") as key_fp:
        key_dict = json.load(key_fp)
    v = vuforia.Vuforia(access_key=key_dict["ACCESS_KEY"],
                        secret_key=key_dict["SECRET_KEY"])
    data = {"active_flag": new_is_open}
    i.save()
    res = v.update_target(i.target_id, data)

    # Vuforia APIで登録処理が成功したら続きの処理を行う。
    if res['result_code'] == "Success":
        i.is_open = new_is_open
        return redirect('/content/list')
    # Vuforiaのレスポンスが成功でない場合
    else:
        # エラーメッセージを出力して戻る。
        error_message = res['result_code']
    return render(request, 'content_list.html',
                  {'error_message': error_message})


#class CustomClearableFileInput(ClearableFileInput):
class CustomFileInput(FileInput):
    """
    下の ContentFormクラスのためのウィジェット
    (画像編集の時の Djangoのデフォルトを修正するために)
    """
    def render(self, name, value, attrs=None):
        substitutions = {
            #uncomment to get 'Currently'
            'initial_text': "", # self.initial_text,
            #'input_text': self.input_text,
            'clear_template': '',
            #'clear_checkbox_label': self.clear_checkbox_label,
            }
        template = '%(input)s'
        substitutions['input'] = Input.render(self, name, value, attrs)

        if value and hasattr(value, "url"):
            #template = self.template_with_initial
            substitutions['initial'] = (
                        '<img src="%s" alt="%s" width="80" height="80"/>'
                                        % (escape(value.url),
                                           escape(force_text(value))))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(
                                                            checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(
                                                            checkbox_id)
                substitutions['clear'] = CheckboxInput().render(
                            checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = (self.template_with_clear
                                                        % substitutions)

        return mark_safe(template % substitutions)

class ContentForm(forms.ModelForm):
    image = forms.ImageField(label='マーカー', required=True,
                             widget=CustomFileInput(),
                             #allow_empty_file=True
                             )
    #image = forms.ImageField(label='マーカー', required=False, widget=forms.FileInput)
    class Meta:
        model = Content
        fields = ('open_from', 'open_to', 'title', 'mapping_url', 'image',)

