import tkinter as tk
from antrian import SistemAntrian
import tkinter.messagebox

# Inisialisasi sistem antrian
sistem_antrian = SistemAntrian()

# Fungsi untuk menambah antrian ke ruangan tertentu
def tambah_antrian(kode_ruangan):
    nomor_antrian = len(sistem_antrian.ruangan[kode_ruangan].queue) + 1
    sistem_antrian.tambah_antrian(kode_ruangan, nomor_antrian)
    tk.messagebox.showinfo("Informasi", f"Nomor antrian {nomor_antrian} untuk {kode_ruangan} telah ditambahkan.")
    update_notifikasi()

# Fungsi untuk memanggil antrian dengan suara dan menampilkan tulisan
def panggil_antrian_dan_suara():
    kode_ruangan = kode_ruangan_var.get()
    if kode_ruangan in sistem_antrian.ruangan:
        pesan = sistem_antrian.panggil_antrian_dan_suara(kode_ruangan)
        antrian_label.config(text=pesan)
        update_notifikasi()
    else:
        tk.messagebox.showerror("Error", "Kode ruangan tidak valid.")

# Fungsi untuk menghentikan timer otomatis
def hentikan_timer():
    kode_ruangan = kode_ruangan_var.get()
    if kode_ruangan in sistem_antrian.ruangan:
        sistem_antrian.hentikan_timer(kode_ruangan)
        tk.messagebox.showinfo("Informasi", f"Timer untuk {kode_ruangan} telah dihentikan.")
    else:
        tk.messagebox.showerror("Error", "Kode ruangan tidak valid.")

# Fungsi untuk menampilkan antrian yang sedang aktif
def tampilkan_antrian():
    antrian_list = ""
    for kode_ruangan, antrian in sistem_antrian.ruangan.items():
        antrian_list += str(antrian) + "\n"
    tk.messagebox.showinfo("Antrian Aktif", antrian_list)

# Fungsi untuk keluar dari aplikasi
def keluar():
    app.quit()

# Fungsi untuk memperbarui jendela notifikasi
def update_notifikasi():
    for i, (kode_ruangan, antrian) in enumerate(sistem_antrian.ruangan.items()):
        notifikasi_labels[i + 1][0].config(text=antrian.nama_ruangan)  # +1 untuk melewati header
        notifikasi_labels[i + 1][1].config(text=antrian.current if antrian.current else "Tidak ada antrian")

# Membuat aplikasi GUI
app = tk.Tk()
app.title("Aplikasi Antrian Rumah Sakit")
app.geometry("400x400")
app.configure(bg="black")

# Membuat jendela notifikasi
notifikasi_window = tk.Toplevel(app)
notifikasi_window.title("Notifikasi Antrian")
notifikasi_window.geometry("400x200")
notifikasi_window.configure(bg="black")

# Membuat tabel notifikasi dengan header
notifikasi_labels = []
header = ["Ruang", "No Antrian"]
for i in range(4):  # Jumlah ruangan + 1 untuk header
    row = []
    for j in range(2):  # Dua kolom: Nama Ruangan dan Nomor Antrian
        if i == 0:  # Baris header
            label = tk.Label(notifikasi_window, text=header[j], bg="blue", fg="white", borderwidth=1, relief="solid", width=20)
        else:  # Baris data
            label = tk.Label(notifikasi_window, text="", bg="black", fg="white", borderwidth=1, relief="solid", width=20)
        label.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        row.append(label)
    notifikasi_labels.append(row)

# Membuat tombol untuk menambahkan antrian ke setiap ruangan
tk.Button(app, text="Tambah Antrian CTScan (R01)", command=lambda: tambah_antrian("R01"), bg="blue", fg="white").pack(pady=5)
tk.Button(app, text="Tambah Antrian MRI 1,5T (R02)", command=lambda: tambah_antrian("R02"), bg="blue", fg="white").pack(pady=5)
tk.Button(app, text="Tambah Antrian USG (R03)", command=lambda: tambah_antrian("R03"), bg="blue", fg="white").pack(pady=5)

# Membuat label dan entry untuk memasukkan kode ruangan yang akan dipanggil
tk.Label(app, text="Kode Ruangan:", bg="black", fg="white").pack(pady=5)
kode_ruangan_var = tk.StringVar()
tk.Entry(app, textvariable=kode_ruangan_var).pack()

# Membuat tombol untuk memanggil antrian dengan suara
tk.Button(app, text="Panggil Antrian dengan Suara", command=panggil_antrian_dan_suara, bg="blue", fg="white").pack(pady=5)

# Membuat label untuk menampilkan tulisan antrian yang dipanggil
antrian_label = tk.Label(app, text="", bg="black", fg="white")
antrian_label.pack(pady=20)

# Membuat tombol untuk menghentikan timer
tk.Button(app, text="Hentikan Timer", command=hentikan_timer, bg="blue", fg="white").pack(pady=5)

# Membuat tombol untuk menampilkan antrian
tk.Button(app, text="Tampilkan Antrian", command=tampilkan_antrian, bg="blue", fg="white").pack(pady=5)

# Membuat tombol untuk keluar dari aplikasi
tk.Button(app, text="Keluar", command=keluar, bg="blue", fg="white").pack(pady=5)

# Memperbarui jendela notifikasi saat aplikasi pertama kali dijalankan
update_notifikasi()

app.mainloop()
