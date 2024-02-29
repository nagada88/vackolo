from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import FormView
from app_vackolo.forms import ContactForm, OrokbeFogadasForm
from .models import *
from .filters import AllatFilter
import datetime
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse


  
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
    allatid = request.GET.get('allatid')
    allat = Allat.objects.get(id=allatid)
    allatnev = allat.nev
    kapcsolat = Kapcsolat.objects.get(id=1)

    if request.method == 'POST':
        form = OrokbeFogadasForm(request.POST)
        if form.is_valid():
            subject = "vackolo.hu - érdeklődés"
            body = {
                'név': 'Feladó: ' + form.cleaned_data['name'],
                'email cím': form.cleaned_data['email_address'],
                'aki iránt érdeklődöm:': '\nAki iránt érdeklődöm: ' + allatnev,
                'üzenet': form.cleaned_data['message'],
            }
            message = "Üzenet érkezett az örökbefogadási űrlapon keresztül: \n\n" + "\n".join(body.values())

            try:
                send_mail(subject, message,  body['email cím'], ["nagada88@gmail.com"])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("sikeresmail.html")

    form = OrokbeFogadasForm()

    return render(request, "formorokbe.html", {'form': form, 'allat': allat, 'kapcsolat': kapcsolat})    


def tamogatas(request):
    tamogatas = Tamogatas.objects.get(id=1)
    onkentesmunka = OnkentesMunka.objects.get(id=1)
    kapcsolat = Kapcsolat.objects.get(id=1)
    
    return render(request, 'tamogatas.html', {'tamogatas': tamogatas, 'onkentesmunka': onkentesmunka, 'kapcsolat': kapcsolat})

def kapcsolativ(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "vackolo.hu - érdeklődés"
            body = {
                'név': 'Feladó: ' + form.cleaned_data['name'],
                'email cím': form.cleaned_data['email_address'],
                'üzenet': form.cleaned_data['message'],
            }
            message = "Üzenet érkezett az örökbefogadási űrlapon keresztül: \n\n" + "\n".join(body.values())

            try:
                send_mail(subject, message,  body['email cím'], ["nagada88@gmail.com"])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("sikeresmail.html")

    form = ContactForm()

    return render(request, "kapcsolat.html", {'form': form})
    
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def sikeresmail(request):
    return render(request, 'sikeresmail.html', {'title': 'sikeres email küldés'})