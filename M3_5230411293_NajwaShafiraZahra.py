def harga(rupiah):
    return rupiah

class DaftarMenu:
    def __init__(self):
        self.makanan = {
            "Kwetiaw": 10000,
            "Mie dokdok": 15000,
            "Telur Gulung": 12000,
            "Nasi Goreng": 18000,
        }
        self.minuman = {
            "Jus Alpukat": 5000,
            "Jus Mangga": 6000,
            "Kopi Susu": 7000,
            "Teh Manis": 4000,
        }

    def tampilkan_daftar_makanan(self):
        if not self.makanan:
            print("Daftar makanan kosong.")
        else:
            print("Daftar Makanan:")
            for idx, makanan in enumerate(self.makanan, start=1):
                print(f"{idx}. {makanan}")

    def tampilkan_daftar_minuman(self):
        if not self.minuman:
            print("Daftar minuman kosong.")
        else:
            print("Daftar Minuman:")
            for idx, minuman in enumerate(self.minuman, start=1):
                print(f"{idx}. {minuman}")

    def tambah_makanan(self, nama_makanan):
        self.makanan.append(nama_makanan)
        print(f"{nama_makanan} telah ditambahkan ke daftar makanan.")

    def tambah_minuman(self, nama_minuman):
        self.minuman.append(nama_minuman)
        print(f"{nama_minuman} telah ditambahkan ke daftar minuman.")

def main():
    menu = DaftarMenu()

    while True:
        print("=== Menu ===")
        print("1. Tampilkan Daftar Makanan yang ada pada menu ")
        print("2. Tampilkan Daftar Minuman yang ada pada menu ")
        print("3. Tambah Makanan yang ingin anda masukkan")
        print("4. Tambah Minuman yang ingin anda masukkan ")
        print("5. Keluar")
        
        pilihan = input("Pilih opsi (1-5): ")

        if pilihan == '1':
            menu.tampilkan_daftar_makanan()
        elif pilihan == '2':
            menu.tampilkan_daftar_minuman()
        elif pilihan == '3':
            nama_makanan = input("Masukkan nama makanan: ")
            menu.tambah_makanan(nama_makanan)
        elif pilihan == '4':
            nama_minuman = input("Masukkan nama minuman: ")
            menu.tambah_minuman(nama_minuman)
        elif pilihan == '5':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
