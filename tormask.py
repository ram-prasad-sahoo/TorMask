import os
import sys
import subprocess
import time
from datetime import datetime
import requests
import json
from pyfiglet import figlet_format
import signal

# Terminal color settings
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
MAGENTA = '\033[0;35m'
NC = '\033[0m'

TOOL_NAME = "TorMasker"
VERSION = "1.0"

# Log file path for storing the IP change history
LOG_FILE_PATH = os.path.expanduser("~/Desktop/tor_ip_changed_log.txt")

# Ensure the directory exists
log_dir = os.path.dirname(LOG_FILE_PATH)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def print_colored(color, message):
    print(f"{color}{message}{NC}")

def print_banner():
    # Generate and display a stylish banner using pyfiglet
    banner_text = figlet_format("TOR-MASK", font="slant")
    print(f"{BLUE}{banner_text}{NC}")
    print(f"{BLUE}Author: RAM{NC}\n")

def check_root():
    if os.geteuid() != 0:
        print_colored(RED, "❌ Please run this script as root.")
        sys.exit(1)

def setup():
    distro = ""
    if os.path.exists("/etc/os-release"):
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    distro = line.split("=")[1].strip().strip('"').lower()
                    break
    else:
        print_colored(RED, "❌ Unsupported Linux distribution!")
        sys.exit(1)

    print_colored(BLUE, f"[*] Detected Linux Distro: {distro}")

    packages = ["curl", "tor", "jq", "xxd"]
    tor_group = ""

    if distro in ["arch", "manjaro", "blackarch"]:
        tor_group = "tor"
        print_colored(BLUE, "[*] Installing required packages using pacman...")
        subprocess.run(["pacman", "-S", "--needed", "--noconfirm"] + packages, check=True)
    elif distro in ["debian", "ubuntu", "kali", "parrot"]:
        tor_group = "debian-tor"
        print_colored(BLUE, "[*] Updating apt repositories and installing packages...")
        subprocess.run(["apt", "update"], check=True)
        subprocess.run(["apt", "install", "-y"] + packages, check=True)
    elif distro == "fedora":
        tor_group = "tor"
        print_colored(BLUE, "[*] Installing required packages using dnf...")
        subprocess.run(["dnf", "install", "-y"] + packages, check=True)
    elif distro.startswith("opensuse"):
        tor_group = "tor"
        print_colored(BLUE, "[*] Installing required packages using zypper...")
        subprocess.run(["zypper", "install", "-y"] + packages, check=True)
    else:
        print_colored(RED, "❌ Unsupported distro. Please install curl, tor, jq, and xxd manually.")
        sys.exit(1)

    group_exists = subprocess.run(["getent", "group", tor_group], stdout=subprocess.PIPE, text=True)
    if group_exists.returncode != 0:
        print_colored(BLUE, f"[*] Group '{tor_group}' not found, creating it...")
        subprocess.run(["groupadd", tor_group], check=True)

    try:
        current_user = os.getlogin()
    except Exception:
        current_user = os.environ.get("USER", "root")
    user_groups = subprocess.run(["groups", current_user], stdout=subprocess.PIPE, text=True).stdout
    if tor_group not in user_groups:
        print_colored(BLUE, f"[*] Adding user '{current_user}' to group '{tor_group}'...")
        subprocess.run(["usermod", "-aG", tor_group, current_user], check=True)
    else:
        print_colored(GREEN, f"[✓] User '{current_user}' is already a member of group '{tor_group}'.")

    torrc_file = "/etc/tor/torrc"
    try:
        with open(torrc_file, "r") as f:
            content = f.read()
    except Exception as e:
        print_colored(RED, f"❌ Error reading torrc file: {e}")
        sys.exit(1)

    needs_update = False
    if "ControlPort 9051" not in content:
        needs_update = True
    if "CookieAuthentication 1" not in content:
        needs_update = True
    if "CookieAuthFileGroupReadable 1" not in content:
        needs_update = True

    if needs_update:
        print_colored(BLUE, "[*] Updating torrc with required ControlPort settings...")
        try:
            with open(torrc_file, "a") as f:
                f.write("\n# Added by TorMasker automation script\n")
                f.write("ControlPort 9051\n")
                f.write("CookieAuthentication 1\n")
                f.write("CookieAuthFileGroupReadable 1\n")
            subprocess.run(["systemctl", "restart", "tor"], check=True)
        except Exception as e:
            print_colored(RED, f"❌ Failed to update torrc: {e}")
            sys.exit(1)
    else:
        print_colored(GREEN, "[✓] torrc already configured correctly. Skipping update.")

def get_auth_cookie():
    cookie_paths = [
        "/var/run/tor/control.authcookie",
        "/var/lib/tor/control.authcookie"
    ]
    for path in cookie_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    raw_cookie = f.read().strip()
                if len(raw_cookie) == 32:
                    return raw_cookie.hex()
                else:
                    print_colored(RED, f"Cookie from {path} has unexpected length: {len(raw_cookie)} bytes")
            except Exception as e:
                print_colored(RED, f"Error reading cookie from {path}: {e}")
    raise FileNotFoundError("Could not find a valid Tor authentication cookie at expected paths.")

def get_ip_location(ip):
    url = f"http://ip-api.com/json/{ip}"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("status") == "success":
            return data.get("country", "Unknown"), data.get("city", "Unknown")
        else:
            return "Unknown", "Unknown"
    except Exception:
        return "Unknown", "Unknown"

def ipchanger():
    try:
        cookie = get_auth_cookie()
    except Exception as e:
        print_colored(RED, f"Error retrieving auth cookie: {e}")
        return

    command = f"AUTHENTICATE {cookie}\r\nSIGNAL NEWNYM\r\nQUIT\r\n"
    try:
        proc = subprocess.run(
            ["nc", "127.0.0.1", "9051"],
            input=command,
            text=True,
            capture_output=True,
            check=True
        )
        output = proc.stdout
        if "515" in output:
            print_colored(RED, "Authentication error with Tor control port.")
    except subprocess.CalledProcessError as e:
        print_colored(RED, f"Error communicating with Tor control port: {e}")
        return

    proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050"
    }
    try:
        response = requests.get("https://check.torproject.org/api/ip", proxies=proxies, timeout=10)
        response.raise_for_status()
        ip = response.json().get("IP", "Unknown")
    except Exception as e:
        print_colored(RED, f"Error retrieving Tor IP: {e}")
        ip = "Unknown"

    country, city = get_ip_location(ip)
    log_message = f"{datetime.now()} - New Tor IP: {ip} | Country: {country} | City: {city}"

    # Print colorful output in the desired format
    print(f"{RED}--------------------------------------------------------{NC}")
    print(f"{CYAN}🕒  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{NC}")
    print(f"{GREEN}🌐  New Tor IP: {ip}{NC}")
    print(f"{YELLOW}📍  Location: {country}, {city}{NC}")
    print(f"{RED}--------------------------------------------------------{NC}")

    # Write to the log file
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(log_message + "\n")
        log_file.flush()

def handle_exit_signal(signum, frame):
    print_colored(YELLOW, "\n\n✅ IP changer stopped.")
    sys.exit(0)

def main():
    print_banner()

    # Set up signal handler for graceful exit on Ctrl+C
    signal.signal(signal.SIGINT, handle_exit_signal)

    # Get user input for interval
    while True:
        try:
            interval = int(input(f"{YELLOW}Enter time interval to change IP in seconds (default: 10): "))
            if interval <= 0:
                print_colored(RED, "❌ Please enter a positive number!")
                continue
            break
        except ValueError:
            print_colored(RED, "❌ Invalid input. Please enter a valid number.")

    if interval == 0:
        interval = 10

    print_colored(GREEN, f"⌛ IP will be changed every {interval} seconds!\n")
    print_colored(CYAN, "🚀 Starting IP changer...\n")
    print("-" * 50)

    while True:
        ipchanger()
        time.sleep(interval)

if __name__ == "__main__":
    check_root()
    setup()
    main()
