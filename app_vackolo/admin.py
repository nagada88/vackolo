from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin

class PictureInline(admin.StackedInline):
    model = AllatImage
    
class MainPictureInline(admin.StackedInline):
    model = AllatMainImage
    
class AllatAdmin(TranslatableAdmin):
    inlines = [PictureInline, MainPictureInline]


# Register your models here.
admin.site.register(Allat, AllatAdmin)