"""
URL configuration for vackolo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path('rosetta/', include('rosetta.urls')),
    path('admin/', admin.site.urls),
    re_path(r'', include('app_vackolo.urls')),
)   + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

admin.site.site_header = "Vackoló Admin"
admin.site.site_title  = "Vackoló Admin Portál"
admin.site.index_title = "Üdvözöllek a Vackoló Admin Portál felületén"