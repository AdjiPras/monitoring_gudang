from django.shortcuts import render, redirect, get_object_or_404
from .models import Barang
from .forms import BarangForm

from .models import Pemasok
from .forms import PemasokForm

from django.core.paginator import Paginator
# from django.db.models import Q
from django.db.models import Sum, Count

from django.db.models.functions import TruncMonth



def dashboard(request):
    # Data awal
    total_jumlah_barang = Barang.objects.aggregate(total=Sum('jumlah'))['total'] or 0
    total_data_barang = Barang.objects.aggregate(count=Count('id'))['count'] or 0
    total_data_pemasok = Pemasok.objects.aggregate(count=Count('id'))['count'] or 0

    data_lokasi = Barang.objects.values('lokasi').annotate(total_jumlah=Sum('jumlah')).order_by('-total_jumlah')
    labels = [d['lokasi'] for d in data_lokasi]
    data = [d['total_jumlah'] for d in data_lokasi]

    # Data distribusi barang per bulan (berdasarkan tanggal_masuk)
    data_bulan = (
        Barang.objects
        .annotate(bulan=TruncMonth('tanggal_masuk'))
        .values('bulan')
        .annotate(total_jumlah=Sum('jumlah'))
        .order_by('bulan')
    )
    labels_bulan = [d['bulan'].strftime('%b %Y') for d in data_bulan]  # contoh: 'May 2025'
    data_bulan_jml = [d['total_jumlah'] for d in data_bulan]

    context = {
        'total_jumlah_barang': total_jumlah_barang,
        'total_data_barang': total_data_barang,
        'total_data_pemasok': total_data_pemasok,
        'labels': labels,
        'data': data,
        'labels_bulan': labels_bulan,
        'data_bulan': data_bulan_jml,
    }
    return render(request, 'gudang/dashboard.html', context)

# ================= BARANG =================
def list_barang(request):
    search_query = request.GET.get('search', '')
    lokasi_filter = request.GET.get('lokasi', '')
    sort_by = request.GET.get('sort', 'nama')
    order = request.GET.get('order', 'asc')

    if order == 'desc':
        sort_param = '-' + sort_by
    else:
        sort_param = sort_by

    barangs = Barang.objects.all()

    if search_query:
        barangs = barangs.filter(nama__icontains=search_query)

    if lokasi_filter:
        barangs = barangs.filter(lokasi=lokasi_filter)

    barangs = barangs.order_by(sort_param)

    paginator = Paginator(barangs, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    lokasi_list = Barang.objects.values_list('lokasi', flat=True).distinct()

    kolom = [
        ('nama', 'Nama Barang'),
        ('jumlah', 'Jumlah'),
        ('lokasi', 'Lokasi'),
        ('tanggal_masuk', 'Tanggal Masuk'),
        ('pemasok', 'Pemasok'),
    ]

    return render(request, 'gudang/list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'lokasi_filter': lokasi_filter,
        'sort_by': sort_by,
        'order': order,
        'lokasi_list': lokasi_list,
        'kolom': kolom,
    })

def tambah_barang(request):
    form = BarangForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('list_barang')
    return render(request, 'gudang/form.html', {'form': form})

def edit_barang(request, pk):
    barang = get_object_or_404(Barang, pk=pk)
    form = BarangForm(request.POST or None, instance=barang)
    if form.is_valid():
        form.save()
        return redirect('list_barang')
    return render(request, 'gudang/form.html', {'form': form})

def hapus_barang(request, pk):
    barang = get_object_or_404(Barang, pk=pk)
    if request.method == 'POST':
        barang.delete()
        return redirect('list_barang')
    return render(request, 'gudang/hapus_confirm.html', {'barang': barang})


# ================= PEMASOK =================
def list_pemasok(request):
    search_nama = request.GET.get('search_nama', '')
    search_alamat = request.GET.get('search_alamat', '')
    sort_by = request.GET.get('sort', 'nama')
    order = request.GET.get('order', 'asc')

    qs = Pemasok.objects.all()

    if search_nama:
        qs = qs.filter(nama__icontains=search_nama)

    if search_alamat:
        qs = qs.filter(alamat__icontains=search_alamat)

    # validasi kolom sort yang diizinkan
    allowed_sort_fields = ['nama', 'kontak', 'alamat', 'email']
    if sort_by not in allowed_sort_fields:
        sort_by = 'nama'

    order_prefix = '' if order == 'asc' else '-'
    qs = qs.order_by(f"{order_prefix}{sort_by}")

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    kolom = [
        ('nama', 'Nama'),
        ('kontak', 'Kontak'),
        ('alamat', 'Alamat'),
        ('email', 'Email'),
    ]

    context = {
        'page_obj': page_obj,
        'search_nama': search_nama,
        'search_alamat': search_alamat,
        'sort_by': sort_by,
        'order': order,
        'kolom': kolom,
    }
    return render(request, 'gudang/pemasok_list.html', context)

def tambah_pemasok(request):
    if request.method == 'POST':
        form = PemasokForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_pemasok')
    else:
        form = PemasokForm()
    return render(request, 'gudang/pemasok_form.html', {'form': form})

def edit_pemasok(request, pk):
    pemasok = get_object_or_404(Pemasok, pk=pk)
    if request.method == 'POST':
        form = PemasokForm(request.POST, instance=pemasok)
        if form.is_valid():
            form.save()
            return redirect('list_pemasok')
    else:
        form = PemasokForm(instance=pemasok)
    return render(request, 'gudang/pemasok_form.html', {'form': form})

def hapus_pemasok(request, pk):
    pemasok = get_object_or_404(Pemasok, pk=pk)
    if request.method == 'POST':
        pemasok.delete()
        return redirect('list_pemasok')
    return render(request, 'gudang/hapus_confirm.html', {'obj': pemasok, 'url_kembali': 'list_pemasok'})
