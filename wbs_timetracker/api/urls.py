from django.conf.urls import url, include

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.projects.views import ProjectsModelViewSet
from api.bookings.views import BookingsModelViewSet
from api.workpackages.views import WorkpackagesModelViewSet
from api.users.views import WbsUserModelViewSet, WbsUserProjectsModelViewSet


base_router = DefaultRouter()
base_router.register(r'projects', ProjectsModelViewSet, base_name='dbidentifier')
base_router.register(r'users', WbsUserModelViewSet, base_name='wbsuser')

bookings_router = DefaultRouter()
bookings_router.register(r'bookings', BookingsModelViewSet, base_name='workeffort')

workpackage_router = DefaultRouter()
workpackage_router.register(r'workpackages', WorkpackagesModelViewSet, base_name='workpackage')

user_project_router = DefaultRouter()
user_project_router.register(r'projects', WbsUserProjectsModelViewSet, base_name='userprojects')

urlpatterns = [
    url(r'^login', views.obtain_auth_token),
    url(r'^', include(base_router.urls)),
    url(r'^projects/(?P<project_id>\d+)/', include(bookings_router.urls)),
    url(r'^projects/(?P<project_id>\d+)/', include(workpackage_router.urls)),
    url(r'^users/(?P<user_id>\d+)/', include(user_project_router.urls)),
]
