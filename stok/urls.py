from django.urls import path
from . import views

urlpatterns = [
    path('stok', views.stok, name='stok'),
    path('stok/<stokkodu>', views.stok, name='stok'),
    path('stok_ara', views.stok_ara, name='stok_ara'),
]
