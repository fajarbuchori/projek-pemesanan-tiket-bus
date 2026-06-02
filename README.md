# projek-pemesanan-tiket-bus
Membuat sistem pemesanan tiket bus yang interaktif dan menarik.

# 🚌 AURORA BUSLINES RESERVATION SYSTEM

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Rich](https://img.shields.io/badge/Rich-Terminal_UI-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

# 🚌 AURORA BUSLINES RESERVATION SYSTEM

Sistem Reservasi Tiket Bus berbasis Terminal menggunakan Python.

Aplikasi ini memungkinkan pengguna melakukan pemesanan tiket bus, mencari tiket berdasarkan nomor resi, melihat daftar jurusan, melihat seluruh transaksi, dan menampilkan laporan pendapatan.

---

## ✨ Fitur

### 🔐 Login System
- Login menggunakan ID dan Password.
- Validasi login sebelum masuk ke dashboard.

### 🎫 Pemesanan Tiket
- Input data penumpang.
- Pilihan jurusan berdasarkan kode.
- Pilihan jenis bus.
- Pilihan jenis tiket.
- Pemilihan nomor kursi.
- Generate nomor resi otomatis.
- Diskon otomatis berdasarkan jumlah tiket.

### 🔍 Cari Tiket
- Mencari tiket menggunakan nomor resi.
- Menampilkan detail tiket yang telah dipesan.

### 🗺️ Daftar Jurusan
- Menampilkan seluruh jurusan yang tersedia.
- Menggunakan kode jurusan untuk mengurangi kesalahan input.

### 📊 Laporan Pendapatan
- Total transaksi.
- Total tiket terjual.
- Total pendapatan.

### 🚪 Logout
- Keluar dari sistem.

---

## 🛠️ Teknologi yang Digunakan

- Python 3
- Rich
- Colorama

---

## 📦 Instalasi

Install package yang diperlukan:

```bash
pip install rich colorama
```

---

## ▶️ Menjalankan Program

```bash
python aurora_buslines.py
```

---

## 🔑 Login Default

```text
ID Login : admin
Password : 12345
```

---

## 📌 Daftar Jurusan

| Kode | Jurusan |
|--------|----------|
| SJ01 | Surabaya → Jakarta |
| JS02 | Jakarta → Surabaya |
| BJ03 | Bandung → Jakarta |
| JB04 | Jakarta → Bandung |
| YS05 | Yogyakarta → Surabaya |

---

## 🎟️ Jenis Tiket

### Ekonomi
Harga paling terjangkau.

### Eksekutif
Kursi lebih nyaman.

### VIP
Fasilitas premium dan kursi eksklusif.

---

## 💺 Sistem Kursi

- Setiap kursi hanya dapat dipilih satu kali.
- Kursi yang sudah digunakan tidak dapat dipilih kembali.
- Sistem akan menampilkan kursi yang tersedia.

---

## 💰 Sistem Diskon

| Jumlah Tiket | Diskon |
|-------------|---------|
| 1 - 2 | 0% |
| 3 - 4 | 5% |
| ≥ 5 | 10% |

---

## 📄 Contoh Nomor Resi

```text
ABL-137563
```

---

## ⚠️ Disclaimer

Tiket yang sudah dibeli **tidak dapat direfund**.

---

## 👨‍💻 Developer

Project dibuat menggunakan Python sebagai implementasi konsep:

- Function
- Dictionary
- List
- Looping
- Validation
- Conditional Statement
- Data Management
- Terminal User Interface (TUI)

---

## 📷 Tampilan

Dashboard:

```text
[1] Pesan Tiket
[2] Cari Tiket
[3] Daftar Jurusan
[4] Lihat Semua Transaksi
[5] Laporan Pendapatan
[6] Logout
```

---

## 🎯 Tujuan Project

Project ini dibuat sebagai simulasi sistem reservasi tiket bus berbasis terminal untuk mempelajari penerapan pemrograman Python dalam pengelolaan data dan interaksi pengguna.
