<<<<<<< HEAD
# Aurora Buslines Reservation System

The **Aurora Buslines Reservation System** is a CLI (Command Line Interface) based bus ticket booking management application built using Python. This application features a multi-role architecture (**Admin** and **User**) and automates transaction workflows, including instant HTML email confirmations, payment verification, cancellations, and refund processing integrated with dynamic QR code generation.

---

## 🚀 Key Features

### 1. Multi-Role System (Authentication & Login)
* **User Role:** Book bus tickets, choose routes, select departure schedules, choose bus types, pick seats interactively, select payment methods, search transaction history, and cancel active tickets.
* **Admin Role:** Manage master route data (add, edit, delete, and modify ticket prices), verify pending payments to "PAID" status, process ticket refunds/returns manually, and view a centralized revenue report.

### 2. Automated Email Notifications (SMTP Integration)
Directly integrated with the Gmail SMTP server to send formatted responsive HTML emails to customers for various events:
* Booking confirmations (with an embedded *inline QR Code* containing transaction metadata for QRIS payments).
* Payment verification updates once marked as paid by the Admin.
* Reservation cancellation confirmations.
* Refund/return request receipts.

### 3. Interactive & Modern CLI Interface
* Leverages the `rich` library to present data using beautiful visual panels, organized tables, status-based text coloring, and animated loading delays.
* Interactive seat mapping (`[A1]` to `[D4]`) with real-time visual cues: Green means available, and Red marked with `[X]` means already booked/reserved.

---

## 🛠️ Prerequisites & Dependencies

Before running the application, ensure that you have Python (version 3.8 or newer) installed along with the following third-party libraries:

```bash
pip install colorama rich qrcode pillow
=======
# 🚀 Nexus Innovate Landing Page

Landing page modern bertema teknologi dan transformasi digital yang dibangun menggunakan **HTML, CSS, dan JavaScript** murni tanpa framework.

## ✨ Fitur

* Responsive Design (Desktop & Mobile)
* Modern Glassmorphism UI
* Smooth Scroll Animation
* Reveal Animation saat Scroll
* Animated Counter Statistics
* Sticky Navigation Bar
* Gradient Branding
* Fast Loading
* SEO Friendly Structure

## 📸 Preview

Nexus Innovate merupakan landing page perusahaan teknologi fiktif yang menawarkan layanan:

* Scale-Up Bisnis
* Custom Software Development
* AI Integration
* Digital Transformation

## 🛠️ Teknologi yang Digunakan

* HTML5
* CSS3
* JavaScript (Vanilla JS)
* Font Awesome Icons
* Google Fonts (Plus Jakarta Sans)

## 📂 Struktur Folder

```text
project/
│
├── index.html
├── css/
│   └── style.css
│
├── js/
│   └── script.js
│
└── assets/
    ├── images/
    ├── videos/
    └── icons/
```

## 🚀 Cara Menjalankan

1. Clone repository

```bash
git clone https://github.com/username/nexus-innovate.git
```

2. Masuk ke folder project

```bash
cd nexus-innovate
```

3. Buka file `index.html` menggunakan browser

Atau gunakan Live Server pada VS Code untuk pengalaman pengembangan yang lebih baik.

## 🎨 Fitur Animasi

### Navbar Blur Effect

Navbar akan berubah menjadi transparan blur ketika pengguna melakukan scroll.

### Reveal Animation

Elemen akan muncul dengan animasi fade-up saat memasuki viewport.

### Counter Animation

Statistik perusahaan akan bertambah secara otomatis ketika section terlihat.

## 📱 Responsive Design

Website telah dioptimalkan untuk:

* Desktop
* Laptop
* Tablet
* Smartphone

## 📈 Pengembangan Selanjutnya

Beberapa fitur yang dapat ditambahkan:

* Dark / Light Mode
* Testimonial Section
* Portfolio Gallery
* Blog Section
* Contact Form
* Backend Integration
* CMS Dashboard
* AI Chat Assistant

## 👨‍💻 Author

Developed by **Fajar Skyy**

## 📄 License

This project is available for personal and educational use.

---

⭐ Jika project ini membantu, jangan lupa berikan star pada repository.
>>>>>>> 3a9addc7ef022ce059308d14d17a9393df46f4f4
