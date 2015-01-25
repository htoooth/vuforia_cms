from django.http import HttpResponse
from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import authenticate, login, logout
from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser

# cf. 「Django完全解説」p.278、「TDD with Python」p.245
#     「Django Essentials」No.1396
def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id', None)
        acc_type_id = request.POST.get('acc_type_id', None)
        if acc_type_id == '1':
            identifier = 'ad-' + str(user_id).zfill(8)
        elif acc_type_id == '2':
            identifier = 'ag-' + str(user_id).zfill(8)
        elif acc_type_id == '3':
            identifier = 'co-' + str(user_id).zfill(8)
        password = request.POST.get('password', None)

        # TODO: フォームのバリデーション

        # フォームの認証
        user = authenticate(identifier=identifier, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #return render(request, 'login.html', {'form': form})
                return redirect('/')
                #return HttpResponse("ログイン成功" + "\n" + identifier)
            else:
                return HttpResponse("アカウントが無効です。")
        else:
            return HttpResponse("Your username and password didn't match.")
    else:
        form = UserProfileForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')
    #return HttpResponse("ログアウト")


class UserProfileForm(forms.Form):
    user_id = forms.IntegerField(label="ユーザーID")
    acc_type_id = forms.ChoiceField(label="アカウントタイプ",
                                  choices=UserProfile.ACC_TYPE_CHOICES)
    #identifier = forms.CharField(label="アカウント")
    password = forms.CharField(label="パスワード",
                               widget=forms.PasswordInput)


def page(request):
    if request.POST:
        form = Form_connection(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                if request.GET.get('next') is not None:
                    return redirect(request.GET['next'])
        else:
            return render(request,
                          'en/public/connection.html',
                          {'form': form})
    else:
        form = Form_connection()
    return render(request,
                  'en/public/connection.html',
                  {'form': form})

class Form_connection(forms.Form):
    username = forms.CharField(label="Login")
    password = forms.CharField(label="Password",
                               widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(Form_connection, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Wrong login or password")
        return self.cleaned_data
