from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vuforia_cms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'cms.views.session.login_view', name='login'),
    url(r'^logout$', 'cms.views.session.logout_view', name='logout'),
    url(r'^content/list$', 'cms.views.content.list',
        name='content_list'),
    url(r'^admin/', include(admin.site.urls)),
)
