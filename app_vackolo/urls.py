from django.urls import include, path, re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.Bemutatkozas.as_view(), name='bemutatkozas'),
    re_path(r'bemutatkozas', views.Bemutatkozas.as_view(), name='bemutatkozas'),
    re_path(r'orokbefogadas', views.orokbefogadas, name='orokbefogadas'),
    re_path(r'allat', views.allat, name='allat'),
    re_path(r'tamogatas', views.Tamogatas.as_view(), name='tamogatas'),
    re_path(r'kapcsolat', views.Kapcsolat.as_view(), name='kapcsolat'),
    re_path(r'formorokbe', views.formorokbe, name='kapcsolat'),
    ]