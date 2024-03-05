from django.urls import include, path, re_path

from . import views

from django.contrib import admin

admin.site.index_template = 'admin/index.html'
admin.autodiscover()

urlpatterns = [
    re_path(r'^$', views.bemutatkozas, name='bemutatkozas'),
    re_path(r'bemutatkozas', views.bemutatkozas, name='bemutatkozas'),
    re_path(r'orokbefogadas', views.orokbefogadas, name='orokbefogadas'),
    re_path(r'allat', views.allat, name='allat'),
    re_path(r'tamogatas', views.tamogatas, name='tamogatas'),
    re_path(r'kapcsolat', views.kapcsolativ, name='kapcsolat'),
    re_path(r'formorokbe', views.formorokbe, name='kapcsolat'),
    re_path(r'sikeresmail', views.sikeresmail, name='sikeresmail'),
    ]
