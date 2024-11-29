import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from openpyxl import Workbook

# Fungsi untuk menambah program kerja
def tambah_proker():
    nama_proker = entry_nama.get()
    detail_proker = entry_detail.get()
    kategori_proker = kategori_var.get()
    tanggal_proker = entry_tanggal.get()

    # Validasi input
    if nama_proker == "" or detail_proker == "" or tanggal_proker == "":
        messagebox.showwarning("Input Error", "Semua kolom harus diisi!")
        return

    # Validasi format tanggal
    try:
        datetime.strptime(tanggal_proker, "%d/%m/%Y")
    except ValueError:
        messagebox.showwarning("Format Tanggal Salah", "Gunakan format DD/MM/YYYY.")
        return

    # Menambahkan ke daftar
    proker_list.append({"nama": nama_proker, "detail": detail_proker, "kategori": kategori_proker, "tanggal": tanggal_proker})
    listbox_proker.insert(tk.END, f"{tanggal_proker} - {nama_proker} - {kategori_proker}")
    entry_nama.delete(0, tk.END)
    entry_detail.delete(0, tk.END)
    entry_tanggal.delete(0, tk.END)

# Fungsi untuk menghapus program kerja
def hapus_proker():
    try:
        selected_index = listbox_proker.curselection()[0]
        listbox_proker.delete(selected_index)
        del proker_list[selected_index]
    except IndexError:
        messagebox.showwarning("Peringatan", "Pilih proker yang ingin dihapus!")

# Fungsi untuk menampilkan detail proker
def lihat_detail():
    try:
        selected_index = listbox_proker.curselection()[0]
        proker = proker_list[selected_index]
        messagebox.showinfo(
            "Detail Proker",
            f"Nama: {proker['nama']}\nTanggal: {proker['tanggal']}\nDetail: {proker['detail']}\nKategori: {proker['kategori']}"
        )
    except IndexError:
        messagebox.showwarning("Peringatan", "Pilih proker yang ingin dilihat detailnya!")

# Fungsi untuk mengekspor data ke file Excel
def export_to_excel():
    try:
        file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file:
            wb = Workbook()
            ws = wb.active
            ws.title = "Data Proker"

            # Header
            ws.append(["Tanggal", "Nama Proker", "Detail", "Kategori"])

            # Isi data
            for proker in proker_list:
                ws.append([proker["tanggal"], proker["nama"], proker["detail"], proker["kategori"]])

            # Simpan file
            wb.save(file)
            messagebox.showinfo("Sukses", "Data berhasil diekspor ke Excel!")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal mengekspor data: {e}")

# Data awal proker
proker_list = [
    {"nama": "Workshop Pemrograman", "detail": "Workshop tentang pemrograman Python.", "kategori": "Bulanan", "tanggal": "15/12/2024"},
    {"nama": "Seminar Teknologi", "detail": "Seminar tentang tren teknologi terbaru.", "kategori": "Tahunan", "tanggal": "25/12/2024"}
]

# Setup UI
root = tk.Tk()
root.title("Manajemen Proker Organisasi Himpunan Mahasiswa Informatika")
root.geometry("550x450")
root.config(bg="#E0E0E0")

# Frame Judul
frame_judul = tk.Frame(root, bg="#E0E0E0")
frame_judul.pack(pady=10)
judul = tk.Label(frame_judul, text="Manajemen Proker Organisasi Himpunan Mahasiswa Informatika", font=("Arial", 18, "bold"), bg="#E0E0E0", fg="#F5A623")
judul.pack()

# Frame Input
frame_input = tk.Frame(root, bg="#E0E0E0")
frame_input.pack(pady=10)
label_nama = tk.Label(frame_input, text="Nama Proker:", bg="#E0E0E0")
label_nama.grid(row=0, column=0)
entry_nama = tk.Entry(frame_input, width=30)
entry_nama.grid(row=0, column=1)

label_detail = tk.Label(frame_input, text="Detail Proker:", bg="#E0E0E0")
label_detail.grid(row=1, column=0)
entry_detail = tk.Entry(frame_input, width=30)
entry_detail.grid(row=1, column=1)

label_tanggal = tk.Label(frame_input, text="Tanggal (DD/MM/YYYY):", bg="#E0E0E0")
label_tanggal.grid(row=2, column=0)
entry_tanggal = tk.Entry(frame_input, width=30)
entry_tanggal.grid(row=2, column=1)

label_kategori = tk.Label(frame_input, text="Kategori Proker:", bg="#E0E0E0")
label_kategori.grid(row=3, column=0)
kategori_var = tk.StringVar(value="Bulanan")
kategori_bulanan = tk.Radiobutton(frame_input, text="Bulanan", variable=kategori_var, value="Bulanan", bg="#E0E0E0")
kategori_bulanan.grid(row=3, column=1, sticky="w")
kategori_tahunan = tk.Radiobutton(frame_input, text="Tahunan", variable=kategori_var, value="Tahunan", bg="#E0E0E0")
kategori_tahunan.grid(row=3, column=1, sticky="e")

# Frame Listbox dan Tombol
frame_listbox = tk.Frame(root, bg="#E0E0E0")
frame_listbox.pack(pady=10)
listbox_proker = tk.Listbox(frame_listbox, width=60, height=10)
listbox_proker.pack()

# Frame Tombol
frame_tombol = tk.Frame(root, bg="#E0E0E0")
frame_tombol.pack(pady=10)
tambah_button = tk.Button(frame_tombol, text="Tambah Proker", command=tambah_proker, bg="#F5A623")
tambah_button.pack(side=tk.LEFT, padx=5)

hapus_button = tk.Button(frame_tombol, text="Hapus Proker", command=hapus_proker, bg="#F5A623")
hapus_button.pack(side=tk.LEFT, padx=5)

detail_button = tk.Button(frame_tombol, text="Lihat Detail", command=lihat_detail, bg="#F5A623")
detail_button.pack(side=tk.LEFT, padx=5)

export_button = tk.Button(frame_tombol, text="Export to Excel", command=export_to_excel, bg="#F5A623")
export_button.pack(side=tk.LEFT, padx=5)

# Menampilkan Data Awal
for proker in proker_list:
    listbox_proker.insert(tk.END, f"{proker['tanggal']} - {proker['nama']} - {proker['kategori']}")

# Menjalankan aplikasi
root.mainloop()
