from django.urls import include, path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('MyAPI', views.ApprovalsView)

urlpatterns = [
    # path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('status/', views.approvereject),
]
