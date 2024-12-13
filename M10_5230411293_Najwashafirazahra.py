import pymysql
from tabulate import tabulate
from decimal import Decimal

def read_choice(prompt, options):
    """Fungsi untuk membaca input dengan validasi opsi."""
    while True:
        print(prompt)
        choice = input("Pilih opsi: ")
        if choice in options:
            return choice
        print("\nOpsi tidak valid, coba lagi.")

# Konfigurasi koneksi database
db_config = {
    'host': 'localhost',
    'user': 'root',  # Ganti dengan username MySQL Anda
    'password': '',  # Ganti dengan password MySQL Anda
    'database': 'penjualan',
    'cursorclass': pymysql.cursors.DictCursor  # Menentukan bahwa kursor yang digunakan adalah DictCursor
}

# Fungsi untuk membuat koneksi database
def get_db_connection():
    try:
        connection = pymysql.connect(**db_config)
        return connection
    except pymysql.MySQLError as e:
        print(f"Kesalahan koneksi ke database: {e}")
        return None

# Fungsi untuk menampilkan daftar pegawai
def show_pegawai():
    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Pegawai")
        pegawai = cursor.fetchall()
        if pegawai:
            print("\nDaftar Pegawai:")
            print(tabulate(pegawai, headers="keys", tablefmt="pretty"))
        else:
            print("\nBelum ada data pegawai.")
    except pymysql.MySQLError as e:
        print(f"Kesalahan saat mengambil data pegawai: {e}")
    finally:
        connection.close()

# Fungsi untuk menambahkan data pegawai
def add_pegawai():
    nik = input("Masukkan NIK Pegawai Baru: ")
    nama = input("Masukkan Nama Pegawai Baru: ")
    alamat = input("Masukkan Alamat Pegawai Baru: ")

    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Pegawai (NIK, Nama, Alamat) VALUES (%s, %s, %s)",
            (nik, nama, alamat)
        )
        connection.commit()
        print("\nPegawai baru berhasil ditambahkan!")
    except pymysql.IntegrityError:
        print(f"\nPegawai dengan NIK {nik} sudah ada di database!")
    except pymysql.MySQLError as e:
        print(f"\nGagal menambahkan pegawai: {e}")
    finally:
        connection.close()

# Fungsi untuk menampilkan daftar produk berdasarkan kategori
def show_produk(kategori=None):
    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        if kategori:
            cursor.execute("SELECT * FROM Produk WHERE JenisProduk = %s", (kategori,))
        else:
            cursor.execute("SELECT * FROM Produk")
        produk = cursor.fetchall()
        if produk:
            print(f"\nDaftar Produk ({kategori if kategori else 'Semua Produk'}):")
            print(tabulate(produk, headers="keys", tablefmt="pretty"))
        else:
            print(f"\nBelum ada data produk di kategori {kategori if kategori else 'semua kategori'}.")
    except pymysql.MySQLError as e:
        print(f"Kesalahan saat mengambil data produk: {e}")
    finally:
        connection.close()

# Fungsi untuk menambahkan produk baru
def add_produk():
    kode_produk = input("Masukkan Kode Produk: ")
    nama_produk = input("Masukkan Nama Produk: ")
    harga = float(input("Masukkan Harga Produk: "))
    jenis_produk = input("Masukkan Jenis Produk (Snack/Makanan/Minuman): ")

    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Produk (KodeProduk, NamaProduk, Harga, JenisProduk) VALUES (%s, %s, %s, %s)",
            (kode_produk, nama_produk, harga, jenis_produk)
        )
        connection.commit()
        print("\nProduk baru berhasil ditambahkan!")
    except pymysql.MySQLError as e:
        print(f"\nGagal menambahkan produk: {e}")
    finally:
        connection.close()

# Fungsi untuk menampilkan data transaksi
def show_transaksi():
    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Transaksi")
        transaksi = cursor.fetchall()
        if transaksi:
            print("\nDaftar Transaksi:")
            print(tabulate(transaksi, headers="keys", tablefmt="pretty"))
        else:
            print("\nBelum ada data transaksi.")
    except pymysql.MySQLError as e:
        print(f"Kesalahan saat mengambil data transaksi: {e}")
    finally:
        connection.close()

# Fungsi untuk menambahkan transaksi baru
def add_transaksi():
    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        # Generate nomor transaksi otomatis
        cursor.execute("SELECT IFNULL(MAX(NoTransaksi), 0) + 1 AS NextNoTransaksi FROM Transaksi")
        next_no_transaksi = cursor.fetchone()['NextNoTransaksi']  # Mengakses nilai pertama dari dictionary

        # Pastikan next_no_transaksi adalah integer
        next_no_transaksi = int(next_no_transaksi)

        no_transaksi = f"T{next_no_transaksi:05d}"

        print(f"\nNomor Transaksi: {no_transaksi}")

        no_pegawai = input("Masukkan Nomor Pegawai: ")
        kode_produk = input("Masukkan Kode Produk: ")
        jumlah_produk = int(input("Masukkan Jumlah Produk: "))

        # Ambil harga produk
        cursor.execute("SELECT Harga FROM Produk WHERE KodeProduk = %s", (kode_produk,))
        produk = cursor.fetchone()
        if produk:
            harga_produk = produk['Harga']  # Mengakses harga produk menggunakan nama kolom
            total_harga = harga_produk * jumlah_produk

            print(f"\nTotal Harga: Rp{total_harga}")
            uang_dibayar = input("Masukkan Uang yang Dibayarkan: ").replace('Rp', '').replace(',', '').strip()

            try:
                uang_dibayar = Decimal(uang_dibayar)  # Menggunakan Decimal di sini
            except ValueError:
                print("\nInput tidak valid, pastikan hanya angka yang dimasukkan.")
                return  # Menghentikan eksekusi jika terjadi kesalahan

            # Pastikan total_harga juga menggunakan Decimal
            total_harga = Decimal(total_harga)  # Mengonversi total_harga menjadi Decimal jika perlu

            if uang_dibayar < total_harga:
                print("\nUang yang dibayarkan kurang, transaksi gagal!")
                return

            kembalian = uang_dibayar - total_harga  # Operasi ini sekarang aman
            print(f"Kembalian: Rp{kembalian:.2f}")

            # Simpan transaksi
            cursor.execute(
                "INSERT INTO Transaksi (NoTransaksi, NoPegawai, KodeProduk, JumlahProduk, TotalHarga, UangDibayar, Kembalian) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (no_transaksi, no_pegawai, kode_produk, jumlah_produk, total_harga, uang_dibayar, kembalian)
            )
            connection.commit()

            # Simpan struk
            cursor.execute(
                "INSERT INTO Struk (NoTransaksi, NamaPegawai, NamaProduk, JumlahProduk, TotalHarga) "
                "SELECT %s, p.Nama, pr.NamaProduk, %s, %s "
                "FROM Pegawai p, Produk pr WHERE p.NIK = %s AND pr.KodeProduk = %s",
                (no_transaksi, jumlah_produk, total_harga, no_pegawai, kode_produk)
            )
            connection.commit()
            print("\nTransaksi berhasil ditambahkan!")
        else:
            print("\nProduk tidak ditemukan!")
    except pymysql.MySQLError as e:
        print(f"\nGagal menambahkan transaksi: {e}")
    finally:
        connection.close()

# Menu Pegawai
def menu_pegawai():
    while True:
        choice = read_choice(
            "\n--- Menu Pegawai ---\n1. Lihat Daftar Pegawai\n2. Tambah Pegawai\n3. Kembali ke Menu Utama",
            ['1', '2', '3']
        )

        if choice == '1':
            show_pegawai()
        elif choice == '2':
            add_pegawai()
        elif choice == '3':
            break

# Menu Produk
def menu_produk():
    while True:
        choice = read_choice(
            "\n--- Menu Produk ---\n1. Lihat Semua Produk\n2. Lihat Produk Snack\n3. Lihat Produk Makanan\n4. Lihat Produk Minuman\n5. Tambah Produk\n6. Kembali ke Menu Utama",
            ['1', '2', '3', '4', '5', '6']
        )

        if choice == '1':
            show_produk()
        elif choice == '2':
            show_produk(kategori="Snack")
        elif choice == '3':
            show_produk(kategori="Makanan")
        elif choice == '4':
            show_produk(kategori="Minuman")
        elif choice == '5':
            add_produk()
        elif choice == '6':
            break

# Menu Transaksi
def menu_transaksi():
    while True:
        choice = read_choice(
            "\n--- Menu Transaksi ---\n1. Lihat Daftar Transaksi\n2. Tambah Transaksi\n3. Kembali ke Menu Utama",
            ['1', '2', '3']
        )

        if choice == '1':
            show_transaksi()
        elif choice == '2':
            add_transaksi()
        elif choice == '3':
            break

# Menu Utama
def main():
    while True:
        choice = read_choice(
            "\n--- Menu penjualan ---\n1. Menu Pegawai\n2. Menu Produk\n3. Menu Transaksi\n4. Keluar",
            ['1', '2', '3', '4']
        )

        if choice == '1':
            menu_pegawai()
        elif choice == '2':
            menu_produk()
        elif choice == '3':
            menu_transaksi()
        elif choice == '4':
            print("Terima kasih, program selesai.")
            break

if __name__ == "__main__":
    main()
