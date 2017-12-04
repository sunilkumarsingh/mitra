from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework import routers
from powermitra.settings import dev

from users import views

router = routers.DefaultRouter()
router.register(r'users', views.UsersViewSet)


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'', include('django.contrib.auth.urls')),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/$', auth_views.login, {'template_name': 'backend/admin/login.html'}, name='admin'),	
    url(r'^epc/list/', views.EPCList.as_view()),
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