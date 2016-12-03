from django.conf.urls import include, url

urlpatterns = [
    url(r'^$', lv.login, name='login'),
]
