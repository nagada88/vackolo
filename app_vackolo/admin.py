from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin

class PictureInline(admin.StackedInline):
    model = AllatImage
    
class MainPictureInline(admin.StackedInline):
    model = AllatMainImage
    
class AllatAdmin(TranslatableAdmin):
    inlines = [PictureInline, MainPictureInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'logo', 'background_image', ...),
        }),
        (_("Translatable Fields"), {
            'fields': ('description',)
        }),

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