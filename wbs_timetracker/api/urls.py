from django.conf.urls import url, include

from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from api.projects.views import ProjectsModelViewSet
from api.bookings.views import BookingsModelViewSet


projects_router = DefaultRouter()
projects_router.register(r'projects', ProjectsModelViewSet)

bookings_router = DefaultRouter()
bookings_router.register(r'bookings', BookingsModelViewSet, base_name='workeffort')

urlpatterns = [
    url(r'^login', views.obtain_auth_token),
    url(r'^', include(projects_router.urls)),
    url(r'^projects/(?P<project_id>\d+)/', include(bookings_router.urls)),
]
