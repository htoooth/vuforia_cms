from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout, \
                                update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.db.models.query import Q

from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser, \
                       Content
from cms.utils.decorators import my_permission_required
from cms.forms import ContractForm

NOT_ADMIN_CHOICES = ((3, 'Company'),)

@transaction.atomic
@login_required
@my_permission_required('cms.running', raise_exception=True)
def new(request, companyid):
    if request.user.acc_type_id != 3:
        if request.POST:
            form = ContractForm(request.POST)
            if form.is_valid():
                new_contract = form.save(commit=False)
                company = UserProfile.objects.get(
                        acc_type_id__exact=3, user_id__exact=int(companyid))
                new_contract.company = company
                new_contract.save()
                return redirect('/account/list')
            else:
                return render(request, 'contract_new.html',
                        {'form': form, 'companyid': int(companyid)})
        else:
            form = ContractForm()
        return render(request, 'contract_new.html',
                        {'form': form, 'companyid': int(companyid)})
    else:
        # Companyは新規作成はできない。
        return redirect('/account/list')


@transaction.atomic
@login_required
@my_permission_required('cms.running', raise_exception=True)
def edit(request, contractno):
    i = Content.objects.get(contract_no__exact=contractno)
    if request.POST:
        i.delete()
        return redirect('/content/list')
    else:
        return render(request, 'contract_edit.html', {'content': i})

