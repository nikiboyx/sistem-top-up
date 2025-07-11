from django import forms
from .models import Pesanan, Produk

class PesananForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['nama_pemesan', 'nomor_tujuan', 'alamat', 'jumlah', 'metode_pembayaran']
        labels = {
            'nama_pemesan': 'Nama Lengkap',
            'nomor_tujuan': 'Nomor WhatsApp / HP',
            'alamat': 'Alamat Pengiriman / Keterangan',
            'jumlah': 'Jumlah Produk',
            'metode_pembayaran': 'Pilih E-Wallet',
        }
        widgets = {
            'alamat': forms.Textarea(attrs={
                'rows': 2,
                'class': 'bg-gray-800 text-white p-3 rounded w-full resize-none',
            }),
        }
        
# Edit status pesanan
class PesananStatusForm(forms.ModelForm):
    class Meta:
        model = Pesanan
        fields = ['status']

# Form Produk sederhana
class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        fields = ['nama', 'harga', 'deskripsi', 'gambar']