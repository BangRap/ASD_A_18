import csv
import tabulate
import datetime

FILE_NAME = "kamar.csv"

# ================= DATA GLOBAL =================
data = []             # List utama untuk nampung data dari CSV (buat jembatan)
history_stack = []   # Stack untuk menyimpan riwayat data sebelum perubahan, dipakai untuk fitur undo
log_aktivitas= []    # List untuk menyimpan catatan aktivitas user selama program berjalan


# ================= FILE HANDLING =================

def load_data():
    '''
    Ini fungsi buat ngeload data
    '''
    
    data = []   # Membuat list kosong untuk menampung data dari file CSV

    try: # Mencoba membuka file CSV
        # Buka file CSV dengan mode read (r)
        with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            # Membaca isi CSV sebagai dictionary
            
            for row in reader:  # Melakukan looping untuk setiap baris data di CSV
                data.append(row) # Menambahkan setiap baris data ke dalam list data


    except FileNotFoundError:  # Jika file kamar.csv belum ada, program tidak crash
        pass    # Program lanjut berjalan tanpa melakukan apa-apa

    return data  # Mengembalikan data dari CSV ke program


def save_data(data):
    '''
    Ini fungsi buat ngesave data
    '''

    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:    # Membuka file kamar.csv dalam mode write/tulis, Jika file belum ada, maka akan dibuat otomatis, Jika sudah ada, isi lama akan ditimpa dengan data terbaru
        fieldnames = ["nomor", "lantai", "harga", "status", "penghuni", "tanggal_mulai", "tagihan"] # Menentukan nama kolom yang akan dipakai di file CSV
        writer = csv.DictWriter(file, fieldnames=fieldnames)  # Membuat writer CSV berbasis dictionary
        writer.writeheader()  # menulis header kolom di baris pertama CSV
        writer.writerows(data) # menulis seluruh data list kamar ke file CSV


def import_csv(sll): 
    '''
    Ini fungsi buat import csv
    '''

    global data  # Menggunakan variabel data global agar data utama bisa diganti
    nama_file = input("Masukkan nama file CSV: ")   # User memasukkan nama file CSV yang ingin diimpor

    try:
        with open(nama_file, mode='r', newline='', encoding='utf-8') as file: # Membuka file CSV yang dimasukkan user
            reader = csv.DictReader(file)  # Membaca isi file sebagai dictionary
            data = []  # Mengosongkan data lama sebelum diganti data baru
            for row in reader:
                data.append(row)  # Memasukkan setiap baris CSV ke list data

        save_data(data)  # Menyimpan data hasil import ke file utama kamar.csv
        sll.rebuild(data)  # Membangun ulang linked list berdasarkan data baru

        print("Import CSV berhasil!")

    except FileNotFoundError:   # Jika nama file tidak ditemukan
        print("File tidak ditemukan!") # Cetak File tidak ditemukan!


# ================= LINKED LIST =================

class Node:  # Class Node adalah elemen dasar dari linked list
    def __init__(self, data):     # Constructor yang dijalankan saat node dibuat
        self.data = data      # Menyimpan data kamar di dalam node
        self.next = None      # Menyimpan referensi ke node berikutnya, walnya None karena belum tersambung ke node lain


class SingleLinkedList: # Class untuk membuat struktur data Single Linked List
    def __init__(self): 
        self.head = None  # Head adalah node pertama dalam linked list, awalnya None karena linked list masih kosong

    def tambah_kamar(self, kamar):
        '''
        Ini fungsi buat masukin kamar ke linkedlist
        '''
        
        new_node = Node(kamar)        # Membuat node baru berisi data kamar
        if not self.head:             # Jika linked list masih kosong
            self.head = new_node      # Node baru langsung menjadi head
            return                    # Keluar dari fungsi karena data sudah ditambahkan
        temp = self.head              # Mulai penelusuran dari node pertama
        while temp.next:              # Selama masih ada node berikutnya
            temp = temp.next          # Geser temp ke node berikutnya
        temp.next = new_node          # Setelah sampai node terakhir, sambungkan node baru di bagian akhir

    def rebuild(self, data):
        '''
        Fungsi buat ngebangun ulang linked list dari list data
        '''
        
        self.head = None   # Mengosongkan linked list terlebih dahulu
        for kamar in data:  # Loop semua data kamar dari list
            self.tambah_kamar(kamar)   # Masukkan satu per satu ke linked list

    # --- FITUR BARU: Konversi SLL ke List (Untuk Save ke CSV) ---
    def to_list(self):   
        '''
        Fungsi buat ngubah linked list ke list biasa
        '''
        
        hasil_list = []   # List kosong untuk menampung hasil konversi
        temp = self.head   # Mulai dari node pertama
        while temp:   # Selama node masih ada
            hasil_list.append(temp.data)   # Ambil data dari node lalu masukkan ke list
            temp = temp.next   # Pindah ke node berikutnya
        return hasil_list  # Mengembalikan hasil linked list dalam bentuk list

    # --- FITUR BARU: Hapus Node Asli SLL ---
    def hapus_node_by_nomor(self, nomor_cari):   
        '''
        untuk ngehapus node berdasarkan nomor kamar
        '''
        
        temp = self.head # Mulai dari node pertama
        prev = None  # prev digunakan untuk menyimpan node sebelumnya

        if temp is not None and temp.data["nomor"] == nomor_cari:   # Jika linked list tidak kosong dan node pertama adalah data yang dicari
            self.head = temp.next  # Head dipindahkan ke node berikutnya, sehingga node pertama terhapus
            return True  # Mengembalikan True karena data berhasil dihapus

        # Cari node di tengah/akhir
        while temp is not None and temp.data["nomor"] != nomor_cari:  # Selama node belum habis dan nomor kamar belum ditemukan
            prev = temp  # Simpan node sekarang sebagai node sebelumnya
            temp = temp.next # Geser ke node berikutnya

        if temp is not None:  # Jika data ditemukan
            prev.next = temp.next  # Node sebelumnya disambungkan ke node setelah data yang dihapus
            return True   # Mengembalikan True karena data berhasil dihapus
            
        return False # Jika tidak ketemu, kembalikan False

    # --- FITUR BARU: BUBBLE SORT PADA LINKED LIST ---
    def urutkan_kamar(self): 
        '''
        fungsi buat mengurutkan kamar memakai Bubble Sort pada linked list
        '''
        
        if not self.head or not self.head.next: # Jika linked list kosong atau cuma punya satu node
            return # Tidak perlu sorting

        diurutkan = True # Variabel penanda apakah masih ada pertukaran data
        while diurutkan:  # Selama masih ada data yang ditukar
            diurutkan = False  # Dianggap sudah urut dulu
            temp = self.head   # Mulai pengecekan dari node pertama
            
            # Telusuri SLL sampai node sebelum terakhir
            while temp.next is not None:    # Selama masih ada node setelah temp

                if int(temp.data["nomor"]) > int(temp.next.data["nomor"]): # Jika nomor kamar node sekarang lebih besar dari node berikutnya
                    temp.data, temp.next.data = temp.next.data, temp.data   # Tukar isi data antar node
                    diurutkan = True   # Tandai bahwa masih ada pertukaran
                
                temp = temp.next # Geser ke node berikutnya
        
# ================= NEW FITUR (SEARCH & HISTORY) ====================

#--- Search ---
def cari_kamar(sll): # <-- Selalu ada tambahan parameter 'sll' di sini
    '''
    fungsi buat cari kamar
    '''
    
    keyword = input("Masukkan nomor kamar atau nama penghuni yang ingin dicari: ").lower()
    
    hasil = []
    temp = sll.head # Mulai penelusuran dari Kepala (Head) Linked List
    
    # Looping di linked list
    while temp is not None:
        if keyword in temp.data['nomor'].lower() or keyword in temp.data['penghuni'].lower():
            hasil.append(temp.data)
        temp = temp.next # Jalan ke node berikutnya
    
    print("\n=================== Hasil Pencarian ===================")
    if not hasil: #buat kalo pencariannya kosong
        print("Data yang kamu cari tidak ditemukan")
    else: #atur hasil pencariannya disini
        headers = {
            "nomor": "\033[1mNomor\033[0m",
            "lantai": "\033[1mLantai\033[0m",
            "harga": "\033[1mHarga\033[0m",
            "status": "\033[1mStatus\033[0m",
            "penghuni": "\033[1mPenghuni\033[0m",
            "tanggal_mulai": "\033[1mTanggal Mulai\033[0m",
            "tagihan": "\033[1mTagihan (Rp)\033[0m"
        }
        print(tabulate.tabulate(hasil, headers=headers, tablefmt="rounded_grid")) #disini buat ngerapihin dan membuat jadi tabel
        
#--- History ----
def lihat_history():
    '''
    fungsi buat ngelihat history ngedit data
    '''
    
    print("\n==== RIWAYAT AKTIVITAS ====")
    if not log_aktivitas: #buat Kalo aktivitasnya kosong
        print("Belum ada riwayat aktivitas")
    else: #Disini atur hasil aktivitas
        for i, log in enumerate(log_aktivitas, 1):
            print(f"{i}.{log}")


# ================= CRUD =================

def sort_kamar(sll):
    '''
    fungsi buat mengurutkan data kamar kost
    '''
    global data
    
    if not sll.head: #Buat ngecek linkedlistnya kosong apa engga
        print("\n Data kosong, tidak ada yang bisa diurutkan!")
        return

    print("\nSedang mengurutkan kamar berdasarkan nomor...")
    
    sll.urutkan_kamar() # buat jalanin algoritma Bubble Sort di dalam SLL
    

    data = sll.to_list() # Buat singkronin ke list global abis diurutin
    
    save_data(data) #buat nyimpen data ke csv
    log_aktivitas.append("Mengurutkan daftar kamar berdasarkan nomor")
    
    print(" Kamar berhasil diurutkan dari nomor terkecil ke terbesar!")
    
    # Hasil sorting
    headers = {
        "nomor": "\033[1mNomor\033[0m",
        "lantai": "\033[1mLantai\033[0m",
        "harga": "\033[1mHarga\033[0m",
        "status": "\033[1mStatus\033[0m",
        "penghuni": "\033[1mPenghuni\033[0m",
        "tanggal_mulai": "\033[1mTanggal Mulai\033[0m",
        "tagihan": "\033[1mTagihan (Rp)\033[0m"
    }
    print("\n===================== DATA KAMAR (TERURUT) ======================")
    print(tabulate.tabulate(data, headers=headers, tablefmt="rounded_grid"))


def tambah_kamar(sll):
    '''
    fungsi buat nambah kamar
    '''
    global data
    nomor = input("Nomor kamar: ")
    
# ============= Validasi Nomer ===========
    temp = sll.head # dicek dulu dari head linked list
    while temp is not None:
        if temp.data["nomor"] == nomor:
            print(f"\n Error: Kamar nomor {nomor} sudah ada! Silahkan input nomor kamar yang lain.")
            return # disini langsung keluar dari fungsi, tidak jadi menambahkan data kamar karna sudah terinput
        temp = temp.next # geser ke node berikutnya
# ==========================================================
    lantai = input("Lantai: ")
    harga = input("Harga: ")
    status = input("Status (Terisi/Kosong): ").capitalize()

    if status.lower() == "kosong":
        # Jika kamar kosong, skip penghuni, tanggal_mulai, dan tagihan
        penghuni = ""
        tanggal_mulai = ""
        tagihan = ""
        print("Status Kosong: penghuni, tanggal mulai, dan tagihan dikosongkan otomatis.")
    else:
        penghuni = input("Penghuni: ")

        # Validasi input tagihan: harus berupa angka
        while True:
            tagihan_input = input("Tagihan pembayaran (Rp): ")
            if tagihan_input.isdigit():
                tagihan = tagihan_input
                break
            else:
                print(" Error: Tagihan harus berupa angka! Coba lagi.")

        # Tanggal mulai diisi otomatis dari datetime saat data diinput, bukan dari user
        tanggal_mulai = datetime.datetime.now().strftime("%Y-%m-%d ")

    kamar = {
        "nomor": nomor,
        "lantai": lantai,
        "harga": harga,
        "status": status,
        "penghuni": penghuni,
        "tanggal_mulai": tanggal_mulai,
        "tagihan": tagihan
    }

    history_stack.append([d.copy() for d in data]) #Simpen state data sebelum ditambah (buat undo)

    data.append(kamar)
    log_aktivitas.append(f"Menambahkan kamar nomor {nomor}")
    save_data(data)
    sll.tambah_kamar(kamar)

    if tanggal_mulai:
        print(f"Kamar berhasil ditambahkan! (Tanggal mulai: {tanggal_mulai})")
    else:
        print("Kamar berhasil ditambahkan!")


def lihat_kamar():
    '''
    fungsi buat lihat data kamar kost
    '''
    
    global data

    if not data: #Ngecek data kosong apa engga
        print("Data kosong")
        return

    headers = {
        "nomor": "\033[1mNomor\033[0m",
        "lantai": "\033[1mLantai\033[0m",
        "harga": "\033[1mHarga\033[0m",
        "status": "\033[1mStatus\033[0m",
        "penghuni": "\033[1mPenghuni\033[0m",
        "tanggal_mulai": "\033[1mTanggal Mulai\033[0m",
        "tagihan": "\033[1mTagihan (Rp)\033[0m"
    }

    pilihan = input("Lihat semua kamar atau berdasarkan filter? (semua/filter): ").lower()

    # ini if else buat milih lihat semua kamar atau ngefilter
    if pilihan == "semua":
        tampil = data

    elif pilihan == "filter":
        print("""
Filter berdasarkan:
1. Lantai
2. Harga
3. Status
""")
        jenis_filter = input("Pilih filter (1/2/3): ")

        tampil = []

        # Disini buat if else filter kamar
        if jenis_filter == "1":
            lantai = input("Masukkan lantai (1/2): ")
            tampil = [k for k in data if k["lantai"] == lantai]

        elif jenis_filter == "2":
            harga = input("Masukkan harga yang dicari: ")
            tampil = [k for k in data if k["harga"] == harga]

        elif jenis_filter == "3":
            status = input("Masukkan status (Terisi/Kosong): ").capitalize()
            tampil = [k for k in data if k["status"].lower() == status.lower()]

        else:
            print("Pilihan filter tidak valid!")
            return

        if not tampil:
            print("Tidak ada kamar yang dicari.")
            return

    else:
        print("Pilihan tidak valid!")
        return

    print("\n===================== DATA KAMAR ======================")
    print(tabulate.tabulate(tampil, headers=headers, tablefmt="rounded_grid"))

def update_kamar(sll):
    '''
    fungsi buat ngeupdate data kamar kost
    '''
    global data

    nomor_cari = input("Masukkan Nomor kamar yang mau diupdate: ")

    temp = sll.head #ini dari head SLL dulu
    
    while temp is not None:
        if temp.data["nomor"] == nomor_cari:
            # Simpan state lama ke stack sebelum data diubah (untuk Undo)
            history_stack.append([d.copy() for d in data])
            
            print("""
Pilih yang ingin diupdate:
1. Status & Penghuni
2. Tagihan
3. Harga
""")
            pilih_update = input("Pilihan (1/2/3/4): ")

            if pilih_update == "1":
                # Status ditanya duluan, penghuni menyesuaikan
                status_baru = input("Status baru (Terisi/Kosong): ").capitalize()
                if status_baru.lower() == "kosong":
                    log_aktivitas.append(f"Update kamar {nomor_cari}: status -> Kosong, penghuni '{temp.data['penghuni']}' dikosongkan")
                    temp.data["status"] = "Kosong"
                    temp.data["penghuni"] = ""
                    temp.data["tanggal_mulai"] = ""
                else:
                    penghuni_baru = input("Nama penghuni baru: ")
                    tanggal_mulai_baru = datetime.datetime.now().strftime("%Y-%m-%d ")
                    log_aktivitas.append(f"Update kamar {nomor_cari}: status -> {status_baru}, penghuni {temp.data['penghuni']} -> {penghuni_baru}")
                    temp.data["status"] = status_baru
                    temp.data["penghuni"] = penghuni_baru
                    temp.data["tanggal_mulai"] = tanggal_mulai_baru

            elif pilih_update == "2":
                while True:
                    tagihan_baru = input("Tagihan pembayaran baru (Rp): ")
                    if tagihan_baru.isdigit():
                        break
                    else:
                        print(" Error: Tagihan harus berupa angka! Coba lagi.")
                log_aktivitas.append(f"Update kamar {nomor_cari}: tagihan {temp.data.get('tagihan', '-')} -> {tagihan_baru}")
                temp.data["tagihan"] = tagihan_baru

            elif pilih_update == "3":
                while True:
                    harga_baru = input("Harga baru (Rp): ")
                    if harga_baru.isdigit():
                        break
                    else:
                        print(" Error: Harga harus berupa angka! Coba lagi.")
                log_aktivitas.append(f"Update kamar {nomor_cari}: harga {temp.data.get('harga', '-')} -> {harga_baru}")
                temp.data["harga"] = harga_baru

            else:
                print("Pilihan tidak valid! Update dibatalkan.")
                history_stack.pop()  # Batalkan undo yang sudah disimpan
                return

            # 3. Sinkronkan ke list global dan simpan ke CSV
            data = sll.to_list()
            save_data(data)

            print("Data berhasil diupdate langsung di Linked List!")
            return
        
        temp = temp.next # Pindah ke kamar berikutnya

    print("Nomor kamar tidak ditemukan!")


def hapus_kamar(sll):
    '''
    fungsi buat ngehapus data kamar kost
    '''
    
    global data
    nomor_cari = input("Masukkan Nomor kamar yang dihapus: ")

    # 1. Simpan riwayat untuk Undo (WAJIB sebelum diubah)
    history_stack.append([d.copy() for d in data])

    # 2. Lakukan penghapusan murni menggunakan Linked List
    berhasil_hapus = sll.hapus_node_by_nomor(nomor_cari)

    if berhasil_hapus:
        log_aktivitas.append(f"Menghapus kamar nomor {nomor_cari}")
        
        # 3. Sinkronkan global data dengan kondisi SLL yang baru
        data = sll.to_list() 
        
        # 4. Save ke CSV
        save_data(data)
        print("Data berhasil dihapus dari Linked List!")
    else:
        # Jika tidak ketemu, batalkan undo yang tadi disimpan
        history_stack.pop() 
        print("Nomor kamar tidak ditemukan!")


# ================= STACK UNDO =================

def undo(sll):
    '''
    fungsi buat ngeundo perubahan data
    '''
    
    global data

    if history_stack:
        #Perbaikan: pop data terakhir dari stack
        data = history_stack.pop()
        log_aktivitas.append("Melakukan Undo")
        save_data(data)
        sll.rebuild(data)

        print("Undo berhasil!")

    else:
        print("Tidak ada riwayat untuk undo.")


# ================= MENU =================

def menu():
    '''
    fungsi output menu program
    '''
    
    global data

    data = load_data()

    sll = SingleLinkedList()
    sll.rebuild(data)

    while True:
        print("""
===== MENU APLIKASI =====
1. Tambah Kamar
2. Lihat Semua Kamar
3. Cari Kamar (No/Penghuni)
4. Update Kamar (Nomor)
5. Hapus Kamar (Nomor)
6. Lihat Riwayat
7. Undo
8. Urutkan Kamar (Bubble Sort)
0. Keluar
""")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_kamar(sll)

        elif pilih == "2":
            lihat_kamar()
        
        elif pilih == "3":
            cari_kamar(sll)

        elif pilih == "4":
            update_kamar(sll)

        elif pilih == "5":
            hapus_kamar(sll)

        elif pilih == "6":
            lihat_history()
            
        elif pilih == "7":
            undo(sll)
            
        elif pilih == "8":
            sort_kamar(sll)

        elif pilih == "0":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid!")


# ================= RUN =================
if __name__ == "__main__":   # Mengecek apakah file ini dijalankan langsung
    menu()   # Memanggil fungsi menu untuk menjalankan program
