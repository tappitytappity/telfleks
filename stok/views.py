from django.shortcuts import render
from database.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
from django.conf import settings
import os
import datetime

# Create your views here.
def stok(request, stokkodu=[]):
    if stokkodu:
        # Set up Pagination
        s = Stok.objects.filter(stok_kodu__contains=stokkodu.upper().rstrip()).order_by('stok_kodu')
    else:
        s = Stok.objects.all().order_by('stok_kodu')

    p = Paginator(s,1)
    page = request.GET.get('page')
    stoklar = p.get_page(page)

    if page is None:
        stok = s[0]
    else:
        stok = s[int(page)-1]

    children = UrunAgaci.objects.filter(ana_kodu=stok)
    parents = UrunAgaci.objects.filter(tuketim_kodu=stok)
    hareketler = StokHareketleri.objects.filter(hareket_stok_kodu=stok).order_by('-hareket_tarih')
    siparisler = Siparis.objects.filter(siparis_stok = stok).order_by('-siparis_teslimtar')
    raporlar = Raporlar.objects.filter(rapor_stok_kodu = stok)

    return render(request, "stok/stok.html",{
        'stoklar':stoklar,
        'KLASORLER':KLASORLER,
        'parents':parents,
        'children':children,
        'hareketler':hareketler,
        'siparisler':siparisler,
        'raporlar':raporlar,
    })

def stok_ara(request):
    if request.method == "POST":
        stokkodu = request.POST['aranan']
        return HttpResponseRedirect('stok' + "/" + stokkodu)
    else:
        return render(request, "stok/stok.html",{})

    #return render(request, "urunler/urun_ara.html",
    #    {'stoklar':stoklar,})
