from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required

from cms.models import UserProfile, AdminUser, AgencyUser, CompanyUser
from cms.forms import Form_connection, LoginForm

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
            if user.has_perm('cms.running') or user.acc_type_id == 1:
            #if user.is_active:
                login(request, user)
                #return render(request, 'login.html', {'form': form})
                return redirect('/account/list')
                #return redirect('/')
                #return HttpResponse("ログイン成功" + "\n" + identifier)
            else:
                return HttpResponse("アカウントが無効です。")
        else:
            return HttpResponse("Your username and password didn't match.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')
    #return HttpResponse("ログアウト")

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

