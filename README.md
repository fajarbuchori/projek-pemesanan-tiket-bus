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