from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout, \
                                update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db.models.query import Q
from django.conf import settings

# CustomClearableFileInput用に。
from django.utils.safestring import mark_safe
from django.utils.html import escape, conditional_escape
from django.utils.encoding import force_text
from django.forms.widgets import ClearableFileInput, Input, CheckboxInput

from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser, \
                       Content

import os, json

def create_json(contractno, title, open_from, open_to, mapping_url):
    """
    JSONファイルを作成・保存する関数
    """
    json_dict = {}
    json_dict['CONTRACT_NO'] = contractno
    json_dict['TITLE'] = title
    json_dict['OPEN_FROM'] = open_from.strftime('%Y-%m-%d')
    json_dict['OPEN_TO'] = open_to.strftime('%Y-%m-%d')
    json_dict['TYPE'] = 'url'
    json_dict['URL'] = mapping_url

    p = os.path.join(settings.BASE_DIR, 'cms/static/json',
                     contractno + '.json')
    with open(p, "w", encoding="utf-8") as json_fp:
        #json.dump(json_dict, json_fp)
        json.dump(json_dict, json_fp, ensure_ascii=False)

@login_required
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

    return render(request, 'content_list.html',
                  {'content_list': content_list})

@login_required
def new(request, contractno):
    i = Content.objects.get(contract_no__exact=contractno)
    company = i.company
    if request.POST:
        form = ContentForm(request.POST, request.FILES, instance=i)
        if form.is_valid():
            # Vuforia APIで登録処理が成功したら続きの処理を行う。

            open_from   = form.cleaned_data['open_from']
            open_to     = form.cleaned_data['open_to']
            title       = form.cleaned_data['title']
            mapping_url = form.cleaned_data['mapping_url']

            # JSONファイルを作る。
            create_json(contractno, title, open_from, open_to, mapping_url)

            # 画像サムネイルを作る。

            # フォームのデータをDBに保存する。
            form.save()

            return redirect('/content/list')
        else:
            return render(request, 'content_new.html',
                {'form': form, 'contractno': contractno, 'company': company})
    else:
        form = ContentForm()
    return render(request, 'content_new.html',
            {'form': form, 'contractno': contractno, 'company': company})

@login_required
def edit(request, contractno):
    i = Content.objects.get(contract_no__exact=contractno)
    company = i.company
    if request.POST:
        form = ContentForm(request.POST, request.FILES, instance=i)
        if form.is_valid():
            # Vuforia APIで変更処理が成功したら続きの処理を行う。

            open_from   = form.cleaned_data['open_from']
            open_to     = form.cleaned_data['open_to']
            title       = form.cleaned_data['title']
            mapping_url = form.cleaned_data['mapping_url']

            # JSONファイルを作る。
            create_json(contractno, title, open_from, open_to, mapping_url)

            # 画像サムネイルを作る。

            # フォームのデータをDBに保存する。
            form.save()

            return redirect('/content/list')
        else:
            return render(request, 'content_edit.html',
                {'form': form, 'contractno': contractno, 'company': company})
    else:
        form = ContentForm(instance=i)
    return render(request, 'content_edit.html',
            {'form': form, 'contractno': contractno, 'company': company})


class CustomClearableFileInput(ClearableFileInput):
    """
    下の ContentFormクラスのためのウィジェット
    (画像編集の時の Djangoのデフォルトを修正するために)
    """
    def render(self, name, value, attrs=None):
        substitutions = {
            #uncomment to get 'Currently'
            'initial_text': "", # self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
            }
        template = '%(input)s'
        substitutions['input'] = Input.render(self, name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
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
    image = forms.ImageField(label='マーカー', required=False,
                             widget=CustomClearableFileInput())
    #image = forms.ImageField(label='マーカー', required=False, widget=forms.FileInput)
    class Meta:
        model = Content
        fields = ('open_from', 'open_to', 'title', 'mapping_url', 'image',)

