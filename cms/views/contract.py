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

NOT_ADMIN_CHOICES = ((3, 'Company'),)

@login_required
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


@login_required
def edit(request, contractno):
    i = Content.objects.get(contract_no__exact=contractno)
    if request.POST:
        i.delete()
        return redirect('/content/list')
    else:
        return render(request, 'contract_edit.html', {'content': i})


class ContractForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ('contracted_at',)