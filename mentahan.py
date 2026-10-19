import json
import os
import math
from prettytable import PrettyTable
import pwinput

FILE_USER = "users.json"
FILE_WISATA = "wisata.json"


# =========================
# FUNGSI FILE JSON
# =========================

def baca_json(file):
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
        return []

    try:
        with open(file, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def simpan_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


# =========================
# REGISTRASI
# =========================

def registrasi():
    users = baca_json(FILE_USER)

    print("\n=== REGISTRASI ===")

    username = input("Username : ").strip()

    if not username:
        print("Username tidak boleh kosong!")
        return

    for user in users:
        if user["username"] == username:
            print("Username sudah digunakan!")
            return

    password = pwinput.pwinput("Password : ")

    if len(password) < 6:
        print("Password minimal 6 karakter!")
        return

    users.append({
        "username": username,
        "password": password
    })

    simpan_json(FILE_USER, users)

    print("Registrasi berhasil!")


# =========================
# LOGIN
# =========================

def login():
    users = baca_json(FILE_USER)

    print("\n=== LOGIN ===")

    username = input("Username : ").strip()
    password = pwinput.pwinput("Password : ")

    for user in users:
        if (
            user["username"] == username
            and user["password"] == password
        ):
            print("Login berhasil!")
            print("Selamat datang,", username)
            return True

    print("Username atau password salah!")
    return False


# =========================
# READ DATA WISATA
# =========================

def tampilkan_wisata():
    wisata = baca_json(FILE_WISATA)

    print("\n=== DAFTAR WISATA DAERAH ===")

    if len(wisata) == 0:
        print("Belum ada data wisata.")
        return

    tabel = PrettyTable()

    tabel.field_names = [
        "ID",
        "Nama Wisata",
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


# =========================
# CREATE DATA WISATA
# =========================

def tambah_wisata():
    wisata = baca_json(FILE_WISATA)

    print("\n=== TAMBAH WISATA ===")

    nama = input("Nama wisata : ").strip()
    lokasi = input("Lokasi      : ").strip()
    kategori = input("Kategori    : ").strip()

    if not nama or not lokasi or not kategori:
        print("Semua data harus diisi!")
        return

    try:
        harga = int(input("Harga tiket : Rp"))

        if harga < 0:
            print("Harga tidak boleh negatif!")
            return

    except ValueError:
        print("Harga harus berupa angka!")
        return

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

    simpan_json(FILE_WISATA, wisata)

    print("Data wisata berhasil ditambahkan!")


# =========================
# MENU SISTEM
# =========================

def menu_utama():
    while True:
        print("\n==============================")
        print(" SISTEM PENGELOLAAN WISATA")
        print("==============================")
        print("1. Lihat daftar wisata")
        print("2. Tambah wisata")
        print("3. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_wisata()

        elif pilihan == "2":
            tambah_wisata()

        elif pilihan == "3":
            print("Logout berhasil!")
            break

        else:
            print("Pilihan tidak valid!")


# =========================
# PROGRAM UTAMA
# =========================

def main():
    while True:
        print("\n==============================")
        print(" SISTEM PENGELOLAAN WISATA")
        print("==============================")
        print("1. Registrasi")
        print("2. Login")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            registrasi()

        elif pilihan == "2":
            if login():
                menu_utama()

        elif pilihan == "3":
            print("Program selesai.")
            break

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    main()