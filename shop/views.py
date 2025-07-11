from django.shortcuts import render, get_object_or_404, redirect
from .models import Produk, Pesanan
from .forms import PesananForm, PesananStatusForm, ProdukForm
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_panel')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_panel')
    else:
        form = AuthenticationForm()

    return render(request, 'admin/admin_login.html', {'form': form})

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def daftar_produk(request):
    query = request.GET.get("q")
    if query:
        produk_list = Produk.objects.filter(
            Q(nama__icontains=query) | Q(deskripsi__icontains=query)
        )
    else:
        produk_list = Produk.objects.all()

    return render(request, 'shop/daftar_produk.html', {
        'produk_list': produk_list,
        'query': query
    })

def produk_detail(request, pk):
    produk = get_object_or_404(Produk, pk=pk)

    if request.method == 'POST':
        form = PesananForm(request.POST)
        if form.is_valid():
            pesanan = form.save(commit=False)
            pesanan.produk = produk
            pesanan.save()
            return redirect('struk_pembayaran', pesanan.pk)
    else:
        form = PesananForm()

    return render(request, 'shop/produk_detail.html', {
        'produk': produk,
        'form': form
    })

def buat_pesanan(request, produk_id):
    produk = get_object_or_404(Produk, pk=produk_id)
    if request.method == 'POST':
        form = PesananForm(request.POST)
        if form.is_valid():
            pesanan = form.save(commit=False)
            pesanan.produk = produk
            pesanan.save()
            return redirect('struk_pembayaran', pesanan.pk)
    else:
        form = PesananForm()
    return render(request, 'shop/buat_pesanan.html', {'form': form, 'produk': produk})

def struk_pembayaran(request, pk):
    pesanan = get_object_or_404(Pesanan, pk=pk)
    total_harga = pesanan.jumlah * pesanan.produk.harga
    return render(request, 'shop/struk_pembayaran.html', {
        'pesanan': pesanan,
        'total_harga': total_harga,
    })

@csrf_exempt
def konfirmasi_pembayaran(request, pk):
    pesanan = get_object_or_404(Pesanan, pk=pk)
    # Status tetap 'pending' — nanti admin yang ubah ke 'diproses' atau 'selesai'
    return render(request, 'shop/sukses.html', {'pesanan': pesanan})

def lacak_pesanan(request):
    kode = request.GET.get('kode', '')
    pesanan = None
    if kode:
        pesanan = Pesanan.objects.filter(kode_unik=kode).first()
    return render(request, 'shop/lacak_pesanan.html', {'pesanan': pesanan, 'kode': kode})

# Panel Admin
# Halaman utama admin
@login_required(login_url='admin_login')
def admin_panel(request):
    query = request.GET.get('q')
    if query:
        pesanan_list = Pesanan.objects.filter(nama_pemesan__icontains=query)
    else:
        pesanan_list = Pesanan.objects.all()

    produk_list = Produk.objects.all()
    return render(request, 'admin/admin_panel.html', {
        'produk_list': produk_list,
        'pesanan_list': pesanan_list
    })

# CRUD Produk
@login_required(login_url='admin_login')
def admin_tambah_produk(request):
    if request.method == 'POST':
        form = ProdukForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = ProdukForm()
    return render(request, 'admin/admin_produk_form.html', {'form': form, 'title': 'Tambah Produk'})

@login_required(login_url='admin_login')
def admin_edit_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    if request.method == 'POST':
        form = ProdukForm(request.POST, request.FILES, instance=produk)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = ProdukForm(instance=produk)
    return render(request, 'admin/admin_produk_form.html', {'form': form, 'title': 'Edit Produk'})

@login_required(login_url='admin_login')
def admin_hapus_produk(request, pk):
    produk = get_object_or_404(Produk, pk=pk)
    produk.delete()
    return redirect('admin_panel')

@login_required(login_url='admin_login')
def admin_edit_pesanan(request, pk):
    pesanan = get_object_or_404(Pesanan, pk=pk)
    if request.method == 'POST':
        form = PesananStatusForm(request.POST, instance=pesanan)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = PesananStatusForm(instance=pesanan)
    return render(request, 'admin/admin_pesanan_form.html', {'form': form, 'pesanan': pesanan})

