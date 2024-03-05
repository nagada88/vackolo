from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin
from django.conf import settings

class PictureInline(admin.StackedInline):
    model = AllatImage
    
class MainPictureInline(admin.StackedInline):
    model = AllatMainImage
    
class AllatAdmin(TranslatableAdmin):
    inlines = [PictureInline, MainPictureInline]
    def get_exclude(self, request, obj=None):
        excluded_fields =  []
        if obj is not None and self.get_form_language(request) != settings.LANGUAGE_CODE:
            for field in self.model._meta.get_fields():
                if field.name not in obj._parler_meta.get_all_fields():
                    excluded_fields.append(field.name)
        if excluded_fields:
            self.fields = ()
            self.exclude = ()
        return excluded_fields

class BemutatkozasAdmin(TranslatableAdmin):
    model = Bemutatkozas

class TamogatasAdmin(TranslatableAdmin):
    model = Tamogatas

class OnkentesMunkaAdmin(TranslatableAdmin):
    model = OnkentesMunka
    
# Register your models here.
admin.site.register(Allat, AllatAdmin)
admin.site.register(Bemutatkozas, BemutatkozasAdmin)
admin.site.register(Tamogatas, TamogatasAdmin)
admin.site.register(OnkentesMunka, OnkentesMunkaAdmin)
admin.site.register(Kapcsolat)