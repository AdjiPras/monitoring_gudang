from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_barang, name='list_barang'),
    path('tambah/', views.tambah_barang, name='tambah_barang'),
    path('edit/<int:pk>/', views.edit_barang, name='edit_barang'),
    path('hapus/<int:pk>/', views.hapus_barang, name='hapus_barang'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('pemasok/', views.list_pemasok, name='list_pemasok'),
    path('pemasok/tambah/', views.tambah_pemasok, name='tambah_pemasok'),
    path('pemasok/edit/<int:pk>/', views.edit_pemasok, name='edit_pemasok'),
    path('pemasok/hapus/<int:pk>/', views.hapus_pemasok, name='hapus_pemasok'),
]
