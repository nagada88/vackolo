from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from app_vackolo.forms import ContactForm
from .models import *
from .filters import AllatFilter
import datetime


  
def bemutatkozas(request):
    bemutatkozas = Bemutatkozas.objects.get(id=1)
    kapcsolat = Kapcsolat.objects.get(id=1)
    allatszam = Allat.objects.all().count()
    orokbeadottszam = allatszam - Allat.objects.all().exclude(orokbeadva = True).count()
    orokbevar = allatszam - orokbeadottszam
    today = datetime.date.today()
    year = today.year
    ezota = today.year - 2006

    filtered_animal = Allat.objects.all().exclude(orokbeadva = True)[:4]

    return render(request, 'bemutatkozas.html', {'bemutatkozas': bemutatkozas,'filtered_animal': filtered_animal, 'kapcsolat': kapcsolat, 'orokbevar': orokbevar, 'orokbeadottszam': orokbeadottszam, 'ezota': ezota})
    
    
def orokbefogadas(request):
    filtered_animal = AllatFilter(request.GET, queryset=Allat.objects.all().exclude(orokbeadva = True))
    paginator = Paginator(filtered_animal.qs, 8)
    kapcsolat = Kapcsolat.objects.get(id=1)

    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'orokbefogadas.html', {'page_obj': page_obj, 'filtered_animal': filtered_animal, 'kapcsolat': kapcsolat})

def allat(request):
    allatid = request.GET.get('allatid')
    allat = Allat.objects.get(id=allatid)
    allatpictures = AllatImage.objects.filter(allat=allat)
    kapcsolat = Kapcsolat.objects.get(id=1)

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


    return render(request, 'allat.html', {'allat': allat, 'allatpictures': allatpictures,'bplist': bplist, 'page_obj': page_obj, 'kapcsolat': kapcsolat})

def formorokbe(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "vackolo.hu - érdeklődés"
            body = {
                'név': form.cleaned_data['name'],
                'email cím': form.cleaned_data['email_address'],
                'üzenet': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message,  body['cím'], [body['üzenet']])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("sikeresmail.html")

    form = OrokbeFogadasForm()
    allatid = request.GET.get('allatid')
    allat = Allat.objects.get(id=allatid)
    kapcsolat = Kapcsolat.objects.get(id=1)

    return render(request, "formorokbe.html", {'form': form, 'allat': allat, 'kapcsolat': kapcsolat})    


def tamogatas(request):
    tamogatas = Tamogatas.objects.get(id=1)
    onkentesmunka = OnkentesMunka.objects.get(id=1)
    kapcsolat = Kapcsolat.objects.get(id=1)
    
    return render(request, 'tamogatas.html', {'tamogatas': tamogatas, 'onkentesmunka': onkentesmunka, 'kapcsolat': kapcsolat})

class KapcsolatIv(FormView):
    template_name = "kapcsolat.html"
    form_class = ContactForm
    success_url = "sikeresmail"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super().form_valid(form)
    
    def get_context_data(self,*args, **kwargs):
        context = super(KapcsolatIv, self).get_context_data(*args,**kwargs)
        context['kapcsolat'] = Kapcsolat.objects.get(id=1)
        return context
    
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def sikeresmail(request):
    return render(request, 'sikeresmail.html', {'title': 'sikeres email küldés'})