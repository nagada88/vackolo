from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from app_vackolo.forms import ContactForm, OrokbeFogadasForm
from .models import *
from .filters import AllatFilter

class Bemutatkozas(ListView):
    model = Allat
    template_name = "bemutatkozas.html"
   
def orokbefogadas(request):
    filtered_animal = AllatFilter(request.GET, queryset=Allat.objects.all().exclude(orokbeadva = True))
    paginator = Paginator(filtered_animal.qs, 8)
    
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'orokbefogadas.html', {'page_obj': page_obj, 'filtered_animal': filtered_animal})
    
# class Orokbefogadas(ListView):
    # model = Allat
    # template_name = "orokbefogadas.html"
    
    # def get_queryset(self):
        # qs = self.model.objects.all()
        # animal_filtered_list = AllatFilter(self.request.GET, queryset=qs)
        # return animal_filtered_list    

def allat(request):
    allatid = request.GET.get('allatid')
    allat = Allat.objects.get(id=allatid)
    allatpictures = AllatImage.objects.filter(allat=allat)
    
    allatok = Allat.objects.exclude(pk = allatid)
    paginator = Paginator(allatok, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    picture_quantity = len(allatpictures)
    breakpnumber = round(picture_quantity/3.)
    breakpremaining = picture_quantity%3
    bplist = [0]
    if breakpremaining in [0,2]:
        bplist.append(breakpnumber)
        bplist.append(2*breakpnumber)
    elif breakpremaining in [1]:
        bplist.append(breakpnumber+1)
        bplist.append(2*breakpnumber+1)


    return render(request, 'allat.html', {'allat': allat, 'allatpictures': allatpictures,'bplist': bplist, 'page_obj': page_obj})

def formorokbe(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'name': form.cleaned_data['name'],
                'email_address': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message,  body['email_address'], [body['email_address']])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("gallery.html")

    form = OrokbeFogadasForm()
    allatid = request.GET.get('allatid')
    allat = Allat.objects.get(id=allatid)
    
    return render(request, "formorokbe.html", {'form': form, 'allat': allat})    


class Tamogatas(TemplateView):
    template_name = "tamogatas.html"
    
class Kapcsolat(FormView):
    template_name = "kapcsolat.html"
    form_class = ContactForm
    success_url = "kapcsolat"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)