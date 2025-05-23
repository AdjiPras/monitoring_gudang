from django import forms
from .models import Barang
from .models import Pemasok

class BarangForm(forms.ModelForm):
    class Meta:
        model = Barang
        fields = '__all__'  # semua field termasuk pemasok
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Laptop'}),
            'jumlah': forms.NumberInput(attrs={'class': 'form-control'}),
            'lokasi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Gudang A'}),
            'tanggal_masuk': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pemasok': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama pemasok'}),
        }

class PemasokForm(forms.ModelForm):
    class Meta:
        model = Pemasok
        fields = ['nama', 'kontak', 'alamat', 'email']
        widgets = {
            'alamat': forms.Textarea(attrs={'rows': 3}),
        }