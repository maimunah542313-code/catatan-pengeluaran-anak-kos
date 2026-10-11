import unittest
from program_suhu import analisis_suhu


class TestAnalisisSuhu(unittest.TestCase):

    def setUp(self):
        self.data = [
            {"hari": "Senin", "suhu": 31},
            {"hari": "Selasa", "suhu": 33},
            {"hari": "Rabu", "suhu": 29}
        ]

    def test_rata_rata(self):
        hasil = analisis_suhu(self.data)
        self.assertAlmostEqual(
            hasil["rata_rata"], 31
        )

    def test_suhu_tertinggi(self):
        hasil = analisis_suhu(self.data)
        self.assertEqual(
            hasil["tertinggi"]["hari"], "Selasa"
        )

    def test_jumlah_hari_panas(self):
        hasil = analisis_suhu(self.data)
        self.assertEqual(
            hasil["jumlah_panas"], 1
        )


if __name__ == "__main__":
    unittest.main()