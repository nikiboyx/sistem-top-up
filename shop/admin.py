from django.contrib import admin
from .models import Produk, Pesanan

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    list_display = ['nama', 'harga', 'deskripsi']
    search_fields = ['nama']
    list_per_page = 10

@admin.register(Pesanan)
class PesananAdmin(admin.ModelAdmin):
    list_display = ['kode_unik', 'nama_pemesan', 'produk', 'nomor_tujuan', 'status', 'metode_pembayaran', 'tanggal']
    list_filter = ['status', 'metode_pembayaran', 'tanggal']
    search_fields = ['kode_unik', 'nama_pemesan', 'nomor_tujuan']
    fields = ('kode_unik', 'nama_pemesan', 'nomor_tujuan', 'produk', 'metode_pembayaran', 'status', 'tanggal')
    readonly_fields = ('kode_unik', 'tanggal', 'nama_pemesan', 'nomor_tujuan', 'produk', 'metode_pembayaran')
    ordering = ('-tanggal',)
    list_per_page = 15

