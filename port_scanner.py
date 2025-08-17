import socket
from concurrent.futures import ThreadPoolExecutor

# Daftar port penting dan rawan
risky_ports = {
    21:  ("FTP", "Transfer file tanpa enkripsi → rawan dicuri"),
    22:  ("SSH", "Remote login, penting diamankan"),
    23:  ("Telnet", "Login plaintext → rawan"),
    25:  ("SMTP", "Email relay, bisa disalahgunakan"),
    53:  ("DNS", "Bisa dijadikan target DDoS atau spoofing"),
    80:  ("HTTP", "Web server, sering diserang"),
    110: ("POP3", "Email tanpa enkripsi"),
    139: ("NetBIOS", "File sharing Windows, rawan malware"),
    143: ("IMAP", "Email tanpa enkripsi"),
    443: ("HTTPS", "Web aman, tetap bisa diserang jika service salah konfigurasi"),
    445: ("SMB", "File sharing Windows, rawan serangan WannaCry"),
    3389:("RDP", "Remote Desktop, sangat rawan serangan brute-force")
}

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((host, port))
        if result == 0:
            service, note = risky_ports[port]
            print(f"[+] Port {port} ({service}) TERBUKA → {note}", flush=True)
        sock.close()
    except Exception as e:
        print(f"[-] Error pada port {port}: {e}", flush=True)

def scan_host(host):
    print(f"\nMemulai pemindaian pada {host} untuk port penting dan rawan...\n", flush=True)

    # Cetak daftar port yang akan dipindai
    print(f"{'Port':<6} {'Layanan':<8} Risiko / Catatan")
    print("-"*60)
    for port, (service, note) in risky_ports.items():
        print(f"{port:<6} {service:<8} {note}")
    print("\nHasil pemindaian:\n")

    with ThreadPoolExecutor(max_workers=20) as executor:
        for port in risky_ports:
            executor.submit(scan_port, host, port)

def main():
    while True:
        host = input("\nMasukkan IP atau hostname target (atau ketik 'exit' untuk keluar): ")
        if host.lower() == "exit":
            print("Keluar dari port scanner.")
            break
        scan_host(host)

if __name__ == "__main__":
    main()
