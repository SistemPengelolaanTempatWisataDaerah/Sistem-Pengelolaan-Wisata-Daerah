
import json
import os
import math
from pathlib import Path
from prettytable import PrettyTable
import pwinput

DATA_DIR = Path(__file__).resolve().parent

data = {
    "akun": [
        {"username": "admin", "password": "admin123",
         "role": "admin", "saldo": 0}
    ],
    "wisata": [
        {"nama": "Pulau Derawan", "lokasi": "Berau", "harga": 50000},
        {"nama": "Danau Labuan Cermin", "lokasi": "Berau", "harga": 35000},
        {"nama": "Desa Budaya Pampang", "lokasi": "Samarinda", "harga": 25000}
    ],
    "transaksi": []
}


def simpan_data_wisata():
    with open(DATA_DIR / "data_wisata.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        return

def simpan_data_user():
    with open(DATA_DIR / "data_user.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        return

def simpan_data_transaksi():
    with open(DATA_DIR / "data_transaksi.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
        return



def baca_data():
    global data

    sumber_data = {
        "akun": (DATA_DIR / "data_user.json", simpan_data_user),
        "wisata": (DATA_DIR / "data_wisata.json", simpan_data_wisata),
        "transaksi": (DATA_DIR / "data_transaksi.json", simpan_data_transaksi)
    }

    for bagian, (lokasi_file, fungsi_simpan) in sumber_data.items():
        try:
            with open(lokasi_file, "r", encoding="utf-8") as file:
                data_tersimpan = json.load(file)
        except FileNotFoundError:
            fungsi_simpan()
            continue

        if bagian in data_tersimpan:
            data[bagian] = data_tersimpan[bagian]


def tampilkan_wisata():
    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Wisata", "Lokasi", "Harga"]

    for i, wisata in enumerate(data["wisata"], 1):
        tabel.add_row([
            i, wisata["nama"], wisata["lokasi"],
            "Rp" + str(wisata["harga"])
        ])

    print(tabel)


def login():
    username = input("Username: ")
    password = pwinput.pwinput("Password: ")

    for akun in data["akun"]:
        if akun["username"] == username and akun["password"] == password:
            print("Login berhasil!")
            return akun

    print("Login gagal.")
    return None


def registrasi():
    username = input("Username baru: ")

    for akun in data["akun"]:
        if akun["username"] == username:
            print("Username sudah digunakan.")
            return

    password = pwinput.pwinput("Password baru: ")

    data["akun"].append({
        "username": username,
        "password": password,
        "role": "user",
        "saldo": 0
    })

    simpan_data_user()
    print("Registrasi berhasil!")


def tambah_wisata():
    nama = input("Nama wisata: ")
    lokasi = input("Lokasi: ")

    try:
        harga = int(input("Harga tiket: "))

        if harga > 0:
            data["wisata"].append({
                "nama": nama,
                "lokasi": lokasi,
                "harga": harga
            })
            simpan_data_wisata()
            print("Wisata berhasil ditambahkan.")
        else:
            print("Harga harus lebih dari 0.")

    except ValueError:
        print("Harga harus berupa angka.")


def ubah_wisata():
    tampilkan_wisata()

    try:
        nomor = int(input("Nomor wisata yang diubah: "))

        if 1 <= nomor <= len(data["wisata"]):
            wisata = data["wisata"][nomor - 1]

            nama = input("Nama baru (Enter jika tetap): ")
            lokasi = input("Lokasi baru (Enter jika tetap): ")
            harga = input("Harga baru (Enter jika tetap): ")

            if nama != "":
                wisata["nama"] = nama
            if lokasi != "":
                wisata["lokasi"] = lokasi
            if harga != "":
                if int(harga) > 0:
                    wisata["harga"] = int(harga)
                else:
                    print("Harga harus lebih dari 0.")
                    return

            simpan_data_wisata()
            print("Wisata berhasil diubah.")
        else:
            print("Nomor tidak tersedia.")

    except ValueError:
        print("Input harus berupa angka.")


def hapus_wisata():
    tampilkan_wisata()

    try:
        nomor = int(input("Nomor wisata yang dihapus: "))

        if 1 <= nomor <= len(data["wisata"]):
            data["wisata"].pop(nomor - 1)
            simpan_data_wisata()
            print("Wisata berhasil dihapus.")
        else:
            print("Nomor tidak tersedia.")

    except ValueError:
        print("Input harus berupa angka.")


def menu_admin():
    while True:
        print("\n=== MENU ADMIN ===")
        print("1. Lihat wisata")
        print("2. Tambah wisata")
        print("3. Ubah wisata")
        print("4. Hapus wisata")
        print("5. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_wisata()
        elif pilihan == "2":
            tambah_wisata()
        elif pilihan == "3":
            ubah_wisata()
        elif pilihan == "4":
            hapus_wisata()
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak tersedia.")


def menu_user(akun):
    while True:
        print("\n=== MENU USER ===")
        print("1. Lihat wisata")
        print("2. Top up saldo")
        print("3. Beli tiket")
        print("4. Riwayat transaksi")
        print("5. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_wisata()

        elif pilihan == "2":
            try:
                jumlah = int(input("Jumlah top up: "))

                if jumlah > 0:
                    akun["saldo"] += jumlah
                    simpan_data_user()
                    print("Saldo sekarang: Rp", akun["saldo"])
                else:
                    print("Jumlah harus lebih dari 0.")

            except ValueError:
                print("Masukkan angka.")

        elif pilihan == "3":
            tampilkan_wisata()

            try:
                nomor = int(input("Nomor wisata: "))
                jumlah = int(input("Jumlah tiket: "))

                if 1 <= nomor <= len(data["wisata"]) and jumlah > 0:
                    wisata = data["wisata"][nomor - 1]
                    total = math.ceil(wisata["harga"] * jumlah)

                    print("Total pembayaran: Rp", total)

                    if akun["saldo"] >= total:
                        konfirmasi = input("Bayar tiket? (beli/batal): ")

                        if konfirmasi == "beli":
                            akun["saldo"] -= total

                            data["transaksi"].append({
                                "username": akun["username"],
                                "wisata": wisata["nama"],
                                "jumlah": total
                            })

                            simpan_data_user()
                            simpan_data_transaksi()
                            print("Pembelian berhasil.")
                        else:
                            print("Pembelian dibatalkan.")
                    else:
                        print("Saldo tidak cukup.")
                else:
                    print("Pilihan tidak tersedia.")

            except ValueError:
                print("Input harus berupa angka.")

        elif pilihan == "4":
            for transaksi in data["transaksi"]:
                if transaksi["username"] == akun["username"]:
                    print(transaksi)

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak tersedia.")


def main():
    baca_data()

    while True:
        print("\n=== SISTEM PENGELOLAAN TEMPAT WISATA ===")
        print("1. Login")
        print("2. Registrasi")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            akun = login()

            if akun is not None:
                if akun["role"] == "admin":
                    menu_admin()
                else:
                    menu_user(akun)

        elif pilihan == "2":
            registrasi()

        elif pilihan == "3":
            simpan_data_user()
            print("Terima kasih.")
            break

        else:
            print("Pilihan tidak tersedia.")


main()