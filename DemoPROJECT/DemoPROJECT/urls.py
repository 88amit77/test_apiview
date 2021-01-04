from django.conf.urls import url, include
urlpatterns = [
    url(r'^app/', include('app.urls')),
    url(r'^app1/', include('app1.urls')),
]