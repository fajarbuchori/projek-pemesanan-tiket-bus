from datetime import datetime
import random
import time
import io
import base64
from colorama import init, Fore
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import qrcode

init(autoreset=True)
console = Console()

# ─── Akun login ───────────────────────────────────────────────────────────────
AKUN = {
    "Admin": {"password": "Admin123", "role": "admin"},
    "User":  {"password": "User123",    "role": "user"},
}

EMAIL_PENGIRIM = "fajarskyy833@gmail.com"
APP_PASSWORD   = "gmzq ormq jrxu lsqq"

transaksi = []
kursi_terpakai = set()
refund_history = []
refund_request = []

# ─── Data jurusan + jadwal keberangkatan ──────────────────────────────────────
jurusan = {
    "SJ01": {
        "rute": "Surabaya -> Jakarta",
        "Ekonomi": 250000, "Eksekutif": 350000, "VIP": 500000,
        "jadwal": ["06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    },
    "JS02": {
        "rute": "Jakarta -> Surabaya",
        "Ekonomi": 250000, "Eksekutif": 350000, "VIP": 500000,
        "jadwal": ["07:00", "10:00", "13:00", "16:00", "19:00", "22:00"]
    },
    "BJ03": {
        "rute": "Bandung -> Jakarta",
        "Ekonomi": 100000, "Eksekutif": 150000, "VIP": 250000,
        "jadwal": ["05:30", "08:00", "11:00", "14:00", "17:00", "20:00"]
    },
    "JB04": {
        "rute": "Jakarta -> Bandung",
        "Ekonomi": 100000, "Eksekutif": 150000, "VIP": 250000,
        "jadwal": ["06:30", "09:30", "12:30", "15:30", "18:30", "21:30"]
    },
    "YS05": {
        "rute": "Yogyakarta -> Surabaya",
        "Ekonomi": 150000, "Eksekutif": 250000, "VIP": 350000,
        "jadwal": ["05:00", "08:30", "11:30", "14:30", "17:30", "20:30"]
    },
}

# ──────────────────────────────────────────────────────────────────────────────

def loading(teks):
    print(teks, end="")
    for _ in range(5):
        time.sleep(0.2)
        print(".", end="", flush=True)
    print()

def generate_resi():
    return f"ABL-{random.randint(100000,999999)}"

def generate_qr_bytes(data):
    isi_qr = (
        f"AURORA BUSLINES\n"
        f"Resi   : {data['resi']}\n"
        f"Nama   : {data['nama']}\n"
        f"Rute   : {data['rute']}\n"
        f"Jadwal : {data['jadwal']}\n"
        f"Tiket  : {data['tiket']}\n"
        f"Kursi  : {data['kursi']}\n"
        f"Total  : Rp{data['total']:,.0f}\n"
        f"Bayar  : {data['metode']}\n"
        f"Waktu  : {data['waktu']}"
    )
    qr = qrcode.QRCode(
        version=3,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=8,
        border=3,
    )
    qr.add_data(isi_qr)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer.getvalue()

def kirim_email(data):
    try:
        msg = MIMEMultipart("related")
        msg["Subject"] = f"Konfirmasi Tiket Aurora Buslines - {data['resi']}"
        msg["From"]    = EMAIL_PENGIRIM
        msg["To"]      = data["gmail"]

        is_qris = data["metode"].upper() == "QRIS"

        bagian_qr = ""
        if is_qris:
            bagian_qr = """
            <tr>
                <td colspan="2" style="text-align:center; padding:16px 0;">
                    <p style="color:#2563eb; font-weight:bold; margin-bottom:8px;">
                        Scan QR Code untuk konfirmasi pembayaran QRIS:
                    </p>
                    <img src="cid:qrcode_image"
                         style="width:200px; height:200px; border:4px solid #2563eb; border-radius:8px;"
                         alt="QR Code Pembayaran"/>
                    <p style="font-size:11px; color:gray; margin-top:6px;">
                        QR Code berisi detail transaksi kamu
                    </p>
                </td>
            </tr>
            """

        isi_html = f"""
        <html><body style="font-family:Arial; background:#f4f4f4; padding:20px;">
        <div style="max-width:520px; background:white; border-radius:10px;
                    padding:24px; margin:auto; border-top:5px solid #2563eb;">
            <h2 style="color:#2563eb;">Aurora Buslines</h2>
            <p>Halo <b>{data['nama']}</b>, tiket kamu berhasil dipesan!</p>
            <hr>
            <table width="100%" cellpadding="6">
                <tr><td><b>No. Resi</b></td><td>{data['resi']}</td></tr>
                <tr><td><b>Rute</b></td><td>{data['rute']}</td></tr>
                <tr><td><b>Jadwal</b></td><td>{data['jadwal']}</td></tr>
                <tr><td><b>Bus</b></td><td>{data['bus']}</td></tr>
                <tr><td><b>Kelas Tiket</b></td><td>{data['tiket']}</td></tr>
                <tr><td><b>Kursi</b></td><td>{data['kursi']}</td></tr>
                <tr><td><b>Jumlah Tiket</b></td><td>{data['jumlah']}</td></tr>
                <tr><td><b>Metode Bayar</b></td><td>{data['metode']}</td></tr>
                <tr><td><b>Waktu Pesan</b></td><td>{data['waktu']}</td></tr>
                <tr style="background:#eff6ff;">
                    <td><b>Total Bayar</b></td>
                    <td><b style="color:#2563eb;">Rp{data['total']:,.0f}</b></td>
                </tr>
                {bagian_qr}
            </table>
            <hr>
            <p style="font-size:12px; color:red;">Tiket tidak dapat direfund.</p>
            <p style="font-size:11px; color:gray;">
                Email ini dikirim otomatis oleh sistem Aurora Buslines.
            </p>
        </div>
        </body></html>
        """

        msg.attach(MIMEText(isi_html, "html"))

        if is_qris:
            qr_bytes = generate_qr_bytes(data)
            img_part = MIMEImage(qr_bytes, _subtype="png")
            img_part.add_header("Content-ID", "<qrcode_image>")
            img_part.add_header("Content-Disposition", "inline", filename="qrcode.png")
            msg.attach(img_part)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_PENGIRIM, APP_PASSWORD)
            server.sendmail(EMAIL_PENGIRIM, data["gmail"], msg.as_string())

        print(Fore.GREEN + f"Email konfirmasi dikirim ke {data['gmail']}")
        if is_qris:
            print(Fore.CYAN + "QR Code pembayaran disertakan di email.")

    except Exception as e:
        print(Fore.YELLOW + f"Email gagal terkirim: {e}")

def kirim_email_batal(data):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Pembatalan Tiket Aurora Buslines - {data['resi']}"
        msg["From"]    = EMAIL_PENGIRIM
        msg["To"]      = data["gmail"]

        isi_html = f"""
        <html><body style="font-family:Arial; background:#f4f4f4; padding:20px;">
        <div style="max-width:500px; background:white; border-radius:10px;
                    padding:24px; margin:auto; border-top:5px solid #dc2626;">
            <h2 style="color:#dc2626;">Aurora Buslines - Pembatalan Tiket</h2>
            <p>Halo <b>{data['nama']}</b>, tiket kamu telah berhasil dibatalkan.</p>
            <hr>
            <table width="100%" cellpadding="6">
                <tr><td><b>No. Resi</b></td><td>{data['resi']}</td></tr>
                <tr><td><b>Rute</b></td><td>{data['rute']}</td></tr>
                <tr><td><b>Jadwal</b></td><td>{data['jadwal']}</td></tr>
                <tr><td><b>Kursi</b></td><td>{data['kursi']}</td></tr>
                <tr><td><b>Waktu Batal</b></td><td>{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</td></tr>
            </table>
            <hr>
            <p style="font-size:12px; color:gray;">
                Email ini dikirim otomatis oleh sistem Aurora Buslines.
            </p>
        </div>
        </body></html>
        """
        msg.attach(MIMEText(isi_html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_PENGIRIM, APP_PASSWORD)
            server.sendmail(EMAIL_PENGIRIM, data["gmail"], msg.as_string())
        print(Fore.GREEN + f"Email pembatalan dikirim ke {data['gmail']}")
    except Exception as e:
        print(Fore.YELLOW + f"Email gagal terkirim: {e}")

def kirim_email_refund(data, nominal_refund):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Konfirmasi Refund Aurora Buslines - {data['resi']}"
        msg["From"]    = EMAIL_PENGIRIM
        msg["To"]      = data["gmail"]

        isi_html = f"""
        <html><body style="font-family:Arial; background:#f4f4f4; padding:20px;">
        <div style="max-width:500px; background:white; border-radius:10px;
                    padding:24px; margin:auto; border-top:5px solid #059669;">
            <h2 style="color:#059669;">Aurora Buslines - Konfirmasi Refund</h2>
            <p>Halo <b>{data['nama']}</b>, refund kamu telah berhasil diproses!</p>
            <hr>
            <table width="100%" cellpadding="6">
                <tr><td><b>No. Resi</b></td><td>{data['resi']}</td></tr>
                <tr><td><b>Rute</b></td><td>{data['rute']}</td></tr>
                <tr><td><b>Total Awal</b></td><td>Rp{data['total']:,.0f}</td></tr>
                <tr style="background:#d1fae5;">
                    <td><b>Nominal Refund</b></td>
                    <td><b style="color:#059669;">Rp{nominal_refund:,.0f}</b></td>
                </tr>
                <tr><td><b>Waktu Refund</b></td><td>{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</td></tr>
            </table>
            <hr>
            <p style="font-size:12px; color:gray;">
                Refund akan diproses ke rekening kamu dalam 3-5 hari kerja.
            </p>
        </div>
        </body></html>
        """
        msg.attach(MIMEText(isi_html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_PENGIRIM, APP_PASSWORD)
            server.sendmail(EMAIL_PENGIRIM, data["gmail"], msg.as_string())
        print(Fore.GREEN + f"Email konfirmasi refund dikirim ke {data['gmail']}")
    except Exception as e:
        print(Fore.YELLOW + f"Email gagal terkirim: {e}")

def kirim_email_request_refund(data, alasan, nominal_request):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"Permintaan Refund Aurora Buslines - {data['resi']}"
        msg["From"]    = EMAIL_PENGIRIM
        msg["To"]      = data["gmail"]

        isi_html = f"""
        <html><body style="font-family:Arial; background:#f4f4f4; padding:20px;">
        <div style="max-width:500px; background:white; border-radius:10px;
                    padding:24px; margin:auto; border-top:5px solid #f59e0b;">
            <h2 style="color:#f59e0b;">Aurora Buslines - Permintaan Refund Diterima</h2>
            <p>Halo <b>{data['nama']}</b>, permintaan refund kamu telah kami terima!</p>
            <hr>
            <table width="100%" cellpadding="6">
                <tr><td><b>No. Resi</b></td><td>{data['resi']}</td></tr>
                <tr><td><b>Rute</b></td><td>{data['rute']}</td></tr>
                <tr><td><b>Total Tiket</b></td><td>Rp{data['total']:,.0f}</td></tr>
                <tr><td><b>Alasan Refund</b></td><td>{alasan}</td></tr>
                <tr style="background:#fef3c7;">
                    <td><b>Nominal Diminta</b></td>
                    <td><b style="color:#f59e0b;">Rp{nominal_request:,.0f}</b></td>
                </tr>
                <tr style="background:#fef3c7;">
                    <td><b>Status</b></td>
                    <td><b style="color:#f59e0b;">PENDING REVIEW</b></td>
                </tr>
                <tr><td><b>Waktu Permintaan</b></td><td>{datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</td></tr>
            </table>
            <hr>
            <p style="font-size:12px; color:gray;">
                Admin kami akan mereview permintaan refund kamu dalam 1x24 jam. Anda akan mendapatkan notifikasi melalui email.
            </p>
        </div>
        </body></html>
        """
        msg.attach(MIMEText(isi_html, "html"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_PENGIRIM, APP_PASSWORD)
            server.sendmail(EMAIL_PENGIRIM, data["gmail"], msg.as_string())
        print(Fore.GREEN + f"Email permintaan refund dikirim ke {data['gmail']}")
    except Exception as e:
        print(Fore.YELLOW + f"Email gagal terkirim: {e}")

# ─── Login & deteksi role ─────────────────────────────────────────────────────

def login():
    console.print(Panel.fit("[bold cyan]AURORA BUSLINES RESERVATION SYSTEM[/bold cyan]"))
    while True:
        user = input("ID Login  : ")
        pw   = input("Password  : ")
        loading("Memverifikasi")

        if user in AKUN and AKUN[user]["password"] == pw:
            role = AKUN[user]["role"]
            if role == "admin":
                print(Fore.YELLOW + f"Login sebagai ADMIN berhasil!")
            else:
                print(Fore.GREEN + f"Login berhasil! Selamat datang, {user}.")
            return role
        else:
            print(Fore.RED + "ID atau Password salah!")

# ─── Fungsi fitur ─────────────────────────────────────────────────────────────

def tampil_jurusan():
    table = Table(title="Daftar Jurusan & Jadwal Keberangkatan")
    table.add_column("Kode",            style="cyan")
    table.add_column("Rute",            style="white")
    table.add_column("Jadwal Tersedia", style="yellow")
    for k, v in jurusan.items():
        jadwal_str = "  |  ".join(v["jadwal"])
        table.add_row(k, v["rute"], jadwal_str)
    console.print(table)

def tampil_kursi():
    console.print("[bold yellow]Kursi Tersedia[/bold yellow]")
    for b in ["A", "B", "C", "D"]:
        row = []
        for i in range(1, 5):
            k = f"{b}{i}"
            row.append(Fore.RED + "[X]" if k in kursi_terpakai else Fore.GREEN + k)
        print("  ".join(row))
    print()

def pesan_tiket():
    nama    = input("Nama : ")
    hp      = input("Nomor HP : ")
    gmail   = input("Gmail : ")
    tanggal = input("Tanggal (dd-mm-yyyy) : ")

    tampil_jurusan()
    kode = input("Kode Jurusan : ").upper()

    if kode not in jurusan:
        print(Fore.RED + "Kode jurusan tidak ditemukan!")
        return

    data_j = jurusan[kode]

    print()
    console.print("[bold yellow]Jadwal Keberangkatan Tersedia:[/bold yellow]")
    for i, j in enumerate(data_j["jadwal"], 1):
        print(f"  {i}. {j}")

    pilih_jadwal = input("Pilih Nomor Jadwal : ")
    try:
        idx_jadwal = int(pilih_jadwal) - 1
        if idx_jadwal < 0 or idx_jadwal >= len(data_j["jadwal"]):
            print(Fore.RED + "Jadwal tidak valid!")
            return
        jadwal_dipilih = data_j["jadwal"][idx_jadwal]
    except ValueError:
        print(Fore.RED + "Input tidak valid!")
        return

    table = Table(title="Jenis Tiket")
    table.add_column("Pilihan")
    table.add_column("Harga")
    table.add_row("1. Ekonomi",   f"Rp{data_j['Ekonomi']:,}")
    table.add_row("2. Eksekutif", f"Rp{data_j['Eksekutif']:,}")
    table.add_row("3. VIP",       f"Rp{data_j['VIP']:,}")
    console.print(table)

    pilih = input("Pilih Tiket : ")
    if   pilih == "1": jenis = "Ekonomi"
    elif pilih == "2": jenis = "Eksekutif"
    elif pilih == "3": jenis = "VIP"
    else:
        print(Fore.RED + "Pilihan tidak valid!")
        return

    print("1. Economy Bus")
    print("2. Premium Bus")
    print("3. Executive Bus")
    bus_map = {"1": "Economy Bus", "2": "Premium Bus", "3": "Executive Bus"}
    bus = bus_map.get(input("Pilih Bus : "), "Economy Bus")

    jumlah = int(input("Jumlah Tiket : "))

    tampil_kursi()
    kursi = input("Pilih Kursi : ").upper()

    if kursi in kursi_terpakai:
        print(Fore.RED + "Kursi sudah digunakan!")
        return
    kursi_terpakai.add(kursi)

    harga  = data_j[jenis]
    diskon = 10 if jumlah >= 5 else 5 if jumlah >= 3 else 0
    total  = harga * jumlah
    total -= total * diskon / 100

    print("\nMetode Pembayaran:")
    print("1. Cash")
    print("2. Transfer")
    print("3. QRIS  (QR Code akan dikirim ke email)")
    print("4. E-Wallet")
    metode_map = {"1": "Cash", "2": "Transfer", "3": "QRIS", "4": "E-Wallet"}
    metode = metode_map.get(input("Pilih Metode Bayar : "), "Cash")

    resi = generate_resi()

    data = {
        "resi"   : resi,
        "nama"   : nama,
        "rute"   : data_j["rute"],
        "jadwal" : f"{tanggal} {jadwal_dipilih}",
        "kursi"  : kursi,
        "tiket"  : jenis,
        "bus"    : bus,
        "total"  : total,
        "jumlah" : jumlah,
        "hp"     : hp,
        "gmail"  : gmail,
        "metode" : metode,
        "waktu"  : datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "status" : "AKTIF",
        "pembayaran" : "PENDING"
    }

    transaksi.append(data)
    loading("Mengirim email konfirmasi")
    kirim_email(data)

    tiket = f"""
NO RESI      : {resi}
NAMA         : {nama}
NO HP        : {hp}
EMAIL        : {gmail}

RUTE         : {data_j['rute']}
JADWAL       : {tanggal} pukul {jadwal_dipilih}
BUS          : {bus}
TIKET        : {jenis}
KURSI        : {kursi}
JUMLAH       : {jumlah}
DISKON       : {diskon}%
METODE BAYAR : {metode}

TOTAL BAYAR  : Rp{total:,.0f}
{"[QR Code dikirim ke email kamu]" if metode == "QRIS" else ""}
"""
    console.print(Panel(tiket, title="AURORA BUSLINES", border_style="green"))

def batal_tiket():
    console.print(Panel.fit("[bold red]PEMBATALAN TIKET[/bold red]"))
    nomor = input("Masukkan Nomor Resi : ").strip()

    tiket_ditemukan = None
    for d in transaksi:
        if d["resi"] == nomor:
            tiket_ditemukan = d
            break

    if not tiket_ditemukan:
        print(Fore.RED + "Nomor resi tidak ditemukan!")
        return

    if tiket_ditemukan["status"] == "BATAL":
        print(Fore.RED + "Tiket ini sudah pernah dibatalkan sebelumnya!")
        return

    console.print(Panel(
        f"Resi   : {tiket_ditemukan['resi']}\n"
        f"Nama   : {tiket_ditemukan['nama']}\n"
        f"Rute   : {tiket_ditemukan['rute']}\n"
        f"Jadwal : {tiket_ditemukan['jadwal']}\n"
        f"Kursi  : {tiket_ditemukan['kursi']}\n"
        f"Total  : Rp{tiket_ditemukan['total']:,.0f}",
        title="Detail Tiket", border_style="yellow"
    ))

    konfirmasi = input("Yakin ingin membatalkan tiket ini? (ya/tidak) : ").lower()

    if konfirmasi != "ya":
        print(Fore.YELLOW + "Pembatalan dibatalkan.")
        return

    tiket_ditemukan["status"] = "BATAL"
    kursi_terpakai.discard(tiket_ditemukan["kursi"])

    loading("Memproses pembatalan")
    print(Fore.GREEN + f"Tiket {nomor} berhasil dibatalkan!")
    print(Fore.GREEN + f"Kursi {tiket_ditemukan['kursi']} kembali tersedia.")

    loading("Mengirim email pembatalan")
    kirim_email_batal(tiket_ditemukan)

def cari_tiket():
    nomor = input("Masukkan Nomor Resi : ")
    for d in transaksi:
        if d["resi"] == nomor:
            status_color = "green" if d["status"] == "AKTIF" else "red"
            pembayaran_color = "yellow" if d.get("pembayaran") == "PENDING" else "green"
            console.print(Panel(
                f"Resi    : {d['resi']}\n"
                f"Nama    : {d['nama']}\n"
                f"Rute    : {d['rute']}\n"
                f"Jadwal  : {d['jadwal']}\n"
                f"Kursi   : {d['kursi']}\n"
                f"Tiket   : {d['tiket']}\n"
                f"Total   : Rp{d['total']:,.0f}\n"
                f"Metode  : {d['metode']}\n"
                f"Status  : {d['status']}\n"
                f"Pembayaran : {d.get('pembayaran', 'PENDING')}",
                title="Tiket Ditemukan", border_style=status_color
            ))
            return
    print(Fore.RED + "Nomor resi tidak ditemukan")

def lihat_transaksi():
    if not transaksi:
        print("Belum ada transaksi")
        return

    table = Table(title="Semua Transaksi")
    table.add_column("Resi",   style="cyan")
    table.add_column("Nama",   style="white")
    table.add_column("Rute",   style="white")
    table.add_column("Jadwal", style="yellow")
    table.add_column("Metode", style="magenta")
    table.add_column("Total",  style="green")
    table.add_column("Status", style="white")
    table.add_column("Bayar",  style="white")

    for d in transaksi:
        status_style = "[green]AKTIF[/green]" if d["status"] == "AKTIF" else "[red]BATAL[/red]"
        pembayaran = d.get("pembayaran", "PENDING")
        pembayaran_style = "[yellow]PENDING[/yellow]" if pembayaran == "PENDING" else "[green]LUNAS[/green]"
        table.add_row(
            d["resi"], d["nama"], d["rute"],
            d["jadwal"], d["metode"], f"Rp{d['total']:,.0f}", status_style, pembayaran_style
        )
    console.print(table)

def laporan():
    # Hanya bisa dipanggil oleh admin
    aktif = [x for x in transaksi if x["status"] == "AKTIF"]
    batal = [x for x in transaksi if x["status"] == "BATAL"]
    lunas = [x for x in transaksi if x.get("pembayaran") == "LUNAS"]

    total_transaksi = len(aktif)
    total_tiket     = sum(x["jumlah"] for x in aktif)
    pendapatan      = sum(x["total"]  for x in lunas)

    # Rincian per rute
    rute_data = {}
    for x in aktif:
        r = x["rute"]
        if r not in rute_data:
            rute_data[r] = {"jumlah": 0, "pendapatan": 0}
        rute_data[r]["jumlah"]    += x["jumlah"]
        if x.get("pembayaran") == "LUNAS":
            rute_data[r]["pendapatan"] += x["total"]

    console.print(Panel(
        f"[bold]Total Transaksi Aktif : {total_transaksi}[/bold]\n"
        f"Total Tiket Terjual   : {total_tiket}\n"
        f"Total Dibatalkan      : {len(batal)}\n"
        f"Total Pembayaran Lunas: {len(lunas)}\n"
        f"Pendapatan Bersih     : Rp{pendapatan:,.0f}",
        title="[yellow]Laporan Pendapatan - ADMIN[/yellow]",
        border_style="yellow"
    ))

    if rute_data:
        tbl = Table(title="Rincian Per Rute")
        tbl.add_column("Rute",       style="cyan")
        tbl.add_column("Tiket",      style="white")
        tbl.add_column("Pendapatan", style="green")
        for rute, info in rute_data.items():
            tbl.add_row(rute, str(info["jumlah"]), f"Rp{info['pendapatan']:,.0f}")
        console.print(tbl)

# ═══════════════════════════════════════════════════════════════════════════════
# ═══ FITUR BARU ADMIN ═══════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

# ─── 1. KELOLA DATA JURUSAN ──────────────────────────────────────────────────
def kelola_jurusan():
    console.print(Panel.fit("[bold cyan]KELOLA DATA JURUSAN[/bold cyan]"))
    
    while True:
        print("\n[1] Lihat Semua Jurusan")
        print("[2] Tambah Jurusan Baru")
        print("[3] Edit Jurusan")
        print("[4] Hapus Jurusan")
        print("[5] Edit Harga Tiket")
        print("[6] Kembali")
        
        pilih = input("\nPilih Menu : ")
        
        if pilih == "1":
            tampil_jurusan()
        
        elif pilih == "2":
            kode = input("Kode Jurusan (misal: YJ06) : ").upper()
            if kode in jurusan:
                print(Fore.RED + "Kode jurusan sudah ada!")
                continue
            
            rute = input("Rute (misal: Yogyakarta -> Jakarta) : ")
            ekonomi = int(input("Harga Ekonomi : "))
            eksekutif = int(input("Harga Eksekutif : "))
            vip = int(input("Harga VIP : "))
            
            jadwal_input = input("Jadwal (pisahkan dengan koma, misal: 05:00,08:00,11:00) : ")
            jadwal = [j.strip() for j in jadwal_input.split(",")]
            
            jurusan[kode] = {
                "rute": rute,
                "Ekonomi": ekonomi,
                "Eksekutif": eksekutif,
                "VIP": vip,
                "jadwal": jadwal
            }
            
            print(Fore.GREEN + f"Jurusan {kode} berhasil ditambahkan!")
        
        elif pilih == "3":
            print("\nJurusan yang tersedia:")
            for k in jurusan.keys():
                print(f"  {k}")
            
            kode = input("Kode Jurusan yang akan diedit : ").upper()
            if kode not in jurusan:
                print(Fore.RED + "Kode jurusan tidak ditemukan!")
                continue
            
            print("\n[1] Edit Rute")
            print("[2] Edit Jadwal")
            pilih_edit = input("Pilih : ")
            
            if pilih_edit == "1":
                rute_baru = input("Rute baru : ")
                jurusan[kode]["rute"] = rute_baru
                print(Fore.GREEN + "Rute berhasil diupdate!")
            
            elif pilih_edit == "2":
                jadwal_input = input("Jadwal baru (pisahkan dengan koma) : ")
                jadwal = [j.strip() for j in jadwal_input.split(",")]
                jurusan[kode]["jadwal"] = jadwal
                print(Fore.GREEN + "Jadwal berhasil diupdate!")
        
        elif pilih == "4":
            print("\nJurusan yang tersedia:")
            for k in jurusan.keys():
                print(f"  {k}")
            
            kode = input("Kode Jurusan yang akan dihapus : ").upper()
            if kode not in jurusan:
                print(Fore.RED + "Kode jurusan tidak ditemukan!")
                continue
            
            confirm = input(f"Yakin hapus jurusan {kode}? (ya/tidak) : ").lower()
            if confirm == "ya":
                del jurusan[kode]
                print(Fore.GREEN + "Jurusan berhasil dihapus!")
            else:
                print(Fore.YELLOW + "Penghapusan dibatalkan.")
        
        elif pilih == "5":
            print("\nJurusan yang tersedia:")
            for k in jurusan.keys():
                print(f"  {k}")
            
            kode = input("Kode Jurusan : ").upper()
            if kode not in jurusan:
                print(Fore.RED + "Kode jurusan tidak ditemukan!")
                continue
            
            print("\nHarga Saat Ini:")
            print(f"  Ekonomi : Rp{jurusan[kode]['Ekonomi']:,}")
            print(f"  Eksekutif : Rp{jurusan[kode]['Eksekutif']:,}")
            print(f"  VIP : Rp{jurusan[kode]['VIP']:,}")
            
            print("\n[1] Edit Ekonomi")
            print("[2] Edit Eksekutif")
            print("[3] Edit VIP")
            pilih_harga = input("Pilih : ")
            
            if pilih_harga == "1":
                harga_baru = int(input("Harga Ekonomi baru : "))
                jurusan[kode]["Ekonomi"] = harga_baru
                print(Fore.GREEN + "Harga berhasil diupdate!")
            elif pilih_harga == "2":
                harga_baru = int(input("Harga Eksekutif baru : "))
                jurusan[kode]["Eksekutif"] = harga_baru
                print(Fore.GREEN + "Harga berhasil diupdate!")
            elif pilih_harga == "3":
                harga_baru = int(input("Harga VIP baru : "))
                jurusan[kode]["VIP"] = harga_baru
                print(Fore.GREEN + "Harga berhasil diupdate!")
        
        elif pilih == "6":
            break
        else:
            print(Fore.RED + "Menu tidak tersedia")

# ─── 2. VERIFIKASI PEMBAYARAN ────────────────────────────────────────────────
def verifikasi_pembayaran():
    console.print(Panel.fit("[bold cyan]VERIFIKASI PEMBAYARAN[/bold cyan]"))
    
    pending = [x for x in transaksi if x.get("pembayaran") == "PENDING" and x["status"] == "AKTIF"]
    
    if not pending:
        print(Fore.YELLOW + "Tidak ada pembayaran yang pending.")
        return
    
    print("\nDaftar Pembayaran yang Pending:\n")
    for i, d in enumerate(pending, 1):
        print(f"{i}. Resi: {d['resi']} | Nama: {d['nama']} | Total: Rp{d['total']:,.0f} | Metode: {d['metode']}")
    
    nomor = input("\nMasukkan Nomor Resi untuk diverifikasi : ").strip()
    
    tiket_ditemukan = None
    for d in transaksi:
        if d["resi"] == nomor and d.get("pembayaran") == "PENDING":
            tiket_ditemukan = d
            break
    
    if not tiket_ditemukan:
        print(Fore.RED + "Resi tidak ditemukan atau sudah lunas!")
        return
    
    console.print(Panel(
        f"Resi       : {tiket_ditemukan['resi']}\n"
        f"Nama       : {tiket_ditemukan['nama']}\n"
        f"Rute       : {tiket_ditemukan['rute']}\n"
        f"Metode     : {tiket_ditemukan['metode']}\n"
        f"Total      : Rp{tiket_ditemukan['total']:,.0f}\n"
        f"Status     : {tiket_ditemukan.get('pembayaran')}",
        title="Detail Pembayaran", border_style="yellow"
    ))
    
    confirm = input("Konfirmasi pembayaran lunas? (ya/tidak) : ").lower()
    
    if confirm == "ya":
        tiket_ditemukan["pembayaran"] = "LUNAS"
        loading("Memperbarui status pembayaran")
        print(Fore.GREEN + f"Pembayaran untuk resi {nomor} berhasil diverifikasi!")
        
        # Email notifikasi pembayaran diterima
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = f"Verifikasi Pembayaran Aurora Buslines - {tiket_ditemukan['resi']}"
            msg["From"] = EMAIL_PENGIRIM
            msg["To"] = tiket_ditemukan["gmail"]
            
            isi_html = f"""
            <html><body style="font-family:Arial; background:#f4f4f4; padding:20px;">
            <div style="max-width:500px; background:white; border-radius:10px;
                        padding:24px; margin:auto; border-top:5px solid #059669;">
                <h2 style="color:#059669;">Aurora Buslines - Pembayaran Dikonfirmasi</h2>
                <p>Halo <b>{tiket_ditemukan['nama']}</b>, pembayaran kamu telah berhasil dikonfirmasi!</p>
                <hr>
                <table width="100%" cellpadding="6">
                    <tr><td><b>No. Resi</b></td><td>{tiket_ditemukan['resi']}</td></tr>
                    <tr><td><b>Rute</b></td><td>{tiket_ditemukan['rute']}</td></tr>
                    <tr><td><b>Metode Pembayaran</b></td><td>{tiket_ditemukan['metode']}</td></tr>
                    <tr style="background:#d1fae5;">
                        <td><b>Total Bayar</b></td>
                        <td><b style="color:#059669;">Rp{tiket_ditemukan['total']:,.0f}</b></td>
                    </tr>
                    <tr><td><b>Status</b></td><td><b style="color:#059669;">LUNAS</b></td></tr>
                </table>
                <hr>
                <p style="font-size:12px; color:gray;">
                    Tiket kamu sudah siap digunakan. Silakan tunjukkan nomor resi saat check-in.
                </p>
            </div>
            </body></html>
            """
            msg.attach(MIMEText(isi_html, "html"))
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_PENGIRIM, APP_PASSWORD)
                server.sendmail(EMAIL_PENGIRIM, tiket_ditemukan["gmail"], msg.as_string())
            print(Fore.GREEN + f"Email verifikasi dikirim ke {tiket_ditemukan['gmail']}")
        except Exception as e:
            print(Fore.YELLOW + f"Email gagal terkirim: {e}")
    else:
        print(Fore.YELLOW + "Verifikasi dibatalkan.")

# ─── 3. REFUND & RETUR TIKET (ADMIN) ─────────────────────────────────────────
def refund_retur_tiket():
    console.print(Panel.fit("[bold red]REFUND & RETUR TIKET[/bold red]"))
    
    aktif = [x for x in transaksi if x["status"] == "AKTIF"]
    
    if not aktif:
        print(Fore.YELLOW + "Tidak ada tiket aktif untuk diretur.")
        return
    
    print("\nDaftar Tiket Aktif:\n")
    for i, d in enumerate(aktif, 1):
        print(f"{i}. Resi: {d['resi']} | Nama: {d['nama']} | Total: Rp{d['total']:,.0f}")
    
    nomor = input("\nMasukkan Nomor Resi untuk diretur : ").strip()
    
    tiket_ditemukan = None
    for d in transaksi:
        if d["resi"] == nomor and d["status"] == "AKTIF":
            tiket_ditemukan = d
            break
    
    if not tiket_ditemukan:
        print(Fore.RED + "Resi tidak ditemukan atau tiket sudah dibatalkan!")
        return
    
    console.print(Panel(
        f"Resi       : {tiket_ditemukan['resi']}\n"
        f"Nama       : {tiket_ditemukan['nama']}\n"
        f"Rute       : {tiket_ditemukan['rute']}\n"
        f"Total      : Rp{tiket_ditemukan['total']:,.0f}\n"
        f"Pembayaran : {tiket_ditemukan.get('pembayaran')}",
        title="Detail Tiket", border_style="yellow"
    ))
    
    print("\n[1] Refund 100% (Pembatalan)")
    print("[2] Refund 50% (Perubahan Jadwal)")
    print("[3] Refund Custom")
    print("[4] Batal")
    
    pilih = input("Pilih Tipe Refund : ")
    
    nominal_refund = 0
    alasan = ""
    
    if pilih == "1":
        nominal_refund = tiket_ditemukan["total"]
        alasan = "Pembatalan Penuh"
    elif pilih == "2":
        nominal_refund = tiket_ditemukan["total"] * 0.5
        alasan = "Perubahan Jadwal"
    elif pilih == "3":
        nominal_refund = int(input("Masukkan nominal refund : "))
        alasan = input("Alasan refund : ")
        if nominal_refund > tiket_ditemukan["total"]:
            print(Fore.RED + "Nominal refund melebihi total tiket!")
            return
    elif pilih == "4":
        print(Fore.YELLOW + "Refund dibatalkan.")
        return
    else:
        print(Fore.RED + "Pilihan tidak valid")
        return
    
    confirm = input(f"Konfirmasi refund Rp{nominal_refund:,.0f}? (ya/tidak) : ").lower()
    
    if confirm == "ya":
        tiket_ditemukan["status"] = "BATAL"
        kursi_terpakai.discard(tiket_ditemukan["kursi"])
        
        refund_record = {
            "resi": tiket_ditemukan["resi"],
            "nama": tiket_ditemukan["nama"],
            "gmail": tiket_ditemukan["gmail"],
            "alasan": alasan,
            "nominal_refund": nominal_refund,
            "total_awal": tiket_ditemukan["total"],
            "waktu_refund": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        refund_history.append(refund_record)
        
        loading("Memproses refund")
        print(Fore.GREEN + f"Refund sebesar Rp{nominal_refund:,.0f} berhasil diproses!")
        
        loading("Mengirim email refund")
        kirim_email_refund(tiket_ditemukan, nominal_refund)
    else:
        print(Fore.YELLOW + "Refund dibatalkan.")

def lihat_history_refund():
    if not refund_history:
        print(Fore.YELLOW + "Belum ada history refund.")
        return
    
    table = Table(title="History Refund")
    table.add_column("Resi",   style="cyan")
    table.add_column("Nama",   style="white")
    table.add_column("Alasan", style="yellow")
    table.add_column("Nominal", style="green")
    table.add_column("Waktu",  style="magenta")
    
    for r in refund_history:
        table.add_row(
            r["resi"], r["nama"], r["alasan"],
            f"Rp{r['nominal_refund']:,.0f}", r["waktu_refund"]
        )
    
    console.print(table)

# ─── 4. MANAJEMEN KURSI ──────────────────────────────────────────────────────
def manajemen_kursi():
    console.print(Panel.fit("[bold cyan]MANAJEMEN KURSI[/bold cyan]"))
    
    while True:
        print("\n[1] Lihat Kursi Terpakai")
        print("[2] Lihat Kursi Tersedia")
        print("[3] Reset Kursi")
        print("[4] Blokir Kursi (Maintenance)")
        print("[5] Unblock Kursi")
        print("[6] Statistik Kursi")
        print("[7] Kembali")
        
        pilih = input("\nPilih Menu : ")
        
        if pilih == "1":
            if not kursi_terpakai:
                print(Fore.YELLOW + "Tidak ada kursi yang terpakai.")
            else:
                print("\n[bold yellow]Kursi Terpakai:[/bold yellow]")
                kursi_list = sorted(list(kursi_terpakai))
                for i in range(0, len(kursi_list), 8):
                    print("  " + "  |  ".join(kursi_list[i:i+8]))
                print(f"\nTotal: {len(kursi_terpakai)} kursi")
        
        elif pilih == "2":
            semua_kursi = [f"{b}{i}" for b in ["A", "B", "C", "D"] for i in range(1, 5)]
            tersedia = [k for k in semua_kursi if k not in kursi_terpakai]
            
            if not tersedia:
                print(Fore.RED + "Semua kursi telah terpakai!")
            else:
                print("\n[bold green]Kursi Tersedia:[/bold green]")
                for i in range(0, len(tersedia), 8):
                    print("  " + "  |  ".join(tersedia[i:i+8]))
                print(f"\nTotal: {len(tersedia)} kursi")
        
        elif pilih == "3":
            confirm = input("Yakin reset semua kursi? (ya/tidak) : ").lower()
            if confirm == "ya":
                kursi_terpakai.clear()
                print(Fore.GREEN + "Semua kursi berhasil direset!")
            else:
                print(Fore.YELLOW + "Reset dibatalkan.")
        
        elif pilih == "4":
            kursi = input("Masukkan kursi yang akan diblokir (misal: A1, B2) : ").upper()
            if kursi in kursi_terpakai:
                print(Fore.YELLOW + "Kursi sudah terpakai, tidak bisa diblokir.")
            else:
                kursi_terpakai.add(kursi)
                print(Fore.GREEN + f"Kursi {kursi} berhasil diblokir (Maintenance).")
        
        elif pilih == "5":
            kursi = input("Masukkan kursi yang akan diunblock (misal: A1, B2) : ").upper()
            if kursi not in kursi_terpakai:
                print(Fore.RED + "Kursi tidak ditemukan di daftar terblokir.")
            else:
                kursi_terpakai.discard(kursi)
                print(Fore.GREEN + f"Kursi {kursi} berhasil diunblock.")
        
        elif pilih == "6":
            semua_kursi = [f"{b}{i}" for b in ["A", "B", "C", "D"] for i in range(1, 5)]
            total_kursi = len(semua_kursi)
            terpakai = len(kursi_terpakai)
            tersedia = total_kursi - terpakai
            persen_pakai = (terpakai / total_kursi * 100) if total_kursi > 0 else 0
            
            console.print(Panel(
                f"[bold]Total Kursi[/bold]      : {total_kursi}\n"
                f"Kursi Terpakai     : {terpakai} ({persen_pakai:.1f}%)\n"
                f"Kursi Tersedia     : {tersedia} ({100-persen_pakai:.1f}%)",
                title="Statistik Kursi", border_style="cyan"
            ))
        
        elif pilih == "7":
            break
        else:
            print(Fore.RED + "Menu tidak tersedia")

# ═══════════════════════════════════════════════════════════════════════════════
# ═══ FITUR BARU USER ═══════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════════════════════

# ─── REFUND TIKET (USER) ─────────────────────────────────────────────────────
def refund_tiket_user():
    console.print(Panel.fit("[bold red]AJUKAN REFUND TIKET[/bold red]"))
    
    aktif = [x for x in transaksi if x["status"] == "AKTIF"]
    
    if not aktif:
        print(Fore.YELLOW + "Kamu tidak memiliki tiket aktif untuk diretur.")
        return
    
    print("\nDaftar Tiket Aktif Kamu:\n")
    for i, d in enumerate(aktif, 1):
        print(f"{i}. Resi: {d['resi']} | Rute: {d['rute']} | Total: Rp{d['total']:,.0f}")
    
    nomor = input("\nMasukkan Nomor Resi untuk diretur : ").strip()
    
    tiket_ditemukan = None
    for d in transaksi:
        if d["resi"] == nomor and d["status"] == "AKTIF":
            tiket_ditemukan = d
            break
    
    if not tiket_ditemukan:
        print(Fore.RED + "Resi tidak ditemukan atau tiket sudah dibatalkan!")
        return
    
    console.print(Panel(
        f"Resi       : {tiket_ditemukan['resi']}\n"
        f"Rute       : {tiket_ditemukan['rute']}\n"
        f"Jadwal     : {tiket_ditemukan['jadwal']}\n"
        f"Kursi      : {tiket_ditemukan['kursi']}\n"
        f"Total      : Rp{tiket_ditemukan['total']:,.0f}\n"
        f"Pembayaran : {tiket_ditemukan.get('pembayaran')}",
        title="Detail Tiket", border_style="yellow"
    ))
    
    print("\n[bold cyan]Pilih Alasan Refund:[/bold cyan]")
    print("1. Sakit/Darurat")
    print("2. Ubah Jadwal Perjalanan")
    print("3. Alasan Lain")
    
    pilih_alasan = input("\nPilih Alasan (1-3) : ")
    
    alasan_map = {
        "1": "Sakit/Darurat",
        "2": "Ubah Jadwal Perjalanan",
        "3": "Alasan Lain"
    }
    
    alasan = alasan_map.get(pilih_alasan, "Alasan Tidak Jelas")
    
    if pilih_alasan == "3":
        alasan_detail = input("Jelaskan alasan refund : ")
        alasan = f"Alasan Lain - {alasan_detail}"
    
    # Default 50% refund untuk user, bisa custom request
    print(f"\nNominal Standar: Rp{tiket_ditemukan['total'] * 0.5:,.0f} (50%)")
    print("Atau kamu bisa request custom nominal refund")
    
    pilih_nominal = input("Gunakan standar atau custom? (standar/custom) : ").lower()
    
    if pilih_nominal == "custom":
        try:
            nominal_request = int(input("Nominal refund yang diminta : "))
            if nominal_request > tiket_ditemukan['total']:
                print(Fore.RED + "Nominal tidak boleh melebihi total tiket!")
                return
            if nominal_request <= 0:
                print(Fore.RED + "Nominal harus lebih dari 0!")
                return
        except ValueError:
            print(Fore.RED + "Input tidak valid!")
            return
    else:
        nominal_request = tiket_ditemukan['total'] * 0.5
    
    console.print(Panel(
        f"[bold cyan]Ringkasan Refund:[/bold cyan]\n\n"
        f"Resi       : {tiket_ditemukan['resi']}\n"
        f"Alasan     : {alasan}\n"
        f"Total Awal : Rp{tiket_ditemukan['total']:,.0f}\n"
        f"Request    : Rp{nominal_request:,.0f}",
        title="Konfirmasi Refund", border_style="cyan"
    ))
    
    confirm = input("\nApakah data sudah benar? (ya/tidak) : ").lower()
    
    if confirm == "ya":
        # Tambah ke request refund
        refund_req = {
            "resi": tiket_ditemukan['resi'],
            "nama": tiket_ditemukan['nama'],
            "gmail": tiket_ditemukan['gmail'],
            "hp": tiket_ditemukan['hp'],
            "alasan": alasan,
            "nominal_request": nominal_request,
            "total_awal": tiket_ditemukan['total'],
            "waktu_request": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "status": "PENDING"  # Status approval oleh admin
        }
        refund_request.append(refund_req)
        
        loading("Mengirim permintaan refund")
        kirim_email_request_refund(tiket_ditemukan, alasan, nominal_request)
        
        console.print(Panel(
            f"[bold green]✓ Permintaan Refund Dikirim![/bold green]\n\n"
            f"Resi        : {tiket_ditemukan['resi']}\n"
            f"Status      : PENDING REVIEW\n"
            f"Nominal     : Rp{nominal_request:,.0f}\n\n"
            f"Admin kami akan mereview permintaan kamu dalam 1x24 jam.\n"
            f"Notifikasi akan dikirim ke email: {tiket_ditemukan['gmail']}",
            title="Refund Request Berhasil", border_style="green"
        ))
    else:
        print(Fore.YELLOW + "Refund dibatalkan.")

def lihat_status_refund_user():
    console.print(Panel.fit("[bold cyan]STATUS REFUND KAMU[/bold cyan]"))
    
    if not refund_request:
        print(Fore.YELLOW + "Kamu belum pernah mengajukan refund.")
        return
    
    print("\nDaftar Refund Request:\n")
    
    for i, req in enumerate(refund_request, 1):
        status_color = "🟡" if req["status"] == "PENDING" else "🟢" if req["status"] == "APPROVED" else "🔴"
        print(f"{i}. {status_color} Resi: {req['resi']} | Status: {req['status']} | Nominal: Rp{req['nominal_request']:,.0f}")
    
    pilih = input("\nPilih Nomor untuk melihat detail (atau tekan Enter untuk kembali) : ").strip()
    
    if pilih == "":
        return
    
    try:
        idx = int(pilih) - 1
        if 0 <= idx < len(refund_request):
            req = refund_request[idx]
            status_border = "yellow" if req["status"] == "PENDING" else "green" if req["status"] == "APPROVED" else "red"
            console.print(Panel(
                f"Resi          : {req['resi']}\n"
                f"Alasan        : {req['alasan']}\n"
                f"Total Awal    : Rp{req['total_awal']:,.0f}\n"
                f"Nominal Minta : Rp{req['nominal_request']:,.0f}\n"
                f"Status        : {req['status']}\n"
                f"Waktu Request : {req['waktu_request']}",
                title="Detail Refund Request", border_style=status_border
            ))
        else:
            print(Fore.RED + "Pilihan tidak valid!")
    except ValueError:
        print(Fore.RED + "Input tidak valid!")

# ─── Menu berdasarkan role ────────────────────────────────────────────────────

def menu_admin():
    while True:
        console.print(Panel(
            "[bold yellow][ MODE ADMIN ][/bold yellow]\n\n"
            "[1] Pesan Tiket\n"
            "[2] Cari Tiket\n"
            "[3] Daftar Jurusan & Jadwal\n"
            "[4] Lihat Semua Transaksi\n"
            "[5] Laporan Pendapatan\n"
            "[6] Batalkan Tiket\n"
            "[7] Kelola Data Jurusan\n"
            "[8] Verifikasi Pembayaran\n"
            "[9] Refund & Retur Tiket\n"
            "[10] Manajemen Kursi\n"
            "[11] Logout",
            title="Dashboard Admin",
            border_style="yellow"
        ))

        pilih = input("Pilih Menu : ")

        if   pilih == "1": pesan_tiket()
        elif pilih == "2": cari_tiket()
        elif pilih == "3": tampil_jurusan()
        elif pilih == "4": lihat_transaksi()
        elif pilih == "5": laporan()
        elif pilih == "6": batal_tiket()
        elif pilih == "7": kelola_jurusan()
        elif pilih == "8": verifikasi_pembayaran()
        elif pilih == "9": refund_retur_tiket()
        elif pilih == "10": manajemen_kursi()
        elif pilih == "11": break
        else: print(Fore.RED + "Menu tidak tersedia")

def menu_user():
    while True:
        console.print(Panel(
            "[1] Pesan Tiket\n"
            "[2] Cari Tiket\n"
            "[3] Daftar Jurusan & Jadwal\n"
            "[4] Lihat Semua Transaksi\n"
            "[5] Batalkan Tiket\n"
            "[6] Ajukan Refund Tiket\n"
            "[7] Lihat Status Refund\n"
            "[8] Logout",
            title="Dashboard",
            border_style="blue"
        ))

        pilih = input("Pilih Menu : ")

        if   pilih == "1": pesan_tiket()
        elif pilih == "2": cari_tiket()
        elif pilih == "3": tampil_jurusan()
        elif pilih == "4": lihat_transaksi()
        elif pilih == "5": batal_tiket()
        elif pilih == "6": refund_tiket_user()
        elif pilih == "7": lihat_status_refund_user()
        elif pilih == "8": break
        else: print(Fore.RED + "Menu tidak tersedia")

# ─── Main ─────────────────────────────────────────────────────────────────────

role = login()

if role == "admin":
    menu_admin()
else:
    menu_user()

print(Fore.CYAN + "Terima kasih telah menggunakan AURORA BUSLINES.")