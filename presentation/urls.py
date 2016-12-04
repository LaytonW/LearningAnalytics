from django.conf.urls import include, url
from .views import login_view as lv

urlpatterns = [
    url(r'^$', lv.login, name='login'),
]
