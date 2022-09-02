from django.urls import path
from . import views

urlpatterns = [
    path('uretim', views.uretim, name='uretim'),
    path('uretim/hesapla',views.eksikler_hesapla,name='eksikler_hesapla')
]
