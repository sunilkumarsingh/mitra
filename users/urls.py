from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from powermitra.settings import dev

from users import views
# from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet)


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^user/password/reset/$', auth_views.password_reset,
        {'template_name': 'registration/password_reset_form.html',
         'html_email_template_name' : 'registration/password_reset_email.html',
         'from_email' : 'info@powermitra.com', 'subject_template_name' : 'registration/subject.txt'},
         name="password_reset" ),
    url(r'^user/password/reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/password_reset_done.html'}, name='password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, {'template_name': 'registration/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^user/password/done/$', auth_views.password_reset_complete, {'template_name': 'registration/password_reset_complete.html'}, name='password_reset_complete'),





    # url(r'^admin/$', auth_views.login, {'template_name': 'backend/admin/login.html'}, name='admin'),
    url(r'^users/list/$', views.UsersList.as_view()), 
    url(r'^epc/list/', views.EPCList.as_view()),
    url(r'^users/list/$', views.UsersList.as_view()),
    url(r'^usertype/$',views.UserTypeList.as_view()),
    url(r'^investor/list/', views.InvestorList.as_view()),
    url(r'^project/list/(?P<id>[0-9]+)/$', views.ProjectList.as_view()),
    url(r'^inactiveuser/(?P<id>[0-9]+)/$', views.UpdateUserStatus.as_view(), name='inactive-user'),
    url(r'^password/reset/$', views.UserPasswordReset.as_view(), name="password_reset"),
    url(r'^password/modify/$', views.ModifyUserPassword.as_view(), name="password_modify"),
    url(r'^users/register/$', views.RegisterUserView.as_view()),
    url(r'^consumerepc/list/(?P<id>[0-9]+)/$', views.ConsumerEPCList.as_view()),
    url(r'^epcreview/(?P<id>[0-9]+)/$', views.ConsumerWithEPCReview.as_view()),    
]


if dev.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]