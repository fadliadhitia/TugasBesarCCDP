from datetime import datetime, timedelta

# Pola Singleton
class ManajerPerpustakaan:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ManajerPerpustakaan, cls).__new__(cls)
            cls._instance.buku = []
            cls._instance.anggota = []
        return cls._instance

    def tambahBuku(self, buku):
        self.buku.append(buku)
    
    def hapusBuku(self, buku):
        self.buku.remove(buku)
    
    def daftarkanAnggota(self, anggota):
        self.anggota.append(anggota)
    
    def hapusAnggota(self, anggota):
        self.anggota.remove(anggota)
    
    def pinjamBuku(self, buku, anggota):
        if buku in self.buku and buku.tersedia:
            pinjaman = Pinjaman(buku, anggota, datetime.now(), datetime.now() + timedelta(days=14))
            buku.tersedia = False
            return pinjaman
        else:
            return None
    
    def kembalikanBuku(self, buku, anggota):
        if buku in self.buku:
            buku.tersedia = True
    
    def cariBukuDenganJudul(self, judul):
        for buku in self.buku:
            if buku.judul == judul:
                return buku
        return None

# Pola Factory Method
class Buku:
    def __init__(self, judul, penulis, isbn):
        self.judul = judul
        self.penulis = penulis
        self.isbn = isbn
        self.tersedia = True
        self.state = StateTersedia()

    def pinjam(self):
        self.state.pinjam(self)

    def kembalikan(self):
        self.state.kembalikan(self)

class PabrikBuku:
    def buatBuku(self, judul, penulis, isbn):
        return Buku(judul, penulis, isbn)

# Pola Adapter
class SistemPencarianLama:
    def pencarianLama(self, kataKunci):
        return f"Hasil pencarian lama untuk: {kataKunci}"

class AdapterSistemPencarianLama:
    def __init__(self, sistemPencarianLama):
        self.sistemPencarianLama = sistemPencarianLama

    def cari(self, kataKunci):
        return self.sistemPencarianLama.pencarianLama(kataKunci)

# Pola Decorator
class DekoratorBuku:
    def __init__(self, buku):
        self._buku = buku

    def getJudul(self):
        return self._buku.judul

class DekoratorBukuDenganLabel(DekoratorBuku):
    def __init__(self, buku, label):
        super().__init__(buku)
        self._label = label

    def getJudul(self):
        return f"{self._buku.judul} - {self._label}"

# Pola Observer
class Pengamat:
    def update(self, buku):
        pass

class PemberiNotifikasiKetersediaanBuku:
    def __init__(self):
        self._pengamat = []

    def tambahPengamat(self, pengamat):
        self._pengamat.append(pengamat)

    def hapusPengamat(self, pengamat):
        self._pengamat.remove(pengamat)

    def beriNotifikasi(self, buku):
        for pengamat in self._pengamat:
            pengamat.update(buku)

class Anggota(Pengamat):
    def __init__(self, nama, idAnggota):
        self.nama = nama
        self.idAnggota = idAnggota

    def update(self, buku):
        print(f"{self.nama}, buku {buku.judul} sekarang tersedia!")

# Pola Strategy
class StrategiPencarian:
    def cari(self, kataKunci):
        pass

class StrategiPencarianJudul(StrategiPencarian):
    def cari(self, kataKunci):
        return f"Mencari buku berdasarkan judul: {kataKunci}"

class StrategiPencarianPenulis(StrategiPencarian):
    def cari(self, kataKunci):
        return f"Mencari buku berdasarkan penulis: {kataKunci}"

class PencariBuku:
    def __init__(self, strategi):
        self._strategi = strategi

    def setStrategi(self, strategi):
        self._strategi = strategi

    def cari(self, kataKunci):
        return self._strategi.cari(kataKunci)

# Pola Command
class Perintah:
    def eksekusi(self):
        pass

class PerintahPinjamBuku(Perintah):
    def __init__(self, buku, anggota):
        self.buku = buku
        self.anggota = anggota

    def eksekusi(self):
        manajer_perpustakaan = ManajerPerpustakaan()
        return manajer_perpustakaan.pinjamBuku(self.buku, self.anggota)

class PerintahKembalikanBuku(Perintah):
    def __init__(self, buku, anggota):
        self.buku = buku
        self.anggota = anggota

    def eksekusi(self):
        manajer_perpustakaan = ManajerPerpustakaan()
        manajer_perpustakaan.kembalikanBuku(self.buku, self.anggota)

# Pola Iterator
class IteratorBuku:
    def __init__(self, buku):
        self._buku = buku
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._buku):
            buku = self._buku[self._index]
            self._index += 1
            return buku
        else:
            raise StopIteration()

# Pola State
class StateBuku:
    def pinjam(self, buku):
        pass

    def kembalikan(self, buku):
        pass

class StateTersedia(StateBuku):
    def pinjam(self, buku):
        buku.state = StateTerpinjam()

class StateTerpinjam(StateBuku):
    def kembalikan(self, buku):
        buku.state = StateTersedia()

# Pola Chain of Responsibility
class Pinjaman:
    def __init__(self, buku, anggota, tanggalPinjam, tanggalJatuhTempo):
        self.buku = buku
        self.anggota = anggota
        self.tanggalPinjam = tanggalPinjam
        self.tanggalJatuhTempo = tanggalJatuhTempo
        self.tanggalKembali = None

class PenanganiPinjaman:
    def __init__(self, penerus=None):
        self.penerus = penerus

    def tanganiPermintaan(self, pinjaman):
        if self.penerus:
            self.penerus.tanganiPermintaan(pinjaman)

class PenanganDenda(PenanganiPinjaman):
    def tanganiPermintaan(self, pinjaman):
        if pinjaman.tanggalKembali and pinjaman.tanggalKembali > pinjaman.tanggalJatuhTempo:
            print("Denda diperlukan untuk buku yang terlambat.")
        super().tanganiPermintaan(pinjaman)

# Contoh Penggunaan
if __name__ == "__main__":
    # Inisialisasi manajer dan pabrik
    manajer_perpustakaan = ManajerPerpustakaan()
    pabrik_buku = PabrikBuku()
    
    # Buat buku dan anggota
    buku1 = pabrik_buku.buatBuku("1984", "George Orwell", "123456789")
    anggota1 = Anggota("Alice", "001")
    
    # Tambah buku dan daftarkan anggota
    manajer_perpustakaan.tambahBuku(buku1)
    manajer_perpustakaan.daftarkanAnggota(anggota1)
    
    # Contoh pola Command
    perintah_pinjam = PerintahPinjamBuku(buku1, anggota1)
    pinjaman = perintah_pinjam.eksekusi()
    print(f"Detail Pinjaman: {pinjaman.buku.judul} dipinjam oleh {pinjaman.anggota.nama}")
    
    perintah_kembalikan = PerintahKembalikanBuku(buku1, anggota1)
    perintah_kembalikan.eksekusi()
    print(f"Buku dikembalikan: {buku1.judul} sekarang tersedia")
    
    # Contoh pola Decorator
    buku_terdecorasi = DekoratorBukuDenganLabel(buku1, "Keluaran Baru")
    print(buku_terdecorasi.getJudul())
    
    # Contoh pola Observer
    pemberi_notifikasi = PemberiNotifikasiKetersediaanBuku()
    pemberi_notifikasi.tambahPengamat(anggota1)
    buku1.pinjam()
    pemberi_notifikasi.beriNotifikasi(buku1)
    
    # Contoh pola Strategy
    strategi_judul = StrategiPencarianJudul()
    pencari_buku = PencariBuku(strategi_judul)
    print(pencari_buku.cari("1984"))
    
    # Contoh pola Iterator
    buku = [buku1]
    iterator = IteratorBuku(buku)
    for buku in iterator:
        print(f"Iterasi buku: {buku.judul}")
    
    # Contoh pola State
    buku1.pinjam()
    print(f"Status buku setelah dipinjam: {buku1.state.__class__.__name__}")
    buku1.kembalikan()
    print(f"Status buku setelah dikembalikan: {buku1.state.__class__.__name__}")
    
    # Contoh pola Chain of Responsibility
    penangan_denda = PenanganDenda()
    pinjaman_terlambat = Pinjaman(buku1, anggota1, datetime.now() - timedelta(days=30), datetime.now() - timedelta(days=14))
    penangan_denda.tanganiPermintaan(pinjaman_terlambat)
