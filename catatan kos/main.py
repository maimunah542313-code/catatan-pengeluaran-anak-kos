from datetime import date

from pengeluaran import berkas, pemrosesan, pengujian
from pengeluaran.pemrosesan import Pengeluaran, PengolahData
from pengeluaran.validasi import DataTidakValidError


def tampilkan_menu():
    print("\n===== CATATAN PENGELUARAN ANAK KOS =====")
    print("1. Tambah pengeluaran")
    print("2. Lihat semua pengeluaran")
    print("3. Buat laporan (simpan ke berkas)")
    print("4. Cari berdasarkan kategori")
    print("5. Jalankan pengujian")
    print("0. Keluar")


def menu_tambah():
    #Meminta input, memvalidasi, lalu menyimpan ke berkas.
    tanggal = input("Tanggal (YYYY-MM-DD, kosongkan = hari ini): ").strip()
    if tanggal == "":
        tanggal = date.today().isoformat()
    kategori = input("Kategori (makan/transport/listrik/dll): ")
    keterangan = input("Keterangan: ")
    jumlah = input("Jumlah (Rp): ")
    metode_bayar = input("Metode bayar (opsional, Enter untuk lewati): ").strip()

    # Atribut dikumpulkan di dictionary, atribut opsional hanya ditambah bila diisi
    data = {"tanggal": tanggal, "kategori": kategori,
            "keterangan": keterangan, "jumlah": jumlah}
    if metode_bayar:
        data["metode_bayar"] = metode_bayar

    try:
        catatan = Pengeluaran(**data)            # validasi terjadi di dalam class
        berkas.tambah_data(catatan.ke_baris())   # simpan ke berkas (mode 'a')
        print("[OK] Data tersimpan.")
    except DataTidakValidError as kesalahan:
        print(f"[GAGAL] {kesalahan}")


def menu_lihat():
    daftar, rusak = pemrosesan.muat_pengeluaran()
    if not daftar:
        print("Belum ada data.")
        return
    for nomor, catatan in enumerate(daftar, start=1):
        print(f"{nomor:>2}. {catatan.ringkasan()}")
    if rusak:
        print(f"({rusak} baris rusak dilewati)")


def menu_laporan():
    daftar, _ = pemrosesan.muat_pengeluaran()
    if not daftar:
        print("Belum ada data untuk dilaporkan.")
        return
    teks = PengolahData(daftar).buat_laporan()
    print(teks)
    berkas.tulis_laporan(teks)       # simpan laporan (mode 'w')


def menu_cari():
    kategori = input("Kategori yang dicari: ")
    daftar, _ = pemrosesan.muat_pengeluaran()
    hasil = PengolahData(daftar).filter_kategori(kategori)
    if not hasil:
        print("Tidak ada data untuk kategori itu.")
    for catatan in hasil:
        print(catatan.ringkasan())


def jalankan():
    berkas.buat_berkas_data()        # mode 'x': buat berkas data bila belum ada
    while True:
        tampilkan_menu()
        pilihan = input("Pilihan Anda: ").strip()
        if pilihan == "1":
            menu_tambah()
        elif pilihan == "2":
            menu_lihat()
        elif pilihan == "3":
            menu_laporan()
        elif pilihan == "4":
            menu_cari()
        elif pilihan == "5":
            pengujian.jalankan_pengujian()
        elif pilihan == "0":
            print("Terima kasih, sampai jumpa!")
            break
        else:
            print("Pilihan tidak dikenal, coba lagi.")


if __name__ == "__main__":
    jalankan()
