from django.urls import include, path
from rest_framework import routers
from .import views
from .views import DataAPIView

router = routers.DefaultRouter()
router.register(r'app1', views.DataViewSet,basename='app1')
app_name = "app1"


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),

    #for view all i am using diff viewset
    path('data_apiview/', views.DataAPIView.as_view()),
    path('data_apiview/<int:pk>/', views.DataAPIViewDetail.as_view()),


]