from django.conf.urls import url, include
from django.contrib import admin

from api.urls import urlpatterns as api_urlpatterns


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urlpatterns)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
