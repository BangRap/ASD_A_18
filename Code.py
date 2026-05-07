import csv

FILE_NAME = "kamar.csv"

# ================= DATA GLOBAL =================
data = []
history_stack = []


# ================= FILE HANDLING =================

def load_data():
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
        fieldnames = ["id", "nomor", "lantai", "harga", "status", "penghuni"]

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

    def display(self):
        temp = self.head

        if not temp:
            print("Linked List kosong")
            return

        while temp:
            print(temp.data, end=" -> ")
            temp = temp.next

        print("NULL")


# ================= CRUD =================

def tambah_kamar(sll):
    global data

    id = input("ID: ")
    nomor = input("Nomor kamar: ")
    lantai = input("Lantai: ")
    harga = input("Harga: ")
    status = input("Status: ")
    penghuni = input("Penghuni: ")

    kamar = {
        "id": id,
        "nomor": nomor,
        "lantai": lantai,
        "harga": harga,
        "status": status,
        "penghuni": penghuni
    }

    history_stack.append(data.copy())

    data.append(kamar)
    save_data(data)
    sll.tambah_kamar(kamar)

    print("Kamar berhasil ditambahkan!")


def lihat_kamar():
    global data

    if not data:
        print("Data kosong")
        return

    print("\n===== DATA KAMAR =====")

    for kamar in data:
        print(f"""
ID       : {kamar['id']}
Nomor    : {kamar['nomor']}
Lantai   : {kamar['lantai']}
Harga    : {kamar['harga']}
Status   : {kamar['status']}
Penghuni : {kamar['penghuni']}
------------------------
""")


def update_kamar(sll):
    global data

    id_kamar = input("Masukkan ID kamar: ")

    for kamar in data:
        if kamar["id"] == id_kamar:
            history_stack.append(data.copy())

            kamar["penghuni"] = input("Nama penghuni baru: ")
            kamar["status"] = "Terisi"

            save_data(data)
            sll.rebuild(data)

            print("Data berhasil diupdate!")
            return

    print("ID tidak ditemukan!")


def hapus_kamar(sll):
    global data

    id_kamar = input("Masukkan ID kamar: ")

    for kamar in data:
        if kamar["id"] == id_kamar:
            history_stack.append(data.copy())

            data.remove(kamar)

            save_data(data)
            sll.rebuild(data)

            print("Data berhasil dihapus!")
            return

    print("ID tidak ditemukan!")


# ================= STACK UNDO =================

def undo(sll):
    global data

    if history_stack:
        data = history_stack.pop()

        save_data(data)
        sll.rebuild(data)

        print("Undo berhasil!")

    else:
        print("Tidak ada riwayat.")


# ================= MENU =================

def menu():
    global data

    data = load_data()

    sll = SingleLinkedList()
    sll.rebuild(data)

    while True:
        print("""
===== MENU KAMAR =====
1. Tambah Kamar
2. Lihat Kamar
3. Update Kamar
4. Hapus Kamar
5. Undo
0. Keluar
""")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_kamar(sll)

        elif pilih == "2":
            lihat_kamar()

        elif pilih == "3":
            update_kamar(sll)

        elif pilih == "4":
            hapus_kamar(sll)

        elif pilih == "5":
            undo(sll)

    

        elif pilih == "0":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid!")


# ================= RUN =================

menu()