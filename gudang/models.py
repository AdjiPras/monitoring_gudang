from django.db import models

class Barang(models.Model):
    nama = models.CharField(max_length=100)
    jumlah = models.IntegerField()
    lokasi = models.CharField(max_length=50)
    tanggal_masuk = models.DateField()
    pemasok = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nama



class Pemasok(models.Model):
    nama = models.CharField(max_length=100)
    kontak = models.CharField(max_length=100)
    alamat = models.TextField()
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.nama