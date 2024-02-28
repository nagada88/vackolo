from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from PIL import Image
from io import BytesIO
import os
from django.core.files.base import ContentFile
from parler.models import TranslatableModel, TranslatedFields
from django_quill.fields import QuillField

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
 
class Bemutatkozas(TranslatableModel):
    translations = TranslatedFields(content=QuillField())

    def save(self, *args, **kwargs):
        if not self.pk and Bemutatkozas.objects.exists():
        # if you'll not check for self.pk 
        # then error will also be raised in the update of exists model
            raise ValidationError('Csak egy bemutatkozas bejegyzes lehet')
        return super(Bemutatkozas, self).save(*args, **kwargs)
        
class Tamogatas(TranslatableModel):
    translations = TranslatedFields(content=QuillField())
    szamlaszam = models.CharField(max_length=50, default="")
    paypalemail = models.CharField(max_length=50, default="")
    adoszam = models.CharField(max_length=50, default="")
    
    def save(self, *args, **kwargs):
        if not self.pk and Tamogatas.objects.exists():
        # if you'll not check for self.pk 
        # then error will also be raised in the update of exists model
            raise ValidationError('Csak egy tamogatas bejegyzes lehet')
        return super(Tamogatas, self).save(*args, **kwargs)
        
class OnkentesMunka(TranslatableModel):
    translations = TranslatedFields(content=QuillField())

    def save(self, *args, **kwargs):
        if not self.pk and OnkentesMunka.objects.exists():
        # if you'll not check for self.pk 
        # then error will also be raised in the update of exists model
            raise ValidationError('Csak egy onkentes munka bejegyzes lehet')
        return super(OnkentesMunka, self).save(*args, **kwargs)
        
class Kapcsolat(models.Model):
    nyitvatartas=models.CharField(max_length=50)
    emailcim=models.CharField(max_length=50, default="")
    telephely=models.CharField(max_length=50, default="")
    telephelyterkeplink=models.CharField(max_length=50, default="")
    facebookmessengercim=models.CharField(max_length=50, default="")


