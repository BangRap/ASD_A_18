import csv
import tabulate

FILE_NAME = "kamar.csv"

# ================= DATA GLOBAL =================
data = []
history_stack = []
log_aktivitas= []

# ================= FILE HANDLING =================

def load_data():
    temp_data = [] # variabel lokal dulu
    data = []

    try:
        with open(FILE_NAME, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                data.append(row)

    except FileNotFoundError:
        pass

    return data


def save_data(data):
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["nomor", "lantai", "harga", "status", "penghuni"]
        # Update hapus id dari fieldnames biar ga muncul di CSV
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def import_csv(sll):
    global data

    nama_file = input("Masukkan nama file CSV: ")

    try:
        with open(nama_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            data = []
            for row in reader:
                data.append(row)

        save_data(data)
        sll.rebuild(data)

        print("Import CSV berhasil!")

    except FileNotFoundError:
        print("File tidak ditemukan!")


# ================= LINKED LIST =================

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SingleLinkedList:
    def __init__(self):
        self.head = None

    def tambah_kamar(self, kamar):
        new_node = Node(kamar)
        if not self.head:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    def rebuild(self, data):
        self.head = None
        for kamar in data:
            self.tambah_kamar(kamar)

    # --- FITUR BARU: Konversi SLL ke List (Untuk Save ke CSV) ---
    def to_list(self):
        hasil_list = []
        temp = self.head
        while temp:
            hasil_list.append(temp.data)
            temp = temp.next
        return hasil_list

    # --- FITUR BARU: Hapus Node Asli SLL ---
    def hapus_node_by_nomor(self, nomor_cari):
        temp = self.head
        prev = None

        # Jika yang dihapus adalah node pertama (head)
        if temp is not None and temp.data["nomor"] == nomor_cari:
            self.head = temp.next # Putus rantai head
            return True

        # Cari node di tengah/akhir
        while temp is not None and temp.data["nomor"] != nomor_cari:
            prev = temp
            temp = temp.next

        # Jika ketemu, putus rantainya dari node sebelumnya
        if temp is not None:
            prev.next = temp.next
            return True
            
        return False # Jika tidak ketemu
        
# ================= NEW FITUR (SEARCH & HISTORY) ====================

#--- Search ---
def cari_kamar(sll): # <-- Ingat ada tambahan parameter 'sll' di sini
    keyword = input("Masukkan nomor kamar atau nama penghuni yang ingin dicari: ").lower()
    
    hasil = []
    temp = sll.head # Mulai penelusuran dari Kepala (Head) Linked List
    
    # Looping ala Linked List Sejati
    while temp is not None:
        if keyword in temp.data['nomor'].lower() or keyword in temp.data['penghuni'].lower():
            hasil.append(temp.data)
        temp = temp.next # Jalan ke node berikutnya
    
    print("\n=================== Hasil Pencarian ===================")
    if not hasil:
        print("Data yang kamu cari tidak ditemukan")
    else:
        headers = {
            "nomor": "\033[1mNomor\033[0m",
            "lantai": "\033[1mLantai\033[0m",
            "harga": "\033[1mHarga\033[0m",
            "status": "\033[1mStatus\033[0m",
            "penghuni": "\033[1mPenghuni\033[0m"
        }
        print(tabulate.tabulate(hasil, headers=headers, tablefmt="rounded_grid"))
        
#--- History ----
def lihat_history():
    print("\n==== RIWAYAT AKTIVITAS ====")
    if not log_aktivitas:
        print("Belum ada riwayat aktivitas")
    else:
        for i, log in enumerate(log_aktivitas, 1):
            print(f"{i}.{log}")

# ================= CRUD =================

def tambah_kamar(sll):
    global data
    nomor = input("Nomor kamar: ")
    lantai = input("Lantai: ")
    harga = input("Harga: ")
    status = input("Status: ")
    penghuni = input("Penghuni: ")

    kamar = {
        "nomor": nomor,
        "lantai": lantai,
        "harga": harga,
        "status": status,
        "penghuni": penghuni
    }

    history_stack.append([d.copy() for d in data]) #Simpen state data sebelum ditambah (buat undo)

    data.append(kamar)
    log_aktivitas.append(f"Menambahkan kamar nomor {nomor}")
    save_data(data)
    sll.tambah_kamar(kamar)

    print("Kamar berhasil ditambahkan!")


def lihat_kamar():
    global data

    if not data:
        print("Data kosong")
        return

    headers = {
        "nomor": "\033[1mNomor\033[0m",
        "lantai": "\033[1mLantai\033[0m",
        "harga": "\033[1mHarga\033[0m",
        "status": "\033[1mStatus\033[0m",
        "penghuni": "\033[1mPenghuni\033[0m"
    }

    pilihan = input("Lihat semua kamar atau berdasarkan filter? (semua/filter): ").lower()

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
    global data

    nomor_cari = input("Masukkan Nomor kamar yang mau diupdate: ")

    for kamar in data:
        if kamar["nomor"] == nomor_cari:
            history_stack.append([d.copy() for d in data])
            
            penghuni_baru = input("Nama penghuni baru: ")
            log_aktivitas.append(f"Update kamar {nomor_cari}: {kamar['penghuni']} -> {penghuni_baru}")

            #Perbaikan: Langsung masukin variabel penghuni baru
            kamar["penghuni"] = penghuni_baru
            kamar["status"] = "Terisi"

            save_data(data)
            sll.rebuild(data)

            print("Data berhasil diupdate!")
            return

    print("Nomor kamar tidak ditemukan!")


def hapus_kamar(sll):
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

        elif pilih == "0":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid!")


# ================= RUN =================
if __name__ == "__main__":
    menu()
