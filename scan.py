import socket
import sys
import time
from datetime import datetime

try:
    from tqdm import tqdm
except ImportError:
    print("The 'tqdm' package is required. Install it with:")
    print("  pip install tqdm --break-system-packages")
    sys.exit(1)


# Terminal colors
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"


# Names of some commonly used ports
PORT_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 8080: "HTTP-Alt",
}


def show_banner():
    print(f"{CYAN}{'#' * 55}{RESET}")
    print(f"{CYAN}{BOLD}#{'  NETWORK PORT SCANNER'.center(53)}#{RESET}")
    print(f"{CYAN}{'#' * 55}{RESET}\n")


def get_ip(host):
    """Convert the hostname into an IP address."""
    try:
        return socket.gethostbyname(host)
    except socket.gaierror:
        return None


def check_port(address, port_number, timeout=0.5):
    """Check whether a TCP port accepts a connection."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.settimeout(timeout)
        result = connection.connect_ex((address, port_number))
        return result == 0


def scan_ports(address, first_port, last_port):
    found_ports = []
    port_count = last_port - first_port + 1

    print(f"\n{YELLOW}Scanning {address} — ports {first_port} to {last_port} "
          f"({port_count} ports){RESET}\n")

    timer_start = time.time()

    for current_port in tqdm(
        range(first_port, last_port + 1),
        desc="Scanning",
        unit="port",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} ports"
    ):
        if check_port(address, current_port):
            found_ports.append(current_port)

    scan_time = time.time() - timer_start

    return found_ports, scan_time, port_count


def show_results(address, found_ports, scan_time, port_count):
    print(f"\n{CYAN}{'-' * 55}{RESET}")
    print(f"{BOLD}SCAN SUMMARY{RESET}")
    print(f"{CYAN}{'-' * 55}{RESET}")
    print(f"Target        : {address}")
    print(f"Ports scanned : {port_count}")
    print(f"Open ports    : {len(found_ports)}")
    print(f"Time taken    : {scan_time:.2f} seconds")
    print(f"Scan finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{CYAN}{'-' * 55}{RESET}\n")

    if not found_ports:
        print(f"{RED}No open ports found in the given range.{RESET}\n")
        return

    print(f"{BOLD}{'PORT':<10}{'STATUS':<10}{'SERVICE (guess)':<20}{RESET}")
    print("-" * 40)

    for current_port in found_ports:
        service_name = PORT_SERVICES.get(current_port, "Unknown")
        print(f"{GREEN}{current_port:<10}{'OPEN':<10}{service_name:<20}{RESET}")

    print()


def main():
    show_banner()

    host = input(
        f"{BOLD}Enter target IP or hostname (or 'localhost'): {RESET}"
    ).strip()

    if not host:
        print(f"{RED}No target entered. Exiting.{RESET}")
        sys.exit(1)

    address = get_ip(host)

    if not address:
        print(
            f"{RED}Could not resolve '{host}'. Check the "
            f"hostname/IP and try again.{RESET}"
        )
        sys.exit(1)

    try:
        first_port = int(
            input(f"{BOLD}Start port (e.g. 1): {RESET}").strip()
        )
        last_port = int(
            input(f"{BOLD}End port (e.g. 1024): {RESET}").strip()
        )
    except ValueError:
        print(f"{RED}Ports must be numbers.{RESET}")
        sys.exit(1)

    if first_port < 1 or last_port > 65535 or first_port > last_port:
        print(
            f"{RED}Invalid port range. Must be between 1-65535, "
            f"start <= end.{RESET}"
        )
        sys.exit(1)

    found_ports, scan_time, port_count = scan_ports(
        address, first_port, last_port
    )

    show_results(address, found_ports, scan_time, port_count)


if __name__ == "__main__":
    main()
