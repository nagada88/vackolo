from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 50, label="név", label_suffix="")
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 150, label="email", label_suffix="")
    message = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control'}), max_length = 2000, label="üzenet", label_suffix="")

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        try:
            send_mail(subject, message,  body['email_address'], [body['email_address']])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect("kapcsolat")
        
        
class OrokbeFogadasForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 50, label="név", label_suffix="")
    email_address = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length = 150, label="email", label_suffix="")
    message = forms.CharField(widget = forms.Textarea(attrs={'class': 'form-control'}), max_length = 2000, label="Kérlek írj eddigi tapasztalataidról, és hogy miért őt választanád?", label_suffix="")

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        try:
            send_mail(subject, message,  body['email_address'], [body['email_address']])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect("kapcsolat")
