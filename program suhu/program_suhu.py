def baca_data(nama_file):
    data = []

    try:
        with open(nama_file, "r") as file:
            for baris in file:
                hari, suhu = baris.strip().split(";")
                data.append({
                    "hari": hari,
                    "suhu": float(suhu)
                })

    except FileNotFoundError:
        print("File suhu tidak ditemukan!")
        return []

    return data


def analisis_suhu(data, *args, **kwargs):
    if not data:
        return None

    suhu_tertinggi = max(data, key=lambda x: x["suhu"])
    suhu_terendah = min(data, key=lambda x: x["suhu"])

    rata_rata = sum(
        item["suhu"] for item in data
    ) / len(data)

    batas_panas = kwargs.get("batas_panas", 32)

    hasil = []

    for item in data:
        kategori = (
            "Panas"
            if item["suhu"] >= batas_panas
            else "Normal"
        )

        hasil.append({
            "hari": item["hari"],
            "suhu": item["suhu"],
            "kategori": kategori
        })

    jumlah_panas = sum(
        1 for item in hasil
        if item["kategori"] == "Panas"
    )

    return {
        "rata_rata": rata_rata,
        "tertinggi": suhu_tertinggi,
        "terendah": suhu_terendah,
        "jumlah_panas": jumlah_panas,
        "detail": hasil
    }


def tulis_laporan(hasil, nama_file):
    with open(nama_file, "w") as file:
        file.write("LAPORAN ANALISIS SUHU MINGGUAN\n")
        file.write("==============================\n")

        for item in hasil["detail"]:
            file.write(
                f'{item["hari"]}: {item["suhu"]} derajat - '
                f'{item["kategori"]}\n'
            )

        file.write(
            f'\nRata-rata suhu: {hasil["rata_rata"]:.2f}\n'
        )
        file.write(
            f'Hari terpanas: {hasil["tertinggi"]["hari"]} '
            f'({hasil["tertinggi"]["suhu"]} derajat)\n'
        )
        file.write(
            f'Hari terdingin: {hasil["terendah"]["hari"]} '
            f'({hasil["terendah"]["suhu"]} derajat)\n'
        )
        file.write(
            f'Jumlah hari panas: {hasil["jumlah_panas"]}\n'
        )


def main():
    data = baca_data("suhu.txt")

    if not data:
        return

    hasil = analisis_suhu(data, batas_panas=32)

    tulis_laporan(hasil, "laporan_suhu.txt")

    with open("laporan_suhu.txt", "r") as file:
        print(file.read())


if __name__ == "__main__":
    main()
    