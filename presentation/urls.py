from django.conf.urls import include, url
import presentation.views as views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'login/$', views.login, name='login'),
    url(r'logout/$', views.logout, name='logout'),
    url(r'(?P<userID>[0-9]+)$', views.index, name='index'),
]
