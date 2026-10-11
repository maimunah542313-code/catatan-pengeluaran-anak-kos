NAMA_BERKAS_DATA = "data_pengeluaran.txt"
NAMA_BERKAS_LAPORAN = "laporan_pengeluaran.txt"
HEADER_DATA = "# tanggal | kategori | keterangan | jumlah | metode_bayar(opsional)"
 
 
def buat_berkas_data(nama_berkas=NAMA_BERKAS_DATA):
   
    try:
        with open(nama_berkas, "x", encoding="utf-8") as berkas:
            berkas.write(HEADER_DATA + "\n")
        print(f"[INFO] Berkas '{nama_berkas}' berhasil dibuat.")
        return True
    except FileExistsError:
        # Berkas sudah ada -> aman, tidak perlu dibuat lagi
        print(f"[INFO] Berkas '{nama_berkas}' sudah ada, data lama dipakai.")
        return False
 
 
def tambah_data(baris, nama_berkas=NAMA_BERKAS_DATA):
   
    with open(nama_berkas, "a", encoding="utf-8") as berkas:
        berkas.write(baris + "\n")
 
 
def baca_data(nama_berkas=NAMA_BERKAS_DATA):
   
    daftar_baris = []
    try:
        with open(nama_berkas, "r", encoding="utf-8") as berkas:
            for baris in berkas:               
                baris = baris.strip()           
                if baris == "" or baris.startswith("#"):
                    continue                    
                daftar_baris.append(baris)
    except FileNotFoundError:
        print(f"[PERINGATAN] Berkas '{nama_berkas}' belum ada. "
              f"Tambahkan data dulu atau buat berkas baru.")
    return daftar_baris
 
 
def tulis_laporan(teks_laporan, nama_berkas=NAMA_BERKAS_LAPORAN):
   
    with open(nama_berkas, "w", encoding="utf-8") as berkas:
        berkas.write(teks_laporan)
    print(f"[INFO] Laporan disimpan ke '{nama_berkas}'.")
 
 
if __name__ == "__main__":
    # Pengujian lokal: dijalankan hanya jika file ini dieksekusi langsung
    print("Uji lokal berkas.py")
    print(baca_data("berkas_yang_tidak_ada.txt"))   
 