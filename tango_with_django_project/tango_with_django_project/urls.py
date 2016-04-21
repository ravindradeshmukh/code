from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.conf import settings

from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
	def get_success_url(self, request):
		return '/rango/'

urlpatterns = [
	url(r'^rango/', include('rango.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


