from django.urls import path
from . import views

urlpatterns = [
    path('sevkiyat', views.sevkiyat, name='sevkiyat'),
    path('sevkiyat_yazdir',views.sevkiyat_yazdir,name='sevkiyat_yazdir'),
    path('sevkiyat_planla',views.sevkiyat_planla,name='sevkiyat_planla'),
    path('otomatik_sec',views.otomatik_sec,name='otomatik_sec'),
    path('sevkiyat_secimleri_kaldir',views.sevkiyat_secimleri_kaldir,name='sevkiyat_secimleri_kaldir')
]
