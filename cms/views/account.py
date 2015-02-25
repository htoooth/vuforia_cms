from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, \
                                update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, \
                                           permission_required
from django.db import transaction
from django.db.models.query import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser, \
                       Content
from vws import vuforia

import os, json

NOT_ADMIN_CHOICES = ((3, 'Company'),)
PW_MIN_LENGTH = 8

@login_required
@permission_required('cms.running', raise_exception=True)
def list(request):
    # ログインしているユーザー所有のアカウントをすべて取得する。
    if request.user.acc_type_id == 1:
        acc_list = UserProfile.objects.filter(
            Q(identifier=request.user.identifier) |
            Q(parent_admin_id__exact=request.user.user_id)
        ).order_by('acc_type_id')
    elif request.user.acc_type_id == 2:
        acc_list = UserProfile.objects.filter(
            Q(identifier=request.user.identifier) |
            Q(parent_agency_id__exact=request.user.user_id)
        ).order_by('acc_type_id')
    elif request.user.acc_type_id == 3:
        acc_list = UserProfile.objects.filter(identifier=request.user.identifier)

    paginator = Paginator(acc_list, 2)
    page = request.GET.get('page')
    try:
        accs = paginator.page(page)
    except PageNotAnInteger:
        accs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        accs = paginator.page(paginator.num_pages)

    # テンプレートでは回数（int型）でイテレートできない？
    loop = [x for x in range(paginator.num_pages)]
    return render(request, 'account_list.html',
                  {"loop": loop, "accs": accs})

@transaction.atomic
@login_required
@permission_required('cms.running', raise_exception=True)
def new(request):
    if request.user.acc_type_id != 3:
        if request.POST:
            form = CreateUserProfileForm(request.POST)
            if form.is_valid():
                acc_type_id = form.cleaned_data['acc_type_id']
                enterprise = form.cleaned_data['enterprise']
                person = form.cleaned_data['person']
                address = form.cleaned_data['address']
                email = form.cleaned_data['email']
                phone_number = form.cleaned_data['phone_number']
                password = form.cleaned_data['password']

                if request.user.acc_type_id == 1:
                    parent_admin_id = request.user.parent_admin_id
                    parent_agency_id = None
                elif request.user.acc_type_id == 2:
                    parent_admin_id = request.user.parent_admin_id
                    parent_agency_id = request.user.user_id

                new_account = UserProfile.objects.create_user(
                                acc_type_id=acc_type_id,
                                parent_admin_id=parent_admin_id,
                                parent_agency_id=parent_agency_id,
                                enterprise=enterprise, person=person,
                                address=address, email=email,
                                phone_number=phone_number,
                                password=password)

                return redirect('/account/list')
            else:
                return render(request, 'account_new.html', {'form': form})
        else:
            form = CreateUserProfileForm()
            if request.user.acc_type_id != 1:
                form.fields.get('acc_type_id').choices = NOT_ADMIN_CHOICES
        return render(request, 'account_new.html', {'form': form})
    else:
        # Companyは新規作成はできない。
        return redirect('/account/list')

@transaction.atomic
@login_required
@permission_required('cms.running', raise_exception=True)
def edit(request, acctypeid, userid):
    if request.POST:
        i = UserProfile.objects.get(acc_type_id=acctypeid,
                                    user_id=userid)
        form = UserProfileForm(request.POST, instance=i)
        if form.is_valid():
            form.save()
            return redirect('/account/list')
        else:
            return render(request, 'account_edit.html',
                          {'form': form,
                           'acctypeid': int(acctypeid),
                           'userid': int(userid)})
    else:
        form = UserProfileForm(
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
                company__parent_admin_id__exact=request.user.user_id)
        elif request.user.acc_type_id == 2:
            cont_list = Content.objects.filter(
                company__exact=company,
                company__parent_agency_id__exact=request.user.user_id)
        else:
            cont_list = Content.objects.filter(company__exact=company)
    else:
        cont_list = None

    return render(request, 'account_edit.html',
                  {'form': form,
                   'acctypeid': int(acctypeid), 'userid': int(userid),
                   'cont_list': cont_list})

@transaction.atomic
@login_required
@permission_required('cms.running', raise_exception=True)
def edit_status(request, acctypeid, userid):
    i = UserProfile.objects.get(acc_type_id=acctypeid,
                                user_id=userid)

    perm = Permission.objects.get(codename='running')

    if i.user_running == 0:
        i.user_running = 1
        i.user_permissions.add(perm)
    else:
        i.user_running = 0
        i.user_permissions.remove(perm)

        # Companyを停止した場合は、その全てのマーカーを非公開にする。
        if i.acc_type_id == 3:
            key_path = os.path.join(settings.BASE_DIR, '../accesskey.json')
            with open(key_path, "r", encoding="utf-8") as key_fp:
                key_dict = json.load(key_fp)
            v = vuforia.Vuforia(access_key=key_dict["ACCESS_KEY"],
                                secret_key=key_dict["SECRET_KEY"])
            contents = Content.objects.filter(company__exact=i)
            data = {"active_flag": 0}
            for c in contents:
                res = v.update_target(c.target_id, data)
                # Vuforia APIで登録処理が成功したら続きの処理を行う。
                if res['result_code'] == "Success":
                    c.is_open = 0
                    c.save()
    i.save()
    return redirect('/account/list')


@transaction.atomic
@login_required
@permission_required('cms.running', raise_exception=True)
def edit_pw(request, acctypeid, userid):
    if request.POST:
        i = UserProfile.objects.get(acc_type_id=acctypeid,
                                    user_id=userid)
        form = ValidatingPasswordChangeForm(user=i, data=request.POST)
        #form = UserProfilePasswordForm(request.POST, instance=i)
        if form.is_valid():
            #password = form.cleaned_data['password']

            if request.user.acc_type_id == 1:
                parent_admin_id = request.user.parent_admin_id
                parent_agency_id = None
            elif request.user.acc_type_id == 2:
                parent_admin_id = request.user.parent_admin_id
                parent_agency_id = request.user.user_id
            elif request.user.acc_type_id == 3:
                parent_admin_id = request.user.parent_admin_id
                parent_agency_id = request.user.user_id

            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/list')
        else:
            return render(request, 'account_edit_pw.html',
                          {'form': form,
                           'acctypeid': int(acctypeid),
                           'userid': int(userid)})
    else:
        form = ValidatingPasswordChangeForm(
            user=UserProfile.objects.get(acc_type_id=acctypeid,
                                             user_id=userid)
        )
    return render(request, 'account_edit_pw.html',
                  {'form': form,
                   'acctypeid': int(acctypeid), 'userid': int(userid)})


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('acc_type_id', 'enterprise', 'person', 'address',
                  'email','phone_number',)

class CreateUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('acc_type_id', 'enterprise', 'person', 'address',
                  'email','phone_number', 'password',)
        widgets = {'password': forms.PasswordInput(),}

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # At least PW_MIN_LENGTH long
        if len(password) < PW_MIN_LENGTH:
            raise forms.ValidationError(
                "The new password must be at least %d characters long." % PW_MIN_LENGTH)
        # At least one letter and one non-letter
        first_isalpha = password[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password):
            raise forms.ValidationError(
                "The new password must contain at least one letter and at least one digit or punctuation character.")
        return password


class ValidatingPasswordChangeForm(PasswordChangeForm):
    def clean_new_password1(self):
        password1 = self.cleaned_data.get('new_password1')
        # At least PW_MIN_LENGTH long
        if len(password1) < PW_MIN_LENGTH:
            raise forms.ValidationError(
                "The new password must be at least %d characters long." % PW_MIN_LENGTH)
        # At least one letter and one non-letter
        first_isalpha = password1[0].isalpha()
        if all(c.isalpha() == first_isalpha for c in password1):
            raise forms.ValidationError(
                "The new password must contain at least one letter and at least one digit or punctuation character.")
        return password1
