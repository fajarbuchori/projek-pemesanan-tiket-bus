from datetime import datetime
import random
import time
from colorama import init, Fore
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

init(autoreset=True)
console = Console()

USERNAME = "admin"
PASSWORD = "12345"

transaksi = []
kursi_terpakai = set()

jurusan = {
    "SJ01": {"rute": "Surabaya -> Jakarta", "Ekonomi": 250000, "Eksekutif": 350000, "VIP": 500000},
    "JS02": {"rute": "Jakarta -> Surabaya", "Ekonomi": 250000, "Eksekutif": 350000, "VIP": 500000},
    "BJ03": {"rute": "Bandung -> Jakarta", "Ekonomi": 100000, "Eksekutif": 150000, "VIP": 250000},
    "JB04": {"rute": "Jakarta -> Bandung", "Ekonomi": 100000, "Eksekutif": 150000, "VIP": 250000},
    "YS05": {"rute": "Yogyakarta -> Surabaya", "Ekonomi": 150000, "Eksekutif": 250000, "VIP": 350000},
}

def loading(teks):
    print(teks, end="")
    for _ in range(5):
        time.sleep(0.2)
        print(".", end="", flush=True)
    print()

def generate_resi():
    return f"ABL-{random.randint(100000,999999)}"

def login():
    console.print(Panel.fit("[bold cyan]AURORA BUSLINES RESERVATION SYSTEM[/bold cyan]"))
    while True:
        user = input("ID Login : ")
        pw = input("Password : ")
        loading("Memverifikasi")
        if user == USERNAME and pw == PASSWORD:
            print(Fore.GREEN + "Login berhasil!")
            break
        else:
            print(Fore.RED + "ID atau Password salah!")

def tampil_jurusan():
    table = Table(title="Daftar Jurusan")
    table.add_column("Kode")
    table.add_column("Rute")
    for k, v in jurusan.items():
        table.add_row(k, v["rute"])
    console.print(table)

def tampil_kursi():
    console.print("[bold yellow]Kursi Tersedia[/bold yellow]")
    for b in ["A","B","C","D"]:
        row = []
        for i in range(1,5):
            k = f"{b}{i}"
            row.append("[X]" if k in kursi_terpakai else k)
        print(" ".join(row))

def pesan_tiket():
    nama = input("Nama : ")
    hp = input("Nomor HP : ")
    gmail = input("Gmail : ")


    tampil_jurusan()
    kode = input("Kode Jurusan : ").upper()

    if kode not in jurusan:
        print(Fore.RED + "Jurusan dan tujuan tidak sesuai!")
        return

    data_j = jurusan[kode]

    table = Table(title="Jenis Tiket")
    table.add_column("Pilihan")
    table.add_column("Harga")
    table.add_row("1. Ekonomi", f"Rp{data_j['Ekonomi']:,}")
    table.add_row("2. Eksekutif", f"Rp{data_j['Eksekutif']:,}")
    table.add_row("3. VIP", f"Rp{data_j['VIP']:,}")
    console.print(table)

    pilih = input("Pilih Tiket : ")

    if pilih == "1":
        jenis = "Ekonomi"
    elif pilih == "2":
        jenis = "Eksekutif"
    elif pilih == "3":
        jenis = "VIP"
    else:
        print("Pilihan tidak valid")
        return

    print("1. Economy Bus")
    print("2. Premium Bus")
    print("3. Executive Bus")

    bus_map = {"1":"Economy Bus","2":"Premium Bus","3":"Executive Bus"}
    bus = bus_map.get(input("Pilih Bus : "), "Economy Bus")

    jumlah = int(input("Jumlah Tiket : "))

    tampil_kursi()
    kursi = input("Pilih Kursi : ").upper()

    if kursi in kursi_terpakai:
        print(Fore.RED + "Kursi sudah digunakan!")
        return

    kursi_terpakai.add(kursi)

    harga = data_j[jenis]

    diskon = 10 if jumlah >= 5 else 5 if jumlah >= 3 else 0

    total = harga * jumlah
    total -= total * diskon / 100

    metode = input("Metode Bayar (Cash/Transfer/QRIS/E-Wallet): ")

    resi = generate_resi()

    data = {
        "resi": resi,
        "nama": nama,
        "rute": data_j["rute"],
        "kursi": kursi,
        "tiket": jenis,
        "bus": bus,
        "total": total,
        "jumlah": jumlah,
        "hp": hp,
        "gmail": gmail,
        "metode": metode,
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    transaksi.append(data)

    tiket = f"""
NO RESI      : {resi}
NAMA         : {nama}
NO HP        : {hp}
EMAIL        : {gmail}


RUTE         : {data_j['rute']}
BUS          : {bus}
TIKET        : {jenis}
KURSI        : {kursi}
JUMLAH       : {jumlah}

TOTAL BAYAR  : Rp{total:,.0f}

TIKET TIDAK DAPAT DIREFUND
"""
    console.print(Panel(tiket, title="AURORA BUSLINES", border_style="green"))

def cari_tiket():
    nomor = input("Masukkan Nomor Resi : ")

    for d in transaksi:
        if d["resi"] == nomor:

            tiket = f"""
NO RESI      : {d['resi']}
NAMA         : {d['nama']}
NO HP        : {d['hp']}
EMAIL        : {d['gmail']}

RUTE         : {d['rute']}
BUS          : {d['bus']}
TIKET        : {d['tiket']}
KURSI        : {d['kursi']}
JUMLAH       : {d['jumlah']}

METODE BAYAR : {d['metode']}
TOTAL BAYAR  : Rp{d['total']:,.0f}

WAKTU        : {d['waktu']}
"""

            console.print(
                Panel(
                    tiket,
                    title="🎫 Tiket Ditemukan",
                    border_style="green"
                )
            )

            return

    console.print(
        Panel(
            "Nomor resi tidak ditemukan",
            title="Error",
            border_style="red"
        )
    )

def lihat_transaksi():
    if not transaksi:
        print("Belum ada transaksi")
        return

    table = Table(title="Semua Transaksi")
    table.add_column("Resi")
    table.add_column("Nama")
    table.add_column("Rute")
    table.add_column("Total")

    for d in transaksi:
        table.add_row(d["resi"], d["nama"], d["rute"], f"Rp{d['total']:,.0f}")

    console.print(table)

def laporan():
    total_transaksi = len(transaksi)
    total_tiket = sum(x["jumlah"] for x in transaksi)
    pendapatan = sum(x["total"] for x in transaksi)

    console.print(Panel(
        f"Total Transaksi : {total_transaksi}\n"
        f"Total Tiket     : {total_tiket}\n"
        f"Pendapatan      : Rp{pendapatan:,.0f}",
        title="Laporan Pendapatan",
        border_style="yellow"
    ))

def menu():
    while True:
        console.print(Panel(
            "[1] Pesan Tiket\n[2] Cari Tiket\n[3] Daftar Jurusan\n[4] Lihat Semua Transaksi\n[5] Laporan Pendapatan\n[6] Logout",
            title="Dashboard",
            border_style="blue"
        ))

        pilih = input("Pilih Menu : ")

        if pilih == "1":
            pesan_tiket()
        elif pilih == "2":
            cari_tiket()
        elif pilih == "3":
            tampil_jurusan()
        elif pilih == "4":
            lihat_transaksi()
        elif pilih == "5":
            laporan()
        elif pilih == "6":
            break
        else:
            print(Fore.RED + "Menu tidak tersedia")

login()
menu()
print(Fore.CYAN + "Terima kasih telah menggunakan AURORA BUSLINES.")