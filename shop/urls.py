from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_produk, name='daftar_produk'),
    path('produk/<int:pk>/', views.produk_detail, name='produk_detail'),
    path('produk/<int:produk_id>/pesan/', views.buat_pesanan, name='buat_pesanan'),

    path('lacak/', views.lacak_pesanan, name='lacak_pesanan'),
    path('pesanan/<int:pk>/struk/', views.struk_pembayaran, name='struk_pembayaran'),
    path('pesanan/<int:pk>/konfirmasi/', views.konfirmasi_pembayaran, name='konfirmasi_pembayaran'),

    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/produk/tambah/', views.admin_tambah_produk, name='admin_tambah_produk'),
    path('admin-panel/produk/edit/<int:pk>/', views.admin_edit_produk, name='admin_edit_produk'),
    path('admin-panel/produk/hapus/<int:pk>/', views.admin_hapus_produk, name='admin_hapus_produk'),
    path('admin-panel/pesanan/edit/<int:pk>/', views.admin_edit_pesanan, name='admin_edit_pesanan'),
]
