from django.conf.urls import include, url
import presentation.views as views

urlpatterns = [
    url(r'^$', views.login, name='login'),
]
