from . import berkas, validasi
from .validasi import DataTidakValidError
 
 
def format_rupiah(angka):
    #Mengubah 15000 menjadi 'Rp 15.000'.
    return "Rp " + f"{angka:,}".replace(",", ".")
 
class Pengeluaran:
    # Field wajib; selain ini dianggap atribut tambahan
    FIELD_WAJIB = ("tanggal", "kategori", "keterangan", "jumlah")
 
    def __init__(self, **atribut):
        for nama in self.FIELD_WAJIB:
            if nama not in atribut:
                raise DataTidakValidError(f"Field wajib '{nama}' tidak ada.")
        self.tanggal = validasi.validasi_tanggal(atribut["tanggal"])
        self.kategori = validasi.validasi_tidak_kosong(atribut["kategori"], "kategori").lower()
        self.keterangan = validasi.validasi_tidak_kosong(atribut["keterangan"], "keterangan")
        self.jumlah = validasi.validasi_jumlah(atribut["jumlah"])
        # Semua atribut di luar field wajib disimpan di dictionary 'tambahan'
        self.tambahan = {k: v for k, v in atribut.items() if k not in self.FIELD_WAJIB}
 
    def ke_baris(self):
        bagian = [self.tanggal, self.kategori, self.keterangan, str(self.jumlah)]
        if "metode_bayar" in self.tambahan:
            bagian.append(self.tambahan["metode_bayar"])
        return " | ".join(bagian)
 
    def ringkasan(self):
        return (f"{self.tanggal} | {self.kategori:<10} | "
                f"{self.keterangan:<20} | {format_rupiah(self.jumlah)}")
 
 
class PengolahData:
    def __init__(self, daftar_pengeluaran):
        self.daftar = daftar_pengeluaran
 
    @staticmethod
    def jumlahkan(*angka):
        return sum(angka)
 
    def total(self):
        daftar_jumlah = list(map(lambda p: p.jumlah, self.daftar))
        return self.jumlahkan(*daftar_jumlah)
 
    def filter_kategori(self, kategori):
        return list(filter(lambda p: p.kategori == kategori.lower(), self.daftar))
 
    def total_per_kategori(self):
        hasil = {}
        for p in self.daftar:
            # .get(kategori, 0) -> bila kategori belum ada, mulai dari 0
            hasil[p.kategori] = hasil.get(p.kategori, 0) + p.jumlah
        return hasil
 
    def kategori_terboros(self):
        per_kategori = self.total_per_kategori()
        if not per_kategori:
            return None
        return max(per_kategori.items(), key=lambda pasangan: pasangan[1])
 
    def rata_rata_harian(self):
        if not self.daftar:
            return 0
        jumlah_hari = len(set(p.tanggal for p in self.daftar))
        # assert: memastikan pembagi tidak nol (kalau nol berarti ada bug)
        assert jumlah_hari > 0, "Jumlah hari tidak boleh nol"
        return self.total() // jumlah_hari
 
    def urutkan_terbesar(self, jumlah_teratas=3):
        terurut = sorted(self.daftar, key=lambda p: p.jumlah, reverse=True)
        return terurut[:jumlah_teratas]
 
    def buat_laporan(self):
        baris = ["=" * 50, "LAPORAN PENGELUARAN ANAK KOS", "=" * 50]
        baris.append(f"Jumlah catatan     : {len(self.daftar)}")
        baris.append(f"Total pengeluaran  : {format_rupiah(self.total())}")
        baris.append(f"Rata-rata per hari : {format_rupiah(self.rata_rata_harian())}")
 
        baris.append("\nTotal per kategori:")
        # Urutkan kategori dari yang terbesar
        for kategori, nilai in sorted(self.total_per_kategori().items(),
                                      key=lambda x: x[1], reverse=True):
            baris.append(f"  - {kategori:<12}: {format_rupiah(nilai)}")
 
        terboros = self.kategori_terboros()
        if terboros:
            baris.append(f"\nKategori terboros  : {terboros[0]} ({format_rupiah(terboros[1])})")
 
        baris.append("\n3 pengeluaran terbesar:")
        for p in self.urutkan_terbesar(jumlah_teratas=3):
            baris.append("  " + p.ringkasan())
        return "\n".join(baris) + "\n"
 

def muat_pengeluaran(nama_berkas=berkas.NAMA_BERKAS_DATA):
    daftar = []
    jumlah_rusak = 0
    for nomor, baris in enumerate(berkas.baca_data(nama_berkas), start=1):
        try:
            data = validasi.ubah_baris_ke_data(baris)
            daftar.append(Pengeluaran(**data))      # ** membongkar dict jadi kwargs
        except (DataTidakValidError, ValueError) as kesalahan:
            jumlah_rusak += 1
            print(f"[DILEWATI] Data ke-{nomor} rusak: {kesalahan}")
    return daftar, jumlah_rusak
 
 
if __name__ == "__main__":
    # Pengujian lokal pemrosesan.py
    contoh = [
        Pengeluaran(tanggal="2025-10-01", kategori="makan", keterangan="nasi", jumlah=15000),
        Pengeluaran(tanggal="2025-10-01", kategori="transport", keterangan="ojek", jumlah=12000),
    ]
    pengolah = PengolahData(contoh)
    assert pengolah.total() == 27000
    print(pengolah.buat_laporan())
 