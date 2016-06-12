from django.conf.urls import url

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.projects.views import ProjectsModelViewSet


router = DefaultRouter()
router.register(r'projects', ProjectsModelViewSet)

urlpatterns = [
    url(r'^login', views.obtain_auth_token),
]

urlpatterns += router.urls
