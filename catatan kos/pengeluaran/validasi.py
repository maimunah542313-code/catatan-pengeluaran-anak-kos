from datetime import datetime
 
class DataTidakValidError(Exception):
    pass
 
 
def validasi_tidak_kosong(nilai, nama_field):
    if nilai is None or str(nilai).strip() == "":
        raise DataTidakValidError(f"Field '{nama_field}' tidak boleh kosong.")
    return str(nilai).strip()
 
 
def validasi_jumlah(teks_jumlah):
    try:
        jumlah = int(teks_jumlah)               # bisa gagal - ValueError
    except (ValueError, TypeError):
        raise DataTidakValidError(f"Jumlah '{teks_jumlah}' bukan angka bulat.")
    if jumlah <= 0:
        raise DataTidakValidError("Jumlah harus lebih dari 0 (tidak boleh negatif).")
    return jumlah
 
 
def validasi_tanggal(teks_tanggal):
    try:
        datetime.strptime(teks_tanggal, "%Y-%m-%d")
    except ValueError:
        raise DataTidakValidError(
            f"Tanggal '{teks_tanggal}' salah. Pakai format TTTT-BB-HH, contoh 2025-10-31.")
    return teks_tanggal
 
 
def ubah_baris_ke_data(baris):
    bagian = [b.strip() for b in baris.split("|")]
    if len(bagian) < 4:
        raise DataTidakValidError(f"Kolom kurang (butuh minimal 4): '{baris}'")
 
    data = {
        "tanggal": validasi_tanggal(bagian[0]),
        "kategori": validasi_tidak_kosong(bagian[1], "kategori").lower(),
        "keterangan": validasi_tidak_kosong(bagian[2], "keterangan"),
        "jumlah": validasi_jumlah(bagian[3]),
    }
    if len(bagian) >= 5 and bagian[4] != "":
        data["metode_bayar"] = bagian[4]
    return data
 
 
if __name__ == "__main__":
    # Pengujian lokal memakai assert
    assert validasi_jumlah("15000") == 15000
    assert validasi_tanggal("2025-10-31") == "2025-10-31"
    try:
        validasi_jumlah("-500")
    except DataTidakValidError as pesan:
        print("OK, nilai negatif ditolak:", pesan)
    print("Semua uji lokal validasi.py lulus.")
 