from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from PIL import Image, ExifTags
from io import BytesIO
import os
from django.core.files.base import ContentFile
from parler.models import TranslatableModel, TranslatedFields
from django_quill.fields import QuillField
from django.core.exceptions import ValidationError

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
        orientation = None
        for key in ExifTags.TAGS.keys():
            if ExifTags.TAGS[key] == 'Orientation':
                orientation = key
                break
                        
        # EXIF adatokat lekéred és ellenőrzöd, hogy van-e orientáció
        try:
            exif = dict(image._getexif().items())
            orientation_value = exif.get(orientation)  # Biztonságos hozzáférés
        except AttributeError:
            exif = None
            orientation_value = None
            
        if orientation_value == 3:
            image = image.rotate(180, expand=True)
        elif orientation_value == 6:
            image = image.rotate(270, expand=True)
        elif orientation_value == 8:
            image = image.rotate(90, expand=True)
            
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
    fiu = "kan", _("kan")
    lany = "szuka", _("szuka")


class Allat(TranslatableModel):
    translations = TranslatedFields(leiras=models.TextField(default="Leírás később érkezik. Amennyiben a képek alapján érdeklődnél, keress facebook messengeren vagy telefonon."))
    faj = models.CharField(max_length=200, choices=AllatFaj.choices, default=_("kutya"), verbose_name = _("kutya/cica"))
    meret = models.CharField(max_length=200, choices=AllatMeret.choices, default=_("kicsi"), verbose_name = _("méret"))
    ivar = models.CharField(max_length=200, choices=Ivar.choices, default=_("kan"), verbose_name = _("ivar"))
    nev = models.CharField(max_length=200, verbose_name = "név")
    bekerulesideje = models.DateField()
    szuletesiideje = models.DateField()
    ivartalanitva = models.BooleanField(verbose_name=_("ivartalanitva"))
    virtualisgazdi = models.CharField(max_length=200, default="nincs", editable=False)
    orokbeadva = models.BooleanField(default = False)

    def __str__(self):
        return self.nev

    @property
    def eletkor(self):
        eletkor = int(((datetime.date.today()  - self.szuletesiideje).days)/365.25)
        return eletkor

    @property
    def eletkor_float(self):
        eletkor_float = int((datetime.date.today()  - self.szuletesiideje).days/30)
        return eletkor_float
    
    class Meta:
        verbose_name = 'Állat'
        verbose_name_plural = 'Állatok'

class AllatMainImage(ImageHandlerMixin, models.Model):
    allat = models.OneToOneField(Allat, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='app_menhely/img/photos/', verbose_name = _("kiemelt kép"))
    photo_tumb = models.ImageField(upload_to='app_menhely/img/thumbs/', editable=False)

    class Meta:
        verbose_name = 'kiemelt kép'
        verbose_name_plural = 'kiemelt kép'

    def __str__(self):
        return "kiemelt kép"

class AllatImage(ImageHandlerMixin, models.Model):
    allat = models.ForeignKey(Allat, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='app_menhely/img/photos/', verbose_name = _("galéria kép"))
    photo_tumb = models.ImageField(upload_to='app_menhely/img/thumbs/', editable=False) 

    class Meta:
        verbose_name = 'kép'
        verbose_name_plural = 'képek'

    def __str__(self):
        return "kép"
    
class Bemutatkozas(TranslatableModel):
    translations = TranslatedFields(content=QuillField(verbose_name = "Bemutatkozó szöveg"))

    class Meta:
        verbose_name = 'Bemutatkozás'
        verbose_name_plural = 'Bemutatkozás'

    def __str__(self):
        return "Bemutatkozás " + str(self.id)
    
class Tamogatas(TranslatableModel):
    translations = TranslatedFields(content=QuillField(verbose_name = "Támogatás szöveg" ))
    szamlaszam = models.CharField(max_length=50, default="")
    paypalemail = models.CharField(max_length=50, default="")
    adoszam = models.CharField(max_length=50, default="")
    
    def save(self, *args, **kwargs):
        if not self.pk and Tamogatas.objects.exists():
        # if you'll not check for self.pk 
        # then error will also be raised in the update of exists model
            raise ValidationError('Csak egy tamogatas bejegyzes lehet')
        return super(Tamogatas, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Támogatás'
        verbose_name_plural = 'Támogatás'

    def __str__(self):
        return "Támogatás"

class OnkentesMunka(TranslatableModel):
    translations = TranslatedFields(content=QuillField(verbose_name = "Önkéntes munka szöveg"))

    def save(self, *args, **kwargs):
        if not self.pk and OnkentesMunka.objects.exists():
        # if you'll not check for self.pk 
        # then error will also be raised in the update of exists model
            raise ValidationError('Csak egy onkentes munka bejegyzes lehet')
        return super(OnkentesMunka, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Önkéntes Munka Szöveg'
        verbose_name_plural = 'Önkéntes Munka Szöveg'

    def __str__(self):
        return "Önkéntes Munka Szöveg"

class Kapcsolat(models.Model):
    nyitvatartas=models.CharField(max_length=50)
    emailcim=models.CharField(max_length=50, default="")
    telephely=models.CharField(max_length=50, default="")
    telephelyterkeplink=models.CharField(max_length=50, default="")
    facebook=models.CharField(max_length=150, default="")
    telefonszam=models.CharField(max_length=50, default="", verbose_name="telefonszám")
    telefonszam1=models.CharField(max_length=50, default="", verbose_name="másodlagos telefonszám")

    class Meta:
        verbose_name = 'Kapcsolat'
        verbose_name_plural = 'Kapcsolat'

    def __str__(self):
        return "Kapcsolat"
    
class OrokbefogadasSzoveg(TranslatableModel):
    translations = TranslatedFields(content=QuillField(verbose_name = "Örökbefogadás szöveg"))

    def save(self, *args, **kwargs):
        if not self.pk and OrokbefogadasSzoveg.objects.exists():
        # if you'll not check for self.pk 
        # then error will also be raised in the update of exists model
            raise ValidationError('Csak egy onkentes munka bejegyzes lehet')
        return super(OrokbefogadasSzoveg, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Örökbefogadás Szöveg'
        verbose_name_plural = 'Örökbefogadás Szöveg'

    def __str__(self):
        return "Örökbefogadás Szöveg"


