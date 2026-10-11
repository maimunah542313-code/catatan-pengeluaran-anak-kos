import os
import tempfile
import unittest
 
from . import berkas, validasi
from .pemrosesan import Pengeluaran, PengolahData, muat_pengeluaran
from .validasi import DataTidakValidError
 
 
class PengujianValidasi(unittest.TestCase):
 
    def test_jumlah_valid(self):
        self.assertEqual(validasi.validasi_jumlah("15000"), 15000)
 
    def test_jumlah_negatif_ditolak(self):
        with self.assertRaises(DataTidakValidError):
            validasi.validasi_jumlah("-100")
 
    def test_jumlah_bukan_angka_ditolak(self):
        with self.assertRaises(DataTidakValidError):
            validasi.validasi_jumlah("abc")
 
    def test_tanggal_salah_ditolak(self):
        with self.assertRaises(DataTidakValidError):
            validasi.validasi_tanggal("31-10-2025")
 
    def test_field_kosong_ditolak(self):
        with self.assertRaises(DataTidakValidError):
            validasi.validasi_tidak_kosong("   ", "kategori")
 
 
class PengujianPengolahData(unittest.TestCase):
 
    def setUp(self):
        self.pengolah = PengolahData([
            Pengeluaran(tanggal="2025-10-01", kategori="makan", keterangan="nasi", jumlah=15000),
            Pengeluaran(tanggal="2025-10-01", kategori="makan", keterangan="kopi", jumlah=10000),
            Pengeluaran(tanggal="2025-10-02", kategori="listrik", keterangan="token", jumlah=50000),
        ])
 
    def test_total(self):
        self.assertEqual(self.pengolah.total(), 75000)
 
    def test_total_per_kategori(self):
        self.assertEqual(self.pengolah.total_per_kategori(),
                         {"makan": 25000, "listrik": 50000})
 
    def test_kategori_terboros(self):
        self.assertEqual(self.pengolah.kategori_terboros(), ("listrik", 50000))
 
    def test_urutkan_terbesar(self):
        teratas = self.pengolah.urutkan_terbesar(jumlah_teratas=1)
        self.assertEqual(teratas[0].jumlah, 50000)
 
    def test_rata_rata_harian(self):
        self.assertEqual(self.pengolah.rata_rata_harian(), 37500)  # 75000 / 2 hari
 
 
class PengujianBerkas(unittest.TestCase):
 
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.jalur = os.path.join(self.folder.name, "uji.txt")
 
    def tearDown(self):
        self.folder.cleanup()       # membersihkan folder sementara
 
    def test_buat_berkas_dua_kali(self):
        self.assertTrue(berkas.buat_berkas_data(self.jalur))    # pertama: dibuat
        self.assertFalse(berkas.buat_berkas_data(self.jalur))   # kedua: sudah ada
 
    def test_baca_berkas_tidak_ada(self):
        self.assertEqual(berkas.baca_data(self.jalur), [])
 
    def test_baris_rusak_dilewati(self):
        berkas.buat_berkas_data(self.jalur)
        berkas.tambah_data("2025-10-01 | makan | nasi | 15000", self.jalur)   # benar
        berkas.tambah_data("2025-10-01 | makan | soto | abc", self.jalur)      # rusak
        berkas.tambah_data("data ngawur", self.jalur)                          # rusak
        daftar, rusak = muat_pengeluaran(self.jalur)
        self.assertEqual(len(daftar), 1)
        self.assertEqual(rusak, 2)
 
 
def jalankan_pengujian():
    muat = unittest.TestLoader()
    kumpulan = unittest.TestSuite()
    for kelas in (PengujianValidasi, PengujianPengolahData, PengujianBerkas):
        kumpulan.addTests(muat.loadTestsFromTestCase(kelas))
    unittest.TextTestRunner(verbosity=2).run(kumpulan)
 
 
if __name__ == "__main__":
    jalankan_pengujian()