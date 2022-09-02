from django.shortcuts import render
from database.models import *
from database.views import xlsguncelle
from django.apps import apps
from datetime import datetime

def createheader(week_flag):
    # This week
    week = datetime.today().isocalendar()[1]
    mon  = datetime.today().toordinal()-datetime.today().weekday()
    ay   = {'01':'Ocak', '02':'Şubat', '03':'Mart', '04':'Nisan', '05':'Mayıs', '06':'Haziran', '07':'Temmuz', '08':'Ağustos', '09':'Eylül', '10':'Ekim', '11':'Kasım', '12':'Aralık',}

    this_week = str(week) + ". Hafta (" + datetime.fromordinal(mon).strftime("%d") + " " + ay[datetime.fromordinal(mon).strftime("%m")] + " - " + datetime.fromordinal(mon+4).strftime("%d") + " " + ay[datetime.fromordinal(mon+4).strftime("%m")] + ")"
    next_week = str(week+1) + ". Hafta (" + datetime.fromordinal(mon+7).strftime("%d") + " " + ay[datetime.fromordinal(mon+7).strftime("%m")] + " - " + datetime.fromordinal(mon+7+4).strftime("%d") + " " + ay[datetime.fromordinal(mon+7+4).strftime("%m")] + ")"

    if week_flag == "this_week":
        return this_week
    else:
        return next_week

# Create your views here.
def uretim(request):
    week = datetime.today().isocalendar()[1]
    this_week = createheader('this_week')
    next_week = createheader('next_week')
    return render(request,'uretim/uretim.html',{'this_week':this_week, 'next_week':next_week,})

def eksikler_hesapla(request):
    xlsguncelle('Siparis','guncelle')
    return render(request,'uretim/uretim.html',{})
