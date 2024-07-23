import pyttsx3
import threading

# Kelas Antrian untuk menangani antrian pada setiap ruangan
class Antrian:
    def __init__(self, nama_ruangan):
        self.nama_ruangan = nama_ruangan  # Nama ruangan
        self.queue = []  # Daftar nomor antrian
        self.current = None  # Nomor antrian yang sedang dipanggil
        self.history = []  # Riwayat antrian
        self.timer = None  # Timer untuk antrian otomatis

    def tambah_antrian(self, nomor):
        self.queue.append(nomor)  # Menambahkan nomor antrian ke daftar
        self.history.append((nomor, "Belum Terpanggil"))  # Menambahkan nomor antrian ke riwayat

    def panggil_antrian(self):
        if self.timer is not None:
            self.timer.cancel()  # Membatalkan timer jika ada

        if self.queue:
            self.current = self.queue.pop(0)  # Mengambil nomor antrian pertama
            self.history.append((self.current, "Terpanggil"))  # Menyimpan ke riwayat dengan status 'Terpanggil'
            self.set_timer()  # Mengatur timer untuk panggilan otomatis
        else:
            self.current = None  # Jika tidak ada antrian

    def __str__(self):
        if self.current:
            return f"{self.nama_ruangan}: Memanggil antrian nomor {self.current}"
        else:
            return f"{self.nama_ruangan}: Tidak ada antrian yang dipanggil"

    def panggil_antrian_dengan_suara(self):
        if self.current:
            engine = pyttsx3.init()  # Inisialisasi engine text-to-speech
            pesan = f"{self.nama_ruangan}, memanggil antrian nomor {self.current}"
            engine.say(pesan)  # Mengatur teks yang akan diucapkan
            engine.runAndWait()  # Menjalankan engine text-to-speech
            return pesan
        else:
            return f"{self.nama_ruangan}: Tidak ada antrian yang dipanggil"
        
    def panggil_antrian_dan_suara(self):
        self.panggil_antrian()  # Memanggil antrian
        return self.panggil_antrian_dengan_suara()  # Memanggil antrian dengan suara
    
    def set_timer(self):
        self.timer = threading.Timer(10, self.panggil_antrian_berikutnya_otomatis)  # Mengatur timer 5 menit
        self.timer.start()  # Memulai timer
        
    def panggil_antrian_berikutnya_otomatis(self):
        print(f"{self.nama_ruangan}: Antrian nomor {self.current} tidak hadir, lanjut ke antrian berikutnya.")
        self.panggil_antrian()
        self.panggil_antrian_dengan_suara()
        
    def hentikan_timer(self):
        if self.timer is not None:
            self.timer.cancel()  # Menghentikan timer jika ada
            self.timer = None
            print(f"Timer untuk {self.nama_ruangan} dihentikan.")

    def tampilkan_riwayat(self):
        print(f"Riwayat Panggilan untuk {self.nama_ruangan}:")
        for nomor, status in self.history:
            print(f"Nomor {nomor}: {status}")  # Menampilkan riwayat antrian

# Kelas SistemAntrian untuk menangani keseluruhan sistem antrian
class SistemAntrian:
    def __init__(self):
        self.ruangan = {
            "R01": Antrian("CTScan"),
            "R02": Antrian("MRI 1,5T"),
            "R03": Antrian("USG")
        }

    def tambah_antrian(self, kode_ruangan, nomor):
        if kode_ruangan in self.ruangan:
            self.ruangan[kode_ruangan].tambah_antrian(nomor)  # Menambahkan antrian ke ruangan yang sesuai

    def panggil_antrian_dan_suara(self, kode_ruangan):
        if kode_ruangan in self.ruangan:
            pesan = self.ruangan[kode_ruangan].panggil_antrian_dan_suara()  # Memanggil antrian dengan suara di ruangan yang sesuai
            print(pesan)

    def tampilkan_antrian(self):
        for kode_ruangan, antrian in self.ruangan.items():
            print(antrian)  # Menampilkan antrian untuk setiap ruangan
            
    def tampilkan_riwayat(self):
        for kode_ruangan, antrian in self.ruangan.items():
            antrian.tampilkan_riwayat()  # Menampilkan riwayat antrian untuk setiap ruangan

    def hentikan_timer(self, kode_ruangan):
        if kode_ruangan in self.ruangan:
            self.ruangan[kode_ruangan].hentikan_timer()  # Menghentikan timer untuk ruangan yang sesuai

    def pilih_tindakan(self):
        print("Pilih jenis tindakan:")
        print("1. CTScan (R01)")
        print("2. MRI 1,5T (R02)")
        print("3. USG (R03)")
        pilihan = input("Masukkan pilihan (1/2/3): ")
        if pilihan == "1":
            return "R01"
        elif pilihan == "2":
            return "R02"
        elif pilihan == "3":
            return "R03"
        else:
            print("Pilihan tidak valid.")
            return None
