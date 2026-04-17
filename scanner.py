import socket
from datetime import datetime

# COLORS
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"

PORT_LABELS = {
    21:   "FTP - File Transfer",
    22:   "SSH - Secure Shell",
    25:   "SMTP - Email Sending",
    53:   "DNS - Domain Lookup",
    80:   "HTTP - Web Traffic",
    443:  "HTTPS - Secure Web",
    3306: "MySQL - Database",
    3389: "RDP - Remote Desktop",
    8080: "HTTP Alt - Dev Server",
    8443: "HTTPS Alt - Secure Dev"
}

def scan_ports(host, ports):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = []
    open_count = 0
    closed_count = 0

    print(f"\n{CYAN} Scanning {host} at {timestamp}...{RESET}\n")

    for port in ports:
        s = socket.socket()
        s.settimeout(1)
        label = PORT_LABELS.get(port, "Unknown Service")

        try:
            s.connect((host, port))
            result = f"{GREEN}[OPEN]   Port {port} — {label}{RESET}"
            open_count += 1
        except:
            result = f"{RED}[closed] Port {port} — {label}{RESET}"
            closed_count += 1
        finally:
            s.close()

        print(f"  {result}")
        results.append(result)

    print(f"\n  {GREEN}Open: {open_count}{RESET} | {RED}Closed: {closed_count}{RESET}")

    with open("scan_results.txt", "w") as f:
        f.write(f"Scan Report — {host} — {timestamp}\n")
        f.write("=" * 45 + "\n")
        for r in results:
            f.write(r + "\n")
        f.write(f"\nOpen: {open_count} | Closed: {closed_count}\n")

    print(f"\n{YELLOW} Results saved to scan_results.txt{RESET}\n")

# USER INTERFACE
print(f"{CYAN}{'=' * 45}{RESET}")
print(f"{CYAN}   Ahsanul's Network Port Scanner{RESET}")
print(f"{CYAN}{'=' * 45}{RESET}")

host = input("\nEnter target host: ")

print("\nScan mode:")
print(f"  {YELLOW}1{RESET} — Common ports (quick)")
print(f"  {YELLOW}2{RESET} — Custom ports (manual)")

mode = input("\nChoose 1 or 2: ")

if mode == "1":
    ports_to_scan = [21, 22, 25, 53, 80, 443, 3306, 3389, 8080, 8443]
elif mode == "2":
    raw = input("Enter ports separated by commas (e.g. 22,80,443): ")
    ports_to_scan = [int(p.strip()) for p in raw.split(",")]
else:
    print("Invalid choice, running common ports by default")
    ports_to_scan = [21, 22, 25, 53, 80, 443, 3306, 3389, 8080, 8443]

scan_ports(host, ports_to_scan)
