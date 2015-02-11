from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vuforia_cms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'cms.views.session.login_view', name='login'),
    url(r'^logout$', 'cms.views.session.logout_view', name='logout'),

    url(r'^account/list$', 'cms.views.account.list',
        name='account_list'),
    url(r'^account/new$', 'cms.views.account.new',
        name='account_new'),
    url(r'^account/edit/(?P<acctypeid>\d+)/(?P<userid>\d+)$',
        'cms.views.account.edit', name='account_edit'),
    url(r'^account/edit_pw/(?P<acctypeid>\d+)/(?P<userid>\d+)$',
        'cms.views.account.edit_pw', name='account_edit_pw'),

    url(r'^content/list$', 'cms.views.content.list',
        name='content_list'),

    url(r'^contract/new/(?P<companyid>\d+)$', 'cms.views.contract.new',
        name='contract_new'),
    url(r'^contract/edit/(?P<contractno>\d+)$',
        'cms.views.contract.edit', name='contract_edit'),

    url(r'^admin/', include(admin.site.urls)),
)
