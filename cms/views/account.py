from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models.query import Q

from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser

@login_required
def list(request):
    # ログインしているユーザー所有のアカウントをすべて取得する。
    if request.user.acc_type_id == 1:
        acc_list = UserProfile.objects.filter(
            Q(identifier=request.user.identifier) |
            Q(parent_admin_id__exact=request.user.user_id)
        )
    elif request.user.acc_type_id == 2:
        acc_list = UserProfile.objects.filter(
            Q(identifier=request.user.identifier) |
            Q(parent_agency_id__exact=request.user.user_id)
        )
    elif request.user.acc_type_id == 3:
        acc_list = UserProfile.objects.filter(identifier=request.user.identifier)

    return render(request, 'account_list.html', {'acc_list': acc_list})
