from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.query import Q

from cms.models import (UserProfile, AdminUser, AgencyUser, CompanyUser,
                        Content)

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

