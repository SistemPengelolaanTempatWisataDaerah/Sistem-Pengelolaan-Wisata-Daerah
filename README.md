# Sistem Pengelolaan Wisata Daerah
## Kelas B Kelompok 2
### Anggota & Peran
1. Muhammad Azam (2609116042):
2. Abdul Azis Zulkarnain (2609116051):
3. Ivanka Putri Meisyarah (2609116066):
4. Yasyid Ali Ramadhan (2609116072):

## Deskripsi & Tujuan

### Deskripsi Program

Sistem Pengelolaan Wisata Daerah merupakan program berbasis Python yang dirancang untuk mempermudah pengelolaan informasi tempat wisata serta proses transaksi pembelian tiket wisata. Program ini menggunakan file JSON sebagai media penyimpanan data pengguna, data wisata, dan riwayat transaksi sehingga data tetap tersimpan meskipun program ditutup.

Program ini memiliki dua jenis pengguna, yaitu Admin dan User, dengan hak akses yang berbeda. Admin dapat mengelola data wisata, melihat seluruh riwayat transaksi, serta memantau laporan pendapatan dan penjualan tiket. Sementara itu, User dapat melihat daftar wisata, melakukan top up saldo, membeli tiket wisata, melihat riwayat transaksi, dan mencetak kembali invoice pembelian.

Dengan adanya program ini, proses pengelolaan wisata dan transaksi tiket diharapkan menjadi lebih terstruktur, praktis, dan mudah digunakan.

### Tujuan Program

1. Mempermudah pengelolaan data tempat wisata berdasarkan nama, lokasi, kategori, dan harga tiket.
2. Menyediakan sistem registrasi dan login dengan pembagian hak akses Admin dan User.
3. Memudahkan Admin dalam menambah, mengubah, menghapus, dan melihat data wisata.
4. Memudahkan User dalam melihat informasi dan daftar tempat wisata yang tersedia.
5. Menyediakan fitur top up saldo sebagai metode pembayaran tiket wisata.
6. Mempermudah proses pembelian tiket berdasarkan jumlah tiket dan harga yang telah ditentukan.
7. Menghasilkan invoice sebagai bukti transaksi pembelian tiket maupun top up saldo.
8. Menyimpan riwayat transaksi agar dapat dilihat kembali oleh User dan Admin.
9. Membantu Admin memantau total pendapatan, jumlah transaksi, dan destinasi wisata yang paling banyak terjual tiketnya.
10. Menerapkan penggunaan Python dan JSON dalam pembuatan sistem pengelolaan data dan transaksi.

## Flowchart

### Menu Utama

<img width="1571" height="1223" alt="menu login jpg" src="https://github.com/user-attachments/assets/312875e2-f3f6-453c-a897-23f64b78d8f6" />

### Menu Admin

<img width="2203" height="1760" alt="menu admin" src="https://github.com/user-attachments/assets/7f683608-b881-4f0c-a930-23addd399fba" />

### Menu User

<img width="2313" height="1516" alt="menu user jpg" src="https://github.com/user-attachments/assets/789085ac-0ec2-499b-8ec6-b0eeb6cb7740" />

## Daftar Fitur per Role

### Fitur Menu Utama

1. Login
2. Registrasi
3. Keluar

### Fitur Role Admin
 Admin memiliki akses untuk mengelola data wisata dan melihat seluruh data transaksi pelanggan serta laporan ringkas penjualan:

 1. LIhat daftar wisata
 2. Tambah wisata
 3. Ubah wisata
 4. Hapus wisata
 5. Seluruh riwayat transaksi
 6. Laporan ringkas
 7. Logout

### Fitur Role Pelanggan

Pelanggan memiliki akses untuk:

1. Lihat daftar wisata
2. Top up saldo
3. Beli tiket wisata
4. Riwayat transaksi
5. Lihat invoice
6. Logout

## Output & penjelasan

### Menu Utama
1. Tampilan menu utama dan login sebagai admin.

<img width="666" height="247" alt="WhatsApp Image 2026-11-02 at 20 58 47" src="https://github.com/user-attachments/assets/10171e30-747f-454d-b44e-b5d7685fba0b" />

2. Tampilan menu utama dan registrasi akun. 

<img width="533" height="275" alt="image" src="https://github.com/user-attachments/assets/bb944d50-4b42-4c72-9fe2-2351592b02ef" />

3. Tampilan menu utama dan login sebagai user (Gagal 3 kali).

<img width="603" height="333" alt="image" src="https://github.com/user-attachments/assets/3a2b63f6-d4d8-4c47-bd37-3001e22c4415" />

4. Tampilan menu utama dan login sebagai user (Berhasil), akan otomatis masuk ke tampilan menu user.

<img width="533" height="210" alt="image" src="https://github.com/user-attachments/assets/441fc6ce-6d1b-4339-a0d4-833eb64d0aae" />


### Menu Admin

1. Tampilan Menu Admin

<img width="577" height="243" alt="WhatsApp Image 2026-11-02 at 21 24 58" src="https://github.com/user-attachments/assets/b00674d5-fb82-4be3-9b67-98bbb8e5501d" />

2. Tampilan menu admin 1. (Lihat daftar wisata)

<img width="1041" height="470" alt="WhatsApp Image 2026-11-02 at 21 13 59" src="https://github.com/user-attachments/assets/f6485dca-cc73-4cb6-98df-aaac6c18cbe6" />

3. Tampilan menu admin 2. (Tambah wisata)

<img width="716" height="562" alt="WhatsApp Image 2026-11-02 at 21 38 25" src="https://github.com/user-attachments/assets/960eb3af-056b-40e6-a96b-b01625b61ba4" />

4. Tampilan menu admin 3. (Ubah wisata)

<img width="1201" height="766" alt="WhatsApp Image 2026-11-02 at 21 41 55" src="https://github.com/user-attachments/assets/21eacebe-5e11-44c2-95aa-f388fa4e8d23" />

5. Tampilan menu admin 4. (Hapus wisata)

<img width="820" height="531" alt="WhatsApp Image 2026-11-02 at 21 16 56" src="https://github.com/user-attachments/assets/7633bb26-f651-4d12-96dd-9c17699e0efb" />

6. Tampilan menu admin 5. (Seluruh riwayat transaksi)

<img width="1133" height="442" alt="WhatsApp Image 2026-11-02 at 21 46 30" src="https://github.com/user-attachments/assets/5af1164f-bfe5-4948-88f9-d1c1487c9f1c" />

7. Menu admin 6. (Laporan ringkas)

<img width="641" height="377" alt="WhatsApp Image 2026-11-02 at 21 51 24" src="https://github.com/user-attachments/assets/5bc647b3-aa64-4a20-a454-5b44e6b492a1" />

8. LOGOUT (Kembali ke menu utama)

### Menu User

1. Tampilan Menu User

<img width="565" height="262" alt="image" src="https://github.com/user-attachments/assets/b09aa717-9094-45ae-8397-7b8cb999d444" />

2. Tampilan menu user 1. (Lihat daftar wisata)

<img width="745" height="479" alt="image" src="https://github.com/user-attachments/assets/95eb6e28-6904-4fd8-8f9a-978060878b6d" />

3. Tampilan menu user 2. (Top up saldo)

<img width="525" height="669" alt="image" src="https://github.com/user-attachments/assets/4406c92e-8f49-4aac-be8b-2c54caed7972" />

4. Tampilan menu user 3. (Beli tiket wisata)

<img width="846" height="621" alt="image" src="https://github.com/user-attachments/assets/075a56f6-0093-4ca9-be46-3a62c7cf67ad" />
<img width="669" height="369" alt="image" src="https://github.com/user-attachments/assets/663552e2-3d47-40ec-8aa3-a9de3a579552" />

5. Tampilan menu user 4. (Riwayat transaksi)

<img width="929" height="532" alt="image" src="https://github.com/user-attachments/assets/0c5fdc47-2438-4a5b-a1b4-f51b2d1c3e5b" />

6. Tampilan menu user 5. (Lihat invoice)

<img width="914" height="723" alt="image" src="https://github.com/user-attachments/assets/a9d96d38-3dd9-4f0f-bdb3-eacedfaa50a4" />

7. LOGOUT (Kembali ke menu utama)














