from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app_vackolo.forms import ContactForm, OrokbeFogadasForm
from .models import *
from .filters import AllatFilter
import datetime
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.core.mail import EmailMessage, BadHeaderError

def bemutatkozas(request):
    now=timezone.now()
    month = now.month
    bemutatkozas = Bemutatkozas.objects.all()
    kapcsolat = Kapcsolat.objects.get(id=1)
    allatszam = Allat.objects.all().count()
    orokbeadottszam = allatszam - Allat.objects.all().exclude(orokbeadva = True).count() + 3600
    orokbevar = Allat.objects.all().exclude(orokbeadva = True).count()
    today = datetime.date.today()
    ezota = today.year - 2006
    filtered_animal = Allat.objects.all().exclude(orokbeadva = True).order_by('?')[:4]
    first_day_of_the_current_month = timezone.now().month
    birthday_animal = Allat.objects.all().filter(szuletesiideje__month=month).exclude(orokbeadva = True)
    tamogatas = Tamogatas.objects.get(id=1)
    
    return render(request, 'bemutatkozas.html', {'bemutatkozas': bemutatkozas,'filtered_animal': filtered_animal, 'kapcsolat': kapcsolat, 'orokbevar': orokbevar, 'orokbeadottszam': orokbeadottszam, 'ezota': ezota, 'birthday_animal': birthday_animal, 'title': 'Vackoló Állatmenhely Veszprém és Környéke - Kutya, Cica', 'tamogatas': tamogatas})
    
    
def orokbefogadas(request):
    filtered_animal = AllatFilter(request.GET, queryset=Allat.objects.all().exclude(orokbeadva = True).order_by('nev'))
    paginator = Paginator(filtered_animal.qs, 8)
    kapcsolat = Kapcsolat.objects.get(id=1)

    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page('1')
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'orokbefogadas.html', {'page_obj': page_obj, 'filtered_animal': filtered_animal, 'kapcsolat': kapcsolat, 'title': 'Örökbefogadható kutyák és macskák, örökbefogadási feltételek'})

def allat(request):
    allatid = request.GET.get('allatid')
    allat = Allat.objects.get(id=allatid)
    allatpictures = AllatImage.objects.filter(allat=allat)
    kapcsolat = Kapcsolat.objects.get(id=1)
    orokbefogadasszoveg = OrokbefogadasSzoveg.objects.get(id=1)

    allatok = Allat.objects.exclude(pk = allatid).exclude(orokbeadva = True).order_by('-id')
    paginator = Paginator(allatok, 8)
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


    return render(request, 'allat.html', {'allat': allat, 'allatpictures': allatpictures,'bplist': bplist, 'page_obj': page_obj, 'kapcsolat': kapcsolat, 'orokbefogadasszoveg': orokbefogadasszoveg, 'title': 'Örökbefogadható kutya vagy macska - Vackoló'})

def formorokbe(request):
    allatid = request.GET.get('allatid')
    allat = Allat.objects.get(id=allatid)
    allatnev = allat.nev
    kapcsolat = Kapcsolat.objects.get(id=1)

    if request.method == 'POST':
        form = OrokbeFogadasForm(request.POST)
        if form.is_valid():
            body = {
                'név': 'Feladó: ' + form.cleaned_data['name'],
                'email cím': form.cleaned_data['email_address'],
                'aki iránt érdeklődöm:': '\nAki iránt érdeklődöm: ' + allatnev,
                'üzenet': form.cleaned_data['message'],
            }
            message = "Üzenet érkezett az örökbefogadási űrlapon keresztül: \n\n" + "\n".join(body.values())
            subject = "vackolo.hu - érdeklődés " + str(allatnev) + " iránt"

            try:
                email = EmailMessage(
                subject=subject, 
                body=message,
                from_email='brandbehozunk@gmail.com',
                to=[kapcsolat.emailcim],
                reply_to=[body['email cím']],
                          )
                email.send()    
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("sikeresmail.html")
        else:
            messages.error(request, form.errors)
    else:        
        form = OrokbeFogadasForm()

    return render(request, "formorokbe.html", {'form': form, 'allat': allat, 'kapcsolat': kapcsolat, 'title': 'Érdeklődés örökbefogadással kapcsolatban - kapcsolat'})    


def tamogatas(request):
    tamogatas = Tamogatas.objects.get(id=1)
    onkentesmunka = OnkentesMunka.objects.get(id=1)
    kapcsolat = Kapcsolat.objects.get(id=1)
    
    return render(request, 'tamogatas.html', {'tamogatas': tamogatas, 'onkentesmunka': onkentesmunka, 'kapcsolat': kapcsolat, 'title': 'Vackoló Állatmenhely támogatás, önkéntes munka, adományozás'})

def kapcsolativ(request):
    kapcsolat = Kapcsolat.objects.get(id=1)
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
                email = EmailMessage(
                            subject=subject, 
                            body=message,
                            from_email='brandbehozunk@gmail.com',
                            to=[kapcsolat.emailcim],
                            reply_to=[body['email cím']],
                          )
                email.send()    
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("sikeresmail.html")
        else:
            messages.error(request, form.errors)
    else:
        form = ContactForm()

    return render(request, "kapcsolat.html", {'form': form, 'title': 'Vackoló Állatmenhely Veszprém, kapcsolatfelvétel', 'kapcsolat': kapcsolat })
    
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def sikeresmail(request):
    kapcsolat = Kapcsolat.objects.get(id=1)
    return render(request, 'sikeresmail.html', {'title': 'sikeres email küldés', 'kapcsolat': kapcsolat})