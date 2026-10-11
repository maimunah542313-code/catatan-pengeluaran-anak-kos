def hitung_kelulusan(nama, daftar_nilai, batas_lulus=70):
    rata_rata = sum(daftar_nilai) / len(daftar_nilai)

    print(f"Nama : {nama}")
    print(f"Rata-rata : {rata_rata}")
    
   #untuk penyederhanaan if/else
    status = "Lulus" if rata_rata >= batas_lulus else "Tidak Lulus"
    print(f"Status : {status}\n")
    
    return rata_rata

if __name__ == '__main__':
    hitung_kelulusan("Budi", [80, 75, 90])
    hitung_kelulusan("Sari", [60, 65, 55, 70])