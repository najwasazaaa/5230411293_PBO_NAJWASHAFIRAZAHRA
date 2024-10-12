class Debitur:
    def __init__(self, nama, ktp, limit_pinjaman):
        self.nama = nama
        self.__ktp = ktp  
        self._limit_pinjaman = limit_pinjaman  

    def tampilkan_debitur(self):
        return f"Nama: {self.nama}, KTP: {self.__ktp}, Limit Pinjaman: {self._limit_pinjaman}"

    def get_ktp(self):
        return self.__ktp

    def get_limit_pinjaman(self):
        return self._limit_pinjaman


class KelolaDebitur:
    def __init__(self):
        self.debitur_list = []

    def tambah_debitur(self, nama, ktp, limit_pinjaman):
        if not isinstance(limit_pinjaman, (int, float)) or limit_pinjaman <= 0:
            print("Validasi Gagal: Limit pinjaman harus berupa angka positif.")
            return

        for debitur in self.debitur_list:
            if debitur.get_ktp() == ktp:
                print("Validasi Gagal: KTP sudah ada.")
                return

        debitur_baru = Debitur(nama, ktp, limit_pinjaman)
        self.debitur_list.append(debitur_baru)
        print(f"Debitur {nama} berhasil ditambahkan.")

    def cari_debitur(self, nama):
        for debitur in self.debitur_list:
            if debitur.nama.lower() == nama.lower():
                print(debitur.tampilkan_debitur())
                return
        print("Debitur tidak ditemukan.")

    def tampilkan_debitur(self):
        if not self.debitur_list:
            print("Tidak ada debitur yang terdaftar.")
            return
        for debitur in self.debitur_list:
            print(debitur.tampilkan_debitur())


class Pinjaman:
    def __init__(self, nama_debitur, pinjaman, bunga, bulan):
        self.nama_debitur = nama_debitur
        self.pinjaman = pinjaman
        self.bunga = bunga
        self.bulan = bulan

    def angsuran_pokok(self):
        return self.pinjaman * (self.bunga / 100)

    def anggaran_bulanan(self):
        return self.angsuran_pokok() / self.bulan

    def total_angsuran(self):
        return self.angsuran_pokok() + self.anggaran_bulanan()


class KelolaPinjaman:
    def __init__(self, kelola_debitur):
        self.kelola_debitur = kelola_debitur
        self.pinjaman_list = []

    def tambah_pinjaman(self, nama_debitur, pinjaman, bunga, bulan):
        for debitur in self.kelola_debitur.debitur_list:
            if debitur.nama.lower() == nama_debitur.lower():
                if pinjaman > debitur.get_limit_pinjaman():
                    print("Validasi Gagal: Pinjaman melebihi limit.")
                    return
                pinjaman_baru = Pinjaman(nama_debitur, pinjaman, bunga, bulan)
                self.pinjaman_list.append(pinjaman_baru)
                print(f"Pinjaman untuk {nama_debitur} berhasil ditambahkan.")
                return
        print("Validasi Gagal: Debitur tidak ditemukan.")

    def tampilkan_pinjaman(self):
        if not self.pinjaman_list:
            print("Tidak ada pinjaman yang terdaftar.")
            return
        for pinjaman in self.pinjaman_list:
            print(f"Nama: {pinjaman.nama_debitur}, Pinjaman: {pinjaman.pinjaman}, Bunga: {pinjaman.bunga}%, Bulan: {pinjaman.bulan}, Anggaran/Bulan: {pinjaman.anggaran_bulanan()}")


# Initialize the management classes
kelola_debitur = KelolaDebitur()
kelola_debitur.tambah_debitur("najwa", 23497, 500000)
kelola_debitur.tambah_debitur("afra", 26768, 500000)

kelola_pinjaman = KelolaPinjaman(kelola_debitur)  # Pass the instance of KelolaDebitur

while True:
    print("\nMenu Utama:")
    print("=============Aplikasi admin pinjol =============")
    print("1. Kelola Debitur")
    print("2. Pinjaman")
    print("3. Keluar")

    pilihan_utama = input("Pilih opsi (1-3): ")

    if pilihan_utama == '1':
        while True:
            print("\nMenu Kelola Debitur:")
            print("1. Tampilkan semua debitur")
            print("2. Cari debitur")
            print("3. Tambah debitur")
            print("4. Kembali ke Menu Utama")

            pilihan_debitur = input("Pilih opsi (1-4): ")

            if pilihan_debitur == '1':
                kelola_debitur.tampilkan_debitur()

            elif pilihan_debitur == '2':
                nama = input("Masukkan Nama Debitur yang dicari: ")
                kelola_debitur.cari_debitur(nama)

            elif pilihan_debitur == '3':
                nama = input("Masukkan Nama Debitur: ")
                ktp = input("Masukkan KTP Debitur: ")
                limit_pinjaman = float(input("Masukkan Limit Pinjaman: "))
                kelola_debitur.tambah_debitur(nama, ktp, limit_pinjaman)

            elif pilihan_debitur == '4':
                break  

            else:
                print("Pilihan tidak valid! Silakan pilih lagi.")

    elif pilihan_utama == '2':
        while True:
            print("\nMenu Kelola Peminjaman:")
            print("1. Tambah Pinjaman")
            print("2. Tampilkan Pinjaman")
            print("3. Kembali ke Menu Utama")

            pilihan_pinjaman = input("Pilih opsi (1-3): ")

            if pilihan_pinjaman == '1':
                nama_debitur = input("Masukkan Nama Debitur untuk pinjaman: ")
                pinjaman = float(input("Masukkan Jumlah Pinjaman: "))
                bunga = float(input("Masukkan Bunga (%): "))
                bulan = int(input("Masukkan Lama Pinjaman (bulan): "))
                kelola_pinjaman.tambah_pinjaman(nama_debitur, pinjaman, bunga, bulan)

            elif pilihan_pinjaman == '2':
                kelola_pinjaman.tampilkan_pinjaman()

            elif pilihan_pinjaman == '3':
                break  

            else:
                print("Pilihan tidak valid! Silakan pilih lagi.")

    elif pilihan_utama == '3':
        print("Terima kasih! Program dihentikan.")
        break

    else:
        print("Pilihan tidak valid! Silakan pilih lagi.")