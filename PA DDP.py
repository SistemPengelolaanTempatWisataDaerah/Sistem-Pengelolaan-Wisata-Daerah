import json
import os
import math
import time
import random
import hashlib
from datetime import datetime
from prettytable import PrettyTable
import pwinput


# ==================================================
# KONFIGURASI FILE
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILE_USER = os.path.join(BASE_DIR, "users.json")
FILE_WISATA = os.path.join(BASE_DIR, "wisata.json")
FILE_TRANSAKSI = os.path.join(BASE_DIR, "transaksi.json")
FOLDER_INVOICE = os.path.join(BASE_DIR, "invoice")

current_username = None
current_role = None

KATEGORI_WISATA = (
    "Wisata Alam",
    "Wisata Sejarah",
    "Wisata Budaya",
    "Wisata Religi",
    "Wisata Buatan"
)


# ==================================================
# UTILITAS
# ==================================================

def bersihkan_layar():
    """Membersihkan terminal sesuai sistem operasi."""
    os.system("cls" if os.name == "nt" else "clear")


def hash_password(password):
    """Mengubah password menjadi hash SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def baca_json(file):
    """Membaca file JSON dan mengembalikan list data."""
    if not os.path.exists(file):
        simpan_json(file, [])
        return []

    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data

        print("Format data harus berupa list!")
        return []

    except (json.JSONDecodeError, OSError) as error:
        print(f"Gagal membaca {os.path.basename(file)}: {error}")
        return []


def simpan_json(file, data):
    """Menyimpan data ke file JSON."""
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        return True

    except (OSError, TypeError) as error:
        print(f"Gagal menyimpan data: {error}")
        return False


def input_angka(pesan, minimum=0):
    """Membaca angka bulat dengan validasi."""
    while True:
        try:
            angka = int(input(pesan))

            if angka < minimum:
                print(f"Angka minimal adalah {minimum}!")
                continue

            return angka

        except ValueError:
            print("Input harus berupa angka!")


def konfirmasi(pesan):
    """Mengembalikan True jika pengguna menjawab y."""
    while True:
        jawaban = input(pesan + " (y/n): ").strip().lower()

        if jawaban == "y":
            return True

        if jawaban == "n":
            return False

        print("Masukkan y atau n!")


def jeda():
    """Memberi waktu sebelum kembali ke menu."""
    input("\nTekan Enter untuk melanjutkan...")


# ==================================================
# INISIALISASI DATA AWAL
# ==================================================

def inisialisasi_data():
    """Membuat file, akun admin, dan minimal lima wisata."""

    os.makedirs(FOLDER_INVOICE, exist_ok=True)

    users = baca_json(FILE_USER)
    wisata = baca_json(FILE_WISATA)
    baca_json(FILE_TRANSAKSI)

    # Menambahkan lima wisata contoh hanya jika data wisata kosong.
    if not wisata:
        wisata_awal = [
            {
                "id": 1,
                "nama": "Pulau Kumala",
                "lokasi": "Tenggarong",
                "kategori": "Wisata Buatan",
                "harga": 20000
            },
            {
                "id": 2,
                "nama": "Museum Mulawarman",
                "lokasi": "Tenggarong",
                "kategori": "Wisata Sejarah",
                "harga": 15000
            },
            {
                "id": 3,
                "nama": "Bukit Bangkirai",
                "lokasi": "Samboja",
                "kategori": "Wisata Alam",
                "harga": 25000
            },
            {
                "id": 4,
                "nama": "Desa Budaya Pampang",
                "lokasi": "Samarinda",
                "kategori": "Wisata Budaya",
                "harga": 10000
            },
            {
                "id": 5,
                "nama": "Masjid Islamic Center",
                "lokasi": "Samarinda",
                "kategori": "Wisata Religi",
                "harga": 0
            }
        ]

        if not simpan_json(FILE_WISATA, wisata_awal):
            print("Data wisata awal gagal disimpan.")
            return False

        print("Lima data wisata awal berhasil ditambahkan.")

    # Melengkapi akun lama tanpa mengganti password yang ada.
    users = baca_json(FILE_USER)
    perubahan = False

    for user in users:
        if "saldo" not in user:
            user["saldo"] = 0
            perubahan = True

        if user.get("role") not in ("admin", "user"):
            user["role"] = "user"
            perubahan = True

        # Mengenali password lama yang belum di-hash.
        password = user.get("password", "")
        if len(password) != 64:
            user["password"] = hash_password(password)
            perubahan = True

    if perubahan:
        if not simpan_json(FILE_USER, users):
            return False

    return True


# ==================================================
# REGISTRASI
# ==================================================

def registrasi():
    """Mendaftarkan akun User baru."""

    users = baca_json(FILE_USER)

    print("\n=== REGISTRASI USER ===")

    username = input("Username: ").strip()

    if len(username) < 4:
        print("Username minimal 4 karakter!")
        return False

    if any(user["username"] == username for user in users):
        print("Username sudah digunakan!")
        return False

    password = pwinput.pwinput("Password: ")

    if len(password) < 6:
        print("Password minimal 6 karakter!")
        return False

    konfirmasi_password = pwinput.pwinput("Konfirmasi password: ")

    if password != konfirmasi_password:
        print("Konfirmasi password tidak cocok!")
        return False

    # Registrasi umum hanya menghasilkan akun User.
    users.append({
        "username": username,
        "password": hash_password(password),
        "role": "user",
        "saldo": 0
    })

    if not simpan_json(FILE_USER, users):
        return False

    print("Registrasi berhasil! Role akun: User")
    return True


# ==================================================
# LOGIN
# ==================================================

def login():
    """Login dengan batas tiga kali percobaan."""

    global current_username, current_role

    users = baca_json(FILE_USER)

    print("\n=== LOGIN ===")

    for percobaan in range(3):
        username = input("Username: ").strip()
        password = pwinput.pwinput("Password: ")

        akun = next(
            (
                user for user in users
                if user["username"] == username
                and user["password"] == hash_password(password)
            ),
            None
        )

        if akun:
            current_username = akun["username"]
            current_role = akun["role"]

            print("\nLogin berhasil!")
            print("Selamat datang,", current_username)
            print("Role:", current_role)

            return True

        sisa = 2 - percobaan

        if sisa > 0:
            print(f"Login gagal! Sisa percobaan: {sisa}")
        else:
            print("Login gagal tiga kali. Silakan coba kembali nanti.")

        time.sleep(1)

    return False


def logout():
    """Mengakhiri sesi pengguna."""
    global current_username, current_role

    current_username = None
    current_role = None

    print("Logout berhasil!")


# ==================================================
# CRUD WISATA
# ==================================================

def tampilkan_wisata():
    """Menampilkan semua data wisata."""

    wisata = baca_json(FILE_WISATA)

    print("\n=== DAFTAR WISATA ===")

    if not wisata:
        print("Belum ada data wisata.")
        return []

    tabel = PrettyTable()
    tabel.field_names = [
        "ID",
        "Nama",
        "Lokasi",
        "Kategori",
        "Harga Tiket"
    ]

    for item in wisata:
        tabel.add_row([
            item["id"],
            item["nama"],
            item["lokasi"],
            item["kategori"],
            f"Rp{item['harga']:,}"
        ])

    print(tabel)
    return wisata


def pilih_kategori():
    """Memilih kategori wisata dari pilihan yang tersedia."""

    print("\n=== KATEGORI WISATA ===")

    for nomor, kategori in enumerate(KATEGORI_WISATA, start=1):
        print(f"{nomor}. {kategori}")

    pilihan = input_angka("Pilih kategori (1-5): ", 1)

    if pilihan > len(KATEGORI_WISATA):
        print("Kategori tidak tersedia!")
        return None

    return KATEGORI_WISATA[pilihan - 1]


def tambah_wisata():
    """Menambahkan data wisata. Khusus Admin."""

    if current_role != "admin":
        print("Akses ditolak!")
        return False

    wisata = baca_json(FILE_WISATA)

    print("\n=== TAMBAH WISATA ===")

    nama = input("Nama wisata: ").strip()
    lokasi = input("Lokasi: ").strip()

    if not nama or not lokasi:
        print("Nama dan lokasi wajib diisi!")
        return False

    kategori = pilih_kategori()

    if kategori is None:
        return False

    harga = input_angka("Harga tiket: Rp", 0)

    id_baru = max(
        [item["id"] for item in wisata],
        default=0
    ) + 1

    data_baru = {
        "id": id_baru,
        "nama": nama,
        "lokasi": lokasi,
        "kategori": kategori,
        "harga": harga
    }

    wisata.append(data_baru)

    if simpan_json(FILE_WISATA, wisata):
        print("Data wisata berhasil ditambahkan!")
        return True

    return False


def ubah_wisata():
    """Mengubah data wisata. Khusus Admin."""

    if current_role != "admin":
        print("Akses ditolak!")
        return False

    wisata = tampilkan_wisata()

    if not wisata:
        return False

    id_wisata = input_angka("ID wisata yang diubah: ", 1)

    item = next(
        (data for data in wisata if data["id"] == id_wisata),
        None
    )

    if item is None:
        print("Wisata tidak ditemukan!")
        return False

    print("Kosongkan input jika data tidak ingin diubah.")

    nama = input(f"Nama [{item['nama']}]: ").strip()
    lokasi = input(f"Lokasi [{item['lokasi']}]: ").strip()

    if nama:
        item["nama"] = nama

    if lokasi:
        item["lokasi"] = lokasi

    if konfirmasi("Ubah kategori?"):
        kategori = pilih_kategori()

        if kategori is not None:
            item["kategori"] = kategori

    harga = input(f"Harga tiket [{item['harga']}]: ").strip()

    if harga:
        try:
            harga_baru = int(harga)

            if harga_baru < 0:
                print("Harga tidak boleh negatif!")
                return False

            item["harga"] = harga_baru

        except ValueError:
            print("Harga harus berupa angka!")
            return False

    if simpan_json(FILE_WISATA, wisata):
        print("Data wisata berhasil diperbarui!")
        return True

    return False


def hapus_wisata():
    """Menghapus data wisata. Khusus Admin."""

    if current_role != "admin":
        print("Akses ditolak!")
        return False

    wisata = tampilkan_wisata()

    if not wisata:
        return False

    id_wisata = input_angka("ID wisata yang dihapus: ", 1)

    item = next(
        (data for data in wisata if data["id"] == id_wisata),
        None
    )

    if item is None:
        print("Wisata tidak ditemukan!")
        return False

    if not konfirmasi(f"Hapus wisata {item['nama']}?"):
        print("Penghapusan dibatalkan.")
        return False

    wisata.remove(item)

    if simpan_json(FILE_WISATA, wisata):
        print("Data wisata berhasil dihapus!")
        return True

    return False


# ==================================================
# DATA USER DAN SALDO
# ==================================================

def ambil_user(username=None):
    """Mengambil data akun berdasarkan username."""

    if username is None:
        username = current_username

    users = baca_json(FILE_USER)

    for user in users:
        if user["username"] == username:
            return user

    return None


def ubah_saldo(username, perubahan):
    """Mengubah saldo dan menolak saldo negatif."""

    users = baca_json(FILE_USER)

    for user in users:
        if user["username"] == username:
            saldo_baru = user.get("saldo", 0) + perubahan

            if saldo_baru < 0:
                print("Saldo tidak mencukupi!")
                return False

            user["saldo"] = saldo_baru

            if simpan_json(FILE_USER, users):
                return saldo_baru

            return False

    print("Akun tidak ditemukan!")
    return False


# ==================================================
# TRANSAKSI DAN INVOICE
# ==================================================

def buat_nomor_invoice(transaksi):
    """Membuat kode invoice unik."""

    while True:
        waktu = datetime.now().strftime("%Y%m%d%H%M%S")
        acak = random.randint(1000, 9999)
        nomor = f"INV-{waktu}-{acak}"

        if not any(t["invoice"] == nomor for t in transaksi):
            return nomor


def simpan_transaksi(data):
    """Menyimpan transaksi ke JSON dan mengembalikan status."""

    transaksi = baca_json(FILE_TRANSAKSI)
    data["id"] = max(
        [item.get("id", 0) for item in transaksi],
        default=0
    ) + 1

    data["invoice"] = buat_nomor_invoice(transaksi)

    transaksi.append(data)

    if simpan_json(FILE_TRANSAKSI, transaksi):
        return data

    return None


def cetak_invoice(data):
    """Menampilkan invoice dan menyimpannya ke file TXT."""

    baris = [
        "=" * 45,
        "             INVOICE TRANSAKSI",
        "       SISTEM PENGELOLAAN WISATA",
        "=" * 45,
        f"Nomor Invoice : {data['invoice']}",
        f"Tanggal       : {data['tanggal']}",
        f"Username      : {data['username']}",
        f"Jenis         : {data['jenis']}"
    ]

    if data["jenis"] == "PEMBELIAN TIKET":
        baris.extend([
            f"Wisata        : {data['wisata']}",
            f"Harga Satuan  : Rp{data['harga_satuan']:,}",
            f"Jumlah Tiket  : {data['jumlah_tiket']}"
        ])

    baris.extend([
        "-" * 45,
        f"Total         : Rp{data['total']:,}",
        f"Status        : {data['status']}",
        "=" * 45,
        "       Terima kasih telah bertransaksi!",
        "=" * 45
    ])

    isi_invoice = "\n".join(baris)

    print("\n" + isi_invoice)

    nama_file = os.path.join(
        FOLDER_INVOICE,
        f"{data['invoice']}.txt"
    )

    try:
        with open(nama_file, "w", encoding="utf-8") as f:
            f.write(isi_invoice)

        print("\nInvoice tersimpan:", nama_file)

    except OSError as error:
        print("Invoice gagal disimpan:", error)


def top_up():
    """Menambah saldo dan mencatat transaksi."""

    user = ambil_user()

    if user is None:
        print("Akun tidak ditemukan!")
        return False

    print("\n=== TOP UP SALDO ===")
    print(f"Saldo saat ini: Rp{user['saldo']:,}")

    nominal = input_angka("Nominal top up: Rp", 1)

    # Top up adalah simulasi untuk tugas.
    data_transaksi = {
        "username": current_username,
        "jenis": "TOP UP",
        "wisata": "-",
        "jumlah_tiket": 0,
        "harga_satuan": 0,
        "total": nominal,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "BERHASIL"
    }

    # Catat transaksi dahulu agar saldo tidak bertambah
    # jika penyimpanan transaksi gagal.
    hasil = simpan_transaksi(data_transaksi)

    if hasil is None:
        print("Transaksi gagal disimpan!")
        return False

    saldo_baru = ubah_saldo(current_username, nominal)

    if saldo_baru is False:
        print("Saldo gagal diperbarui. Hubungi Admin.")
        return False

    print(f"Top up berhasil! Saldo sekarang Rp{saldo_baru:,}")
    cetak_invoice(hasil)
    return True


def beli_tiket():
    """Membeli tiket wisata menggunakan saldo."""

    user = ambil_user()

    if user is None:
        print("Akun tidak ditemukan!")
        return False

    wisata = tampilkan_wisata()

    if not wisata:
        return False

    id_wisata = input_angka("ID wisata yang dibeli: ", 1)

    item = next(
        (data for data in wisata if data["id"] == id_wisata),
        None
    )

    if item is None:
        print("Wisata tidak ditemukan!")
        return False

    jumlah = input_angka("Jumlah tiket: ", 1)
    total = item["harga"] * jumlah

    print("\n=== RINCIAN PEMBELIAN ===")
    print("Wisata       :", item["nama"])
    print("Harga satuan :", f"Rp{item['harga']:,}")
    print("Jumlah tiket :", jumlah)
    print("Total        :", f"Rp{total:,}")
    print("Saldo        :", f"Rp{user['saldo']:,}")

    if user["saldo"] < total:
        print("Saldo tidak mencukupi! Silakan top up.")
        return False

    if not konfirmasi("Lanjutkan pembelian?"):
        print("Pembelian dibatalkan.")
        return False

    # Kurangi saldo terlebih dahulu.
    saldo_baru = ubah_saldo(current_username, -total)

    if saldo_baru is False:
        print("Pembayaran gagal.")
        return False

    data_transaksi = {
        "username": current_username,
        "jenis": "PEMBELIAN TIKET",
        "wisata": item["nama"],
        "jumlah_tiket": jumlah,
        "harga_satuan": item["harga"],
        "total": total,
        "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "BERHASIL"
    }

    hasil = simpan_transaksi(data_transaksi)

    if hasil is None:
        # Mengembalikan saldo jika transaksi gagal disimpan.
        ubah_saldo(current_username, total)
        print("Transaksi gagal disimpan. Saldo dikembalikan.")
        return False

    print(f"Pembelian berhasil! Sisa saldo Rp{saldo_baru:,}")
    cetak_invoice(hasil)
    return True


def riwayat_transaksi():
    """User melihat transaksinya sendiri."""

    transaksi = baca_json(FILE_TRANSAKSI)

    data_user = [
        item for item in transaksi
        if item["username"] == current_username
    ]

    tampilkan_riwayat(data_user)


def tampilkan_riwayat(transaksi):
    """Menampilkan daftar transaksi menggunakan tabel."""

    if not transaksi:
        print("Belum ada transaksi.")
        return

    tabel = PrettyTable()
    tabel.field_names = [
        "ID",
        "Invoice",
        "Username",
        "Jenis",
        "Wisata",
        "Total",
        "Tanggal",
        "Status"
    ]

    for item in transaksi:
        tabel.add_row([
            item.get("id", "-"),
            item.get("invoice", "-"),
            item.get("username", "-"),
            item.get("jenis", "-"),
            item.get("wisata", "-"),
            f"Rp{item.get('total', 0):,}",
            item.get("tanggal", "-"),
            item.get("status", "-")
        ])

    print(tabel)


def lihat_invoice():
    """Menampilkan kembali invoice milik User."""

    transaksi = baca_json(FILE_TRANSAKSI)

    data_user = [
        item for item in transaksi
        if item["username"] == current_username
    ]

    if not data_user:
        print("Belum ada transaksi.")
        return

    tampilkan_riwayat(data_user)

    nomor = input("\nMasukkan nomor invoice: ").strip()

    data = next(
        (
            item for item in data_user
            if item.get("invoice") == nomor
        ),
        None
    )

    if data is None:
        print("Invoice tidak ditemukan!")
        return

    cetak_invoice(data)


# ==================================================
# FITUR ADMIN: RIWAYAT DAN LAPORAN
# ==================================================

def semua_riwayat_transaksi():
    """Admin melihat semua riwayat transaksi."""

    if current_role != "admin":
        print("Akses ditolak!")
        return

    transaksi = baca_json(FILE_TRANSAKSI)

    print("\n=== SELURUH RIWAYAT TRANSAKSI ===")
    tampilkan_riwayat(transaksi)


def laporan_admin():
    """Meringkas transaksi dan penjualan tiket."""

    if current_role != "admin":
        print("Akses ditolak!")
        return

    transaksi = baca_json(FILE_TRANSAKSI)

    pembelian = [
        item for item in transaksi
        if item.get("jenis") == "PEMBELIAN TIKET"
        and item.get("status") == "BERHASIL"
    ]

    total_pendapatan = sum(
        item.get("total", 0) for item in pembelian
    )

    jumlah_transaksi = len(transaksi)

    tiket_terjual = {}

    for item in pembelian:
        nama = item.get("wisata", "-")
        jumlah = item.get("jumlah_tiket", 0)

        tiket_terjual[nama] = tiket_terjual.get(nama, 0) + jumlah

    wisata_terlaris = "-"

    if tiket_terjual:
        wisata_terlaris = max(
            tiket_terjual,
            key=tiket_terjual.get
        )

    print("\n=== LAPORAN RINGKAS ADMIN ===")
    print("Total pendapatan tiket :", f"Rp{total_pendapatan:,}")
    print("Jumlah seluruh transaksi:", jumlah_transaksi)
    print("Jumlah pembelian tiket :", len(pembelian))
    print("Wisata terlaris         :", wisata_terlaris)

    if wisata_terlaris != "-":
        print(
            "Jumlah tiket terjual   :",
            tiket_terjual[wisata_terlaris]
        )


# ==================================================
# MENU ADMIN
# ==================================================

def menu_admin():
    while True:
        bersihkan_layar()

        print("=" * 42)
        print(" SISTEM PENGELOLAAN WISATA - ADMIN")
        print("=" * 42)
        print("1. Lihat daftar wisata")
        print("2. Tambah wisata")
        print("3. Ubah wisata")
        print("4. Hapus wisata")
        print("5. Seluruh riwayat transaksi")
        print("6. Laporan ringkas")
        print("7. Logout")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            tampilkan_wisata()
            jeda()

        elif pilihan == "2":
            tambah_wisata()
            jeda()

        elif pilihan == "3":
            ubah_wisata()
            jeda()

        elif pilihan == "4":
            hapus_wisata()
            jeda()

        elif pilihan == "5":
            semua_riwayat_transaksi()
            jeda()

        elif pilihan == "6":
            laporan_admin()
            jeda()

        elif pilihan == "7":
            logout()
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# MENU USER
# ==================================================

def menu_user():
    while True:
        bersihkan_layar()

        user = ambil_user()

        if user is None:
            print("Akun tidak ditemukan.")
            logout()
            break

        print("=" * 42)
        print(" SISTEM PENGELOLAAN WISATA - USER")
        print("=" * 42)
        print("Username:", current_username)
        print("Saldo:", f"Rp{user['saldo']:,}")
        print("------------------------------------------")
        print("1. Lihat daftar wisata")
        print("2. Top up saldo")
        print("3. Beli tiket wisata")
        print("4. Riwayat transaksi")
        print("5. Lihat invoice")
        print("6. Logout")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            tampilkan_wisata()
            jeda()

        elif pilihan == "2":
            top_up()
            jeda()

        elif pilihan == "3":
            beli_tiket()
            jeda()

        elif pilihan == "4":
            riwayat_transaksi()
            jeda()

        elif pilihan == "5":
            lihat_invoice()
            jeda()

        elif pilihan == "6":
            logout()
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# PROGRAM UTAMA
# ==================================================

def main():
    if not inisialisasi_data():
        print("Inisialisasi gagal. Periksa file dan folder program.")
        return

    while True:
        bersihkan_layar()

        print("=" * 42)
        print(" SISTEM PENGELOLAAN WISATA DAERAH")
        print("=" * 42)
        print("1. Registrasi User")
        print("2. Login")
        print("3. Keluar")

        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            registrasi()
            jeda()

        elif pilihan == "2":
            if login():
                if current_role == "admin":
                    menu_admin()
                else:
                    menu_user()

        elif pilihan == "3":
            print("Terima kasih telah menggunakan program.")
            break

        else:
            print("Pilihan tidak valid!")
            jeda()


# ==================================================
# MENJALANKAN PROGRAM
# ==================================================

if __name__ == "__main__":
    try:
        main()

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")

    except Exception as error:
        print(f"\nTerjadi kesalahan yang belum ditangani: {error}")
users = baca_json(FILE_USER)

