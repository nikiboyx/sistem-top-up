from django.db import models
import os
import uuid
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

def upload_nama_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{slugify(instance.nama)}-{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('produk/', filename)

class Produk(models.Model):
    nama = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    deskripsi = models.TextField(blank=True)
    gambar = models.ImageField(upload_to=upload_nama_file, blank=True, null=True)

    def __str__(self):
        return f"{self.nama} - Rp{self.harga}"

class Pesanan(models.Model):
    METODE_PEMBAYARAN = [
        ('dana', 'DANA'),
        ('ovo', 'OVO'),
        ('gopay', 'GoPay'),
        ('shopeepay', 'ShopeePay'),
    ]

    STATUS_PESANAN = [
        ('pending', 'Menunggu Pembayaran'),
        ('diproses', 'Diproses'),
        ('selesai', 'Selesai'),
        ('gagal', 'Gagal'),
    ]

    kode_unik = models.CharField(max_length=12, unique=True, blank=True)
    nama_pemesan = models.CharField(max_length=100)
    nomor_tujuan = models.CharField(max_length=20)
    alamat = models.TextField(default= "")
    jumlah = models.PositiveIntegerField(default=1)
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE)
    metode_pembayaran = models.CharField(max_length=20, choices=METODE_PEMBAYARAN)
    status = models.CharField(max_length=20, choices=STATUS_PESANAN, default='pending')
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama_pemesan} - {self.kode_unik}"

    def save(self, *args, **kwargs):
        if not self.kode_unik:
            self.kode_unik = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

@receiver(pre_save, sender=Produk)
def hapus_gambar_lama(sender, instance, **kwargs):
    try:
        produk_lama = Produk.objects.get(pk=instance.pk)
        if produk_lama.gambar and produk_lama.gambar != instance.gambar:
            if os.path.isfile(produk_lama.gambar.path):
                os.remove(produk_lama.gambar.path)
    except Produk.DoesNotExist:
        pass

@receiver(post_delete, sender=Produk)
def hapus_gambar_setelah_hapus(sender, instance, **kwargs):
    if instance.gambar and os.path.isfile(instance.gambar.path):
        os.remove(instance.gambar.path)