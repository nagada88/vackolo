from django import forms
from django.core.mail import BadHeaderError, send_mail
from django.utils.translation import gettext_lazy as _
from django.core import validators

class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 50, label=_("név"), label_suffix="")
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 150, label=_("email"), label_suffix="")
    message = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control'}), max_length = 2000, label=_("üzenet"), label_suffix="")

    
class OrokbeFogadasForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 50, label=_("név"), label_suffix="")
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 150, label=_("email"), label_suffix="")
    message = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control'}), max_length = 2000, label=_("Kérlek írj eddigi tapasztalataidról, és hogy miért őt választanád?"), label_suffix="")

