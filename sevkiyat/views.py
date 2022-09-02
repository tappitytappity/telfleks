from django.shortcuts import render, redirect
from database.models import *
from uretim.views import createheader
from database.views import formatxlsexport
from django.apps import apps
from datetime import datetime
from django.forms.models import model_to_dict
from django.conf import settings
from django.contrib import messages
import xlwt, xlrd

ANA_KLASOR = str(settings.BASE_DIR) + '\\xls\\'
AYLAR      = {'01':'Ocak', '02':'Şubat', '03':'Mart', '04':'Nisan', '05':'Mayıs', '06':'Haziran', '07':'Temmuz', '08':'Ağustos', '09':'Eylül', '10':'Ekim', '11':'Kasım', '12':'Aralık',}


def week_header(dayoftheweek):
    week        = str(dayoftheweek.isocalendar()[1]) + ". Hafta"
    monday      = datetime.fromordinal(dayoftheweek.toordinal()-dayoftheweek.weekday())
    friday      = datetime.fromordinal(dayoftheweek.toordinal()-dayoftheweek.weekday()+4)

    return week + " (" + monday.strftime("%d") + " " + AYLAR[monday.strftime("%m")] + " - " + friday.strftime("%d") + " " + AYLAR[friday.strftime("%m")] + ")"

def sevkiyat(request):
    this_week   = week_header(datetime.today())
    siparisler  = Siparis.objects.filter(sevkiyat_secim=True)
    firmalar    = siparisler.order_by('siparis_musteri__cari_unvani').distinct('siparis_musteri__cari_unvani')

    return render(request,'sevkiyat/sevkiyat.html',{
        'this_week':this_week,
        'siparisler':siparisler,
        'firmalar':firmalar,
        })

def sevkiyat_yazdir(request):
    this_week   = week_header(datetime.today())
    siparisler  = Siparis.objects.filter(sevkiyat_secim=True)
    firmalar    = siparisler.order_by('siparis_musteri__cari_unvani').distinct('siparis_musteri__cari_unvani')

    try:
        sevkiyat_xls_export(siparisler,firmalar)
    except:
        messages.success(request,("Sevkiyat dosyası yazdırılamadı. Başkası tarafından kullanılmadığından emin olun"))


    return redirect('/sevkiyat/sevkiyat',{
        'this_week':this_week,
        'siparisler':siparisler,
        'firmalar':firmalar,
        })

def sevkiyat_secimleri_kaldir(request):
    for obj in [obj for obj in Siparis.objects.filter(siparis_teslimtar__lt = datetime.fromordinal(datetime.today().toordinal()+32)) if obj.eksikhesapla>=0]:
        obj.sevkiyat_secim=False
        obj.save()

    this_week   = week_header(datetime.today())
    siparisler  = [obj for obj in Siparis.objects.filter(siparis_teslimtar__lt = datetime.fromordinal(datetime.today().toordinal()+32)) if obj.eksikhesapla>=0]
    firmalar    = set([firma.siparis_musteri for firma in siparisler])

    return redirect('/sevkiyat/sevkiyat_planla',{
        'this_week':this_week,
        'siparisler':siparisler,
        'firmalar':firmalar,
        })

def otomatik_sec(request):
    for obj in [obj for obj in Siparis.objects.filter(siparis_teslimtar__lt = datetime.fromordinal(datetime.today().toordinal()+32)) if obj.eksikhesapla>=0]:
        if obj.siparis_teslimtar.isocalendar()[1]==datetime.today().isocalendar()[1]:
            obj.sevkiyat_secim=True
        else:
            obj.sevkiyat_secim=False
        obj.save()

    this_week   = week_header(datetime.today())
    siparisler  = [obj for obj in Siparis.objects.filter(siparis_teslimtar__lt = datetime.fromordinal(datetime.today().toordinal()+32)) if obj.eksikhesapla>=0]
    firmalar    = set([firma.siparis_musteri for firma in siparisler])


    return redirect('/sevkiyat/sevkiyat_planla',{
        'this_week':this_week,
        'siparisler':siparisler,
        'firmalar':firmalar,
        })

# Yapilacak Sevkiyatlari Sec
def sevkiyat_planla(request):
    this_week   = week_header(datetime.today())

    if request.method == "POST":
        id_list = request.POST.getlist('boxes')
        Siparis.objects.all().update(sevkiyat_secim=False)
        for siparis_id in id_list:
            Siparis.objects.filter(pk=int(siparis_id)).update(sevkiyat_secim=True)

        siparisler  = Siparis.objects.filter(sevkiyat_secim=True)
        firmalar    = siparisler.order_by('siparis_musteri__cari_unvani').distinct('siparis_musteri__cari_unvani')

        return redirect('/sevkiyat/sevkiyat',{
            'this_week':this_week,
            'siparisler':siparisler,
            'firmalar':firmalar,
            })

    siparisler  = [obj for obj in Siparis.objects.filter(siparis_teslimtar__lt = datetime.fromordinal(datetime.today().toordinal()+32)) if obj.eksikhesapla>=0]
    firmalar    = set([firma.siparis_musteri for firma in siparisler])

    return render(request,'sevkiyat/sevkiyat_planla.html',{
        'this_week':this_week,
        'siparisler':siparisler,
        'firmalar':firmalar,
        })

def sevkiyat_xls_export(siparisler,firmalar):

    fieldnames = siparisler[0].fieldnames()
    headers = siparisler[0].headers()
    xls_file_name = ANA_KLASOR + '\\export\\sevkiyat.xls'
    wb = xlwt.Workbook()
    sheetno = 1

    for firma in firmalar:
        worksheet = wb.add_sheet(str(sheetno))
        rowno = 1
        colno = 1
        worksheet.write(0, 0, 'Firma')
        worksheet.write(0, 1, 'Sipariş No')
        worksheet.write(0, 2, 'Belge No')
        worksheet.write(0, 3, 'Stok Kodu')
        worksheet.write(0, 4, 'Miktar')

        for row in siparisler:
            if row.siparis_musteri.id==firma.siparis_musteri.id:
                worksheet.write(rowno, 0, row.siparis_musteri.cari_unvani)
                worksheet.write(rowno, 1, formatxlsexport(getattr(row,'siparis_no'),'siparis_no'))
                worksheet.write(rowno, 2, formatxlsexport(getattr(row,'siparis_belgeno'),'siparis_belgeno'))
                worksheet.write(rowno, 3, formatxlsexport(getattr(row,'siparis_stok'),'siparis_stok'))
                worksheet.write(rowno, 4, formatxlsexport(getattr(row,'siparis_kalanmiktar'),'siparis_kalanmiktar'))
                rowno += 1
        sheetno += 1

    wb.save(xls_file_name)
