from django.shortcuts import render
from cms.models import (UserProfile, AdminUser, AgencyUser, CompanyUser,
                        Content)

def list(request):
    # 当該ユーザーの持つ全コンテンツを渡す。
    # とりあえず Company
    cid = 1
    contents_list = Content.object.filter(user_id__exact=cid, contract_no=c_no)

    return render(request, 'content_list.html', {'content_list': contents_list})

