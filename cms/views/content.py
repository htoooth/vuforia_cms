from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout, \
                                update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db.models.query import Q

from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser, \
                       Content

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
def edit(request, acctypeid, userid):
    if request.POST:
        i = UserProfile.objects.get(acc_type_id=acctypeid,
                                    user_id=userid)
        form = ContentForm(request.POST, instance=i)
        if form.is_valid():
            form.save()
            return redirect('/account/list')
        else:
            return render(request, 'account_edit.html',
                          {'form': form,
                           'acctypeid': int(acctypeid),
                           'userid': int(userid)})
    else:
        form = ContentForm(
            instance=UserProfile.objects.get(acc_type_id=acctypeid,
                                             user_id=userid)
        )
        if request.user.acc_type_id != 1:
            form.fields.get('acc_type_id').choices = NOT_ADMIN_CHOICES

    # 編集アカウントがCompanyの場合には契約情報を取得して渡す。
    if acctypeid == "3":
        company = UserProfile.objects.get(acc_type_id__exact=3,
                                          user_id__exact=int(userid))
        if request.user.acc_type_id == 1:
            cont_list = Content.objects.filter(
                company__exact=company,
                company__parent_admin_id__exact=request.user.id)
        elif request.user.acc_type_id == 2:
            cont_list = Content.objects.filter(
                company__exact=company,
                company__parent_agency_id__exact=request.user.id)
        else:
            cont_list = None
    else:
        cont_list = None

    return render(request, 'account_edit.html',
                  {'form': form,
                   'acctypeid': int(acctypeid), 'userid': int(userid),
                   'cont_list': cont_list})


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('open_from', 'open_to', 'title', 'mapping_url', 'image',)

