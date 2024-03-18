from django.urls import include, path, re_path
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticSitemap 

sitemaps = {
    'static':StaticSitemap, #add StaticSitemap to the dictionary
}

urlpatterns = [
    re_path(r'^$', views.bemutatkozas, name='bemutatkozas'),
    re_path(r'bemutatkozas', views.bemutatkozas, name='bemutatkozas'),
    re_path(r'orokbefogadas', views.orokbefogadas, name='orokbefogadas'),
    re_path(r'allat', views.allat, name='allat'),
    re_path(r'tamogatas', views.tamogatas, name='tamogatas'),
    re_path(r'kapcsolat', views.kapcsolativ, name='kapcsolat'),
    re_path(r'formorokbe', views.formorokbe, name='kapcsolat'),
    re_path(r'sikeresmail', views.sikeresmail, name='sikeresmail'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    ]

