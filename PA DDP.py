
import json
import os
import math
from prettytable import PrettyTable
import pwinput

#LOKASI FOLDER DATA
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

#DATA AWAL
data = {
    "akun": [
        {
            "username": "admin",
            "password": "admin123",
            "role": "admin",
            "saldo": 0
        }
    ],
    "wisata": [
        {"nama": "Pulau Derawan", "lokasi": "Berau", "harga": 50000},
        {"nama": "Danau Labuan Cermin", "lokasi": "Berau", "harga": 35000},
        {"nama": "Desa Budaya Pampang", "lokasi": "Samarinda", "harga": 25000},
        {"nama": "Maratua", "lokasi": "Berau", "harga": 60000},
        {"nama": "Beras Basah", "lokasi": "Bontang", "harga": 25000}
    ],
    "transaksi": []
}

#MENYIMPAN DATA KE FILE JSON

def simpan_data_user():
    with open(os.path.join(DATA_DIR, "data_user.json"), "w", encoding="utf-8") as file:
        json.dump({"akun": data["akun"]}, file, indent=4)


def simpan_data_wisata():
    with open(os.path.join(DATA_DIR, "data_wisata.json"), "w", encoding="utf-8") as file:
        json.dump({"wisata": data["wisata"]}, file, indent=4)


def simpan_data_transaksi():
    with open(os.path.join(DATA_DIR, "data_transaksi.json"), "w", encoding="utf-8") as file:
        json.dump({"transaksi": data["transaksi"]}, file, indent=4)


#MEMBACA DATA DARI FILE JSON
def baca_data():
    global data

    daftar_file = [
        ("akun", "data_user.json", simpan_data_user),
        ("wisata", "data_wisata.json", simpan_data_wisata),
        ("transaksi", "data_transaksi.json", simpan_data_transaksi)
    ]

    for bagian, nama_file, fungsi_simpan in daftar_file:
        lokasi_file = os.path.join(DATA_DIR, nama_file)

        if not os.path.exists(lokasi_file):
            fungsi_simpan()
            continue

        try:
            with open(lokasi_file, "r", encoding="utf-8") as file:
                isi = json.load(file)

            if bagian in isi and isinstance(isi[bagian], list):
                data[bagian] = isi[bagian]
            else:
                print("Format file", nama_file, "tidak sesuai.")

        except json.JSONDecodeError:
            print("File", nama_file, "kosong atau formatnya salah.")

#MENAMPILKAN DATA WISATA
def tampilkan_wisata():
    tabel = PrettyTable()
    tabel.field_names = ["No", "Nama Wisata", "Lokasi", "Harga"]

    for i, wisata in enumerate(data["wisata"], 1):
        tabel.add_row([
            i,
            wisata["nama"],
            wisata["lokasi"],
            "Rp" + str(wisata["harga"])
        ])

    print(tabel)

#REGISTRASI AKUN
def registrasi():
    username = input("Username baru: ").strip()

    if username == "":
        print("Username tidak boleh kosong.")
        return

    for akun in data["akun"]:
        if akun["username"] == username:
            print("Username sudah digunakan.")
            return

    password = pwinput.pwinput("Password baru: ")

    if password == "":
        print("Password tidak boleh kosong.")
        return

    data["akun"].append({
        "username": username,
        "password": password,
        "role": "user",
        "saldo": 0
    })

    simpan_data_user()
    print("Registrasi berhasil!")

#LOGIN AKUN
def login():
    username = input("Username: ").strip()
    password = pwinput.pwinput("Password: ")

    for akun in data["akun"]:
        if akun["username"] == username and akun["password"] == password:
            print("Login berhasil!")
            return akun

    print("Login gagal.")
    return None

#MENAMBAH WISATA
def tambah_wisata():
    nama = input("Nama wisata: ").strip()
    lokasi = input("Lokasi: ").strip()

    if nama == "" or lokasi == "":
        print("Nama dan lokasi tidak boleh kosong.")
        return

    try:
        harga = int(input("Harga tiket: "))

        if harga <= 0:
            print("Harga harus lebih dari 0.")
            return

        data["wisata"].append({
            "nama": nama,
            "lokasi": lokasi,
            "harga": harga
        })

        simpan_data_wisata()
        print("Wisata berhasil ditambahkan.")

    except ValueError:
        print("Harga harus berupa angka.")

#MENGUBAH WISATA
def ubah_wisata():
    tampilkan_wisata()

    try:
        nomor = int(input("Nomor wisata yang diubah: "))

        if nomor < 1 or nomor > len(data["wisata"]):
            print("Nomor tidak tersedia.")
            return

        wisata = data["wisata"][nomor - 1]

        nama = input("Nama baru (Enter jika tetap): ").strip()
        lokasi = input("Lokasi baru (Enter jika tetap): ").strip()
        harga = input("Harga baru (Enter jika tetap): ").strip()

        if harga != "" and int(harga) <= 0:
            print("Harga harus lebih dari 0.")
            return

        if nama != "":
            wisata["nama"] = nama

        if lokasi != "":
            wisata["lokasi"] = lokasi

        if harga != "":
            wisata["harga"] = int(harga)

        simpan_data_wisata()
        print("Wisata berhasil diubah.")

    except ValueError:
        print("Nomor dan harga harus berupa angka.")

# HAPUS WISATA
def hapus_wisata():
    tampilkan_wisata()

    try:
        nomor = int(input("Nomor wisata yang dihapus: "))

        if nomor < 1 or nomor > len(data["wisata"]):
            print("Nomor tidak tersedia.")
            return

        konfirmasi = input("Yakin hapus wisata ini? (y/n): ").lower()

        if konfirmasi == "y":
            data["wisata"].pop(nomor - 1)
            simpan_data_wisata()
            print("Wisata berhasil dihapus.")
        else:
            print("Penghapusan dibatalkan.")

    except ValueError:
        print("Nomor harus berupa angka.")

#MENU ADMIN
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

#MENU USER
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

                if jumlah <= 0:
                    print("Jumlah harus lebih dari 0.")
                    continue

                akun["saldo"] += jumlah
                simpan_data_user()
                print("Saldo sekarang: Rp", akun["saldo"])

            except ValueError:
                print("Masukkan angka yang benar.")

        elif pilihan == "3":
            tampilkan_wisata()

            try:
                nomor = int(input("Nomor wisata: "))
                jumlah = int(input("Jumlah tiket: "))

                if nomor < 1 or nomor > len(data["wisata"]) or jumlah <= 0:
                    print("Pilihan atau jumlah tiket tidak tersedia.")
                    continue

                wisata = data["wisata"][nomor - 1]
                total = math.ceil(wisata["harga"] * jumlah)

                print("Total pembayaran: Rp", total)
                print("Saldo kamu: Rp", akun["saldo"])

                if akun["saldo"] < total:
                    print("Saldo tidak cukup.")
                    continue

                konfirmasi = input("Bayar tiket? (beli/batal): ").lower()

                if konfirmasi == "beli":
                    akun["saldo"] -= total

                    data["transaksi"].append({
                        "username": akun["username"],
                        "wisata": wisata["nama"],
                        "jumlah_tiket": jumlah,
                        "total": total
                    })

                    simpan_data_user()
                    simpan_data_transaksi()

                    print("Pembelian berhasil!")
                    print("Sisa saldo: Rp", akun["saldo"])
                else:
                    print("Pembelian dibatalkan.")

            except ValueError:
                print("Input harus berupa angka.")

        elif pilihan == "4":
            ada_transaksi = False

            for transaksi in data["transaksi"]:
                if transaksi["username"] == akun["username"]:
                    print(transaksi)
                    ada_transaksi = True

            if not ada_transaksi:
                print("Belum ada transaksi.")

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak tersedia.")

#PROGRAM UTAMA
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
            print("Terima kasih.")
            break

        else:
            print("Pilihan tidak tersedia.")


main()