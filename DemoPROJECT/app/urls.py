from django.urls import include, path
from rest_framework import routers
from .import views


router = routers.DefaultRouter()
router.register(r'app', views.DataViewSet,basename='app')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>', views.snippet_detail),

]

