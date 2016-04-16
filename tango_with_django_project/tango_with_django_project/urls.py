from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.conf import settings


urlpatterns = [
	url(r'^rango/', include('rango.urls', namespace="rango")),
    	url(r'^admin/', admin.site.urls),

]

if settings.DEBUG:
	urlpatterns+=patterns(
		'django.views.static',
		(r'^media/(?P<path>.*)',
		'serve',
		{'document_root': settings.MEDIA_ROOT}), )



