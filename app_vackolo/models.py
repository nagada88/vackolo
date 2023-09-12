from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.

class ImageHandlerMixin():
    def save(self, *args, **kwargs):
        if not self.photo.closed:
            if not self.make_thumbnail():
                # set to a default thumbnail
                raise Exception('Could not create thumbnail - is the file type valid?')

        super(ImageHandlerMixin, self).save(*args, **kwargs)


    def make_thumbnail(self):

        image = Image.open(self.photo)
        image.thumbnail((1000,1000), Image.BICUBIC)

        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False  # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.photo_tumb.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True    

class AllatFaj(models.TextChoices):
    kutya = "kutya", _("kutya")
    cica = "cica", _("cica")
    egyeb = "egyeb", _("egyéb")

class AllatMeret(models.TextChoices):
    kicsi = "kicsi", _("kistestű")
    kozepes = "kozepes", _("közepes testű")
    nagy = "nagy", _("nagytestű")

class Ivar(models.TextChoices):
    fiu = "fiu", _("fiú")
    lany = "lany", _("lány")

class Allat(TranslatableModel):
    translations = TranslatedFields(leiras=models.TextField(default="Leírás később érkezik. Amennyiben a képek alapján érdeklődnél, keress facebook messengeren vagy telefonon."))
    faj = models.CharField(max_length=200, choices=AllatFaj.choices, default=_("kutya"), verbose_name = _("kutya/cica"))
    meret = models.CharField(max_length=200, choices=AllatMeret.choices, default=_("kicsi"), verbose_name = _("méret"))
    ivar = models.CharField(max_length=200, choices=Ivar.choices, default=_("fiu"), verbose_name = _("ivar"))
    nev = models.CharField(max_length=200, verbose_name = "név")
    bekerulesideje = models.DateField()
    szuletesiideje = models.DateField()
    ivartalanitva = models.BooleanField()
    eletkor = models.IntegerField(blank=True, null=True, editable=False)
    virtualisgazdi = models.TextField(default="nincs")
    orokbeadva = models.BooleanField(default = False)

    def __str__(self):
        return self.nev

    def save(self, *args, **kwargs):
        self.eletkor = int(((datetime.date.today()  - self.szuletesiideje).days)/365.25)
        print(self.eletkor)
        super().save(*args, **kwargs)

class AllatMainImage(ImageHandlerMixin, models.Model):
    allat = models.ForeignKey(Allat, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='app_menhely/img/photos/', verbose_name = _("kiemelt kép"))
    photo_tumb = models.ImageField(upload_to='app_menhely/img/thumbs/', editable=False)

class AllatImage(ImageHandlerMixin, models.Model):
    allat = models.ForeignKey(Allat, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='app_menhely/img/photos/', verbose_name = _("galéria kép"))
    photo_tumb = models.ImageField(upload_to='app_menhely/img/thumbs/', editable=False)      
 