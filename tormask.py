import os
import sys
import subprocess
import time
from datetime import datetime
import requests
import json
from pyfiglet import figlet_format
import signal
import threading
from pathlib import Path

# Terminal color settings
BLUE = '\033[0;34m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
CYAN = '\033[0;36m'
MAGENTA = '\033[0;35m'
WHITE = '\033[1;37m'
GRAY = '\033[0;37m'
BOLD = '\033[1m'
NC = '\033[0m'

# Emoji and symbols for better UI
IP_EMOJI = "🌐"
LOCATION_EMOJI = "📍"
TIME_EMOJI = "⏰"
SUCCESS_EMOJI = "✅"
ERROR_EMOJI = "❌"
ARROW_EMOJI = "➤"

TOOL_NAME = "TorMasker"
VERSION = "2.0"
LOG_DIR = Path.home() / "tormasker_logs"
LOG_FILE = LOG_DIR / f"ip_changes_{datetime.now().strftime('%Y%m%d')}.log"

# Global variables
is_running = False
change_count = 0
start_time = None


def print_colored(color, message):
    print(f"{color}{message}{NC}")

def start_tor_service():
    try:
        subprocess.run(["service", "tor", "start"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_colored(GREEN, f"{SUCCESS_EMOJI} Tor service started.")
    except subprocess.CalledProcessError as e:
        print_colored(RED, f"{ERROR_EMOJI} Failed to start Tor service: {e}")
        sys.exit(1)

def stop_tor_service():
    try:
        subprocess.run(["service", "tor", "stop"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_colored(GREEN, f"{SUCCESS_EMOJI} Tor service stopped.")
    except subprocess.CalledProcessError as e:
        print_colored(RED, f"{ERROR_EMOJI} Failed to stop Tor service: {e}")

def print_banner():
    banner_text = figlet_format("TOR-MASK", font="slant")
    print(f"{CYAN}{banner_text}{NC}")
    print(f"{BLUE}{'=' * 60}{NC}")
    print(f"{WHITE}{BOLD}    Advanced Tor IP Changer with Location Detection{NC}")
    print(f"{YELLOW}    Author: RAM | Version: {VERSION}{NC}")
    print(f"{BLUE}{'=' * 60}{NC}\n")


def create_log_directory():
    """Create log directory if it doesn't exist"""
    LOG_DIR.mkdir(exist_ok=True)
    if not LOG_FILE.exists():
        with open(LOG_FILE, 'w') as f:
            f.write(f"# TorMasker IP Change Log - {datetime.now().strftime('%Y-%m-%d')}\n")
            f.write("# Timestamp | IP Address | Country | City | ISP\n")
            f.write("-" * 80 + "\n")


def log_ip_change(ip_info):
    """Log IP change to file"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} | {ip_info['ip']} | {ip_info['country']} | {ip_info['city']} | {ip_info['isp']}\n"

        with open(LOG_FILE, 'a') as f:
            f.write(log_entry)
    except Exception as e:
        print_colored(RED, f"Error writing to log file: {e}")


def get_location_info(ip_address):
    """Get detailed location information for an IP"""
    try:
        # Using multiple APIs for better reliability
        apis = [
            f"http://ip-api.com/json/{ip_address}",
            f"https://ipapi.co/{ip_address}/json/",
        ]

        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()

                    # Handle different API response formats
                    if 'ip-api.com' in api_url:
                        return {
                            'country': data.get('country', 'Unknown'),
                            'city': data.get('city', 'Unknown'),
                            'region': data.get('regionName', 'Unknown'),
                            'isp': data.get('isp', 'Unknown'),
                            'timezone': data.get('timezone', 'Unknown'),
                            'lat': data.get('lat', 0),
                            'lon': data.get('lon', 0)
                        }
                    else:  # ipapi.co format
                        return {
                            'country': data.get('country_name', 'Unknown'),
                            'city': data.get('city', 'Unknown'),
                            'region': data.get('region', 'Unknown'),
                            'isp': data.get('org', 'Unknown'),
                            'timezone': data.get('timezone', 'Unknown'),
                            'lat': data.get('latitude', 0),
                            'lon': data.get('longitude', 0)
                        }
            except:
                continue

        return {
            'country': 'Unknown',
            'city': 'Unknown',
            'region': 'Unknown',
            'isp': 'Unknown',
            'timezone': 'Unknown',
            'lat': 0,
            'lon': 0
        }
    except Exception as e:
        print_colored(RED, f"Error getting location info: {e}")
        return {
            'country': 'Unknown',
            'city': 'Unknown',
            'region': 'Unknown',
            'isp': 'Unknown',
            'timezone': 'Unknown',
            'lat': 0,
            'lon': 0
        }


def display_ip_info(ip_info, location_info):
    """Display IP and location information in a beautiful format"""
    global change_count
    change_count += 1

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"{BLUE}{'─' * 60}{NC}")
    print(f"{TIME_EMOJI} {WHITE}{BOLD}{timestamp}{NC}")
    print(f"{IP_EMOJI} {GREEN}New Tor IP: {YELLOW}{BOLD}{ip_info['ip']}{NC}")
    print(f"{LOCATION_EMOJI} {CYAN}Location: {WHITE}{location_info['city']}, {location_info['country']}{NC}")
    print(f"{ARROW_EMOJI} {MAGENTA}ISP: {WHITE}{location_info['isp']}{NC}")
    print(f"{ARROW_EMOJI} {GRAY}Region: {location_info['region']} | Timezone: {location_info['timezone']}{NC}")
    print(f"{ARROW_EMOJI} {YELLOW}Change #{change_count}{NC}")
    print(f"{BLUE}{'─' * 60}{NC}\n")


def check_root():
    if os.geteuid() != 0:
        print_colored(RED, f"{ERROR_EMOJI} Please run this script as root.")
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
        print_colored(RED, f"{ERROR_EMOJI} Unsupported Linux distribution!")
        sys.exit(1)

    print_colored(BLUE, f"[*] Detected Linux Distro: {distro}")

    packages = ["curl", "tor", "jq", "xxd", "netcat-traditional"]
    tor_group = ""

    if distro in ["arch", "manjaro", "blackarch"]:
        tor_group = "tor"
        print_colored(BLUE, "[*] Installing required packages using pacman...")
        subprocess.run(["pacman", "-S", "--needed", "--noconfirm"] + packages, check=True)
    elif distro in ["debian", "ubuntu", "kali", "parrot"]:
        tor_group = "debian-tor"
        print_colored(BLUE, "[*] Updating apt repositories and installing packages...")
        subprocess.run(["apt", "update"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
        print_colored(RED,
                      f"{ERROR_EMOJI} Unsupported distro. Please install curl, tor, jq, xxd, and netcat-traditional manually.")
        sys.exit(1)

    group_exists = subprocess.run(["getent", "group", tor_group], stdout=subprocess.PIPE, text=True)
    if group_exists.returncode != 0:
        print_colored(BLUE, f"[*] Group '{tor_group}' not found, creating it...")
        subprocess.run(["groupadd", tor_group], check=True)

    try:
        current_user = os.environ.get("SUDO_USER", os.getlogin())
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
        print_colored(RED, f"{ERROR_EMOJI} Error reading torrc file: {e}")
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

            print_colored(MAGENTA, "[*] Restarting Tor service to apply changes...")
            subprocess.run(["systemctl", "restart", "tor@default.service"], check=True)

        except Exception as e:
            print_colored(RED, f"{ERROR_EMOJI} Failed to update torrc: {e}")
            sys.exit(1)
    else:
        print_colored(GREEN, f"{SUCCESS_EMOJI} torrc already configured correctly. Skipping update.")


def get_auth_cookie_hex():
    cookie_paths = [
        "/var/run/tor/control.authcookie",
        "/var/lib/tor/control.authcookie"
    ]
    for path in cookie_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    return f.read().hex()
            except Exception as e:
                print_colored(RED, f"Error reading cookie from {path}: {e}")
    raise FileNotFoundError("Could not find a valid Tor authentication cookie at expected paths.")


def ipchanger():
    """Enhanced IP changer with location detection"""
    try:
        cookie_hex = get_auth_cookie_hex()
    except FileNotFoundError as e:
        print_colored(RED, f"Error: {e}")
        return False

    command = f"AUTHENTICATE {cookie_hex}\r\nSIGNAL NEWNYM\r\nQUIT\r\n"
    try:
        subprocess.run(
            ["nc", "127.0.0.1", "9051"],
            input=command,
            text=True,
            capture_output=True,
            check=True,
            timeout=5
        )
    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        print_colored(RED, f"Error communicating with Tor control port via nc: {e}")
        return False

    # Wait a moment for IP to change
    time.sleep(2)

    try:
        proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050"
        }
        response = requests.get("https://check.torproject.org/api/ip", proxies=proxies, timeout=10)
        response.raise_for_status()
        ip_info = response.json()
        ip_address = ip_info.get("IP", "Unknown")

        if ip_address == "Unknown":
            print_colored(RED, f"{ERROR_EMOJI} Failed to retrieve IP address")
            return False

    except Exception as e:
        print_colored(RED, f"Error retrieving Tor IP via requests: {e}")
        return False

    # Get location information
    location_info = get_location_info(ip_address)

    # Display information
    full_ip_info = {'ip': ip_address}
    display_ip_info(full_ip_info, location_info)

    # Log to file
    log_data = {
        'ip': ip_address,
        'country': location_info['country'],
        'city': location_info['city'],
        'isp': location_info['isp']
    }
    log_ip_change(log_data)

    return True


def show_statistics():
    """Show current session statistics"""
    if start_time:
        runtime = datetime.now() - start_time
        hours, remainder = divmod(runtime.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)

        print(f"\n{CYAN}{'=' * 50}{NC}")
        print(f"{WHITE}{BOLD}SESSION STATISTICS{NC}")
        print(f"{CYAN}{'=' * 50}{NC}")
        print(f"{YELLOW}Runtime: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}{NC}")
        print(f"{YELLOW}IP Changes: {change_count}{NC}")
        print(f"{YELLOW}Log File: {LOG_FILE}{NC}")
        print(f"{CYAN}{'=' * 50}{NC}\n")


def interactive_menu():
    """Show interactive commands during execution"""
    commands = [
        f"{YELLOW}Commands available during execution:{NC}",
        f"{GREEN}  s - Show statistics{NC}",
        f"{GREEN}  l - Show last 5 log entries{NC}",
        f"{GREEN}  q - Quit program{NC}",
        f"{GREEN}  Ctrl+C - Stop IP changer{NC}"
    ]

    for cmd in commands:
        print(cmd)
    print()


def show_recent_logs():
    """Show recent log entries"""
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()

        print(f"\n{MAGENTA}{'=' * 60}{NC}")
        print(f"{WHITE}{BOLD}RECENT IP CHANGES (Last 5){NC}")
        print(f"{MAGENTA}{'=' * 60}{NC}")

        # Show last 5 actual log entries (skip header lines)
        log_lines = [line for line in lines if not line.startswith('#') and not line.startswith('-')]
        recent_lines = log_lines[-5:] if len(log_lines) >= 5 else log_lines

        for line in recent_lines:
            if line.strip():
                print(f"{GRAY}{line.strip()}{NC}")

        print(f"{MAGENTA}{'=' * 60}{NC}\n")

    except Exception as e:
        print_colored(RED, f"Error reading log file: {e}")


def handle_exit_signal(signum, frame):
    global is_running
    is_running = False
    show_statistics()
    # 🔹 Stop Tor service before exiting
    stop_tor_service()
    print_colored(YELLOW, f"\n{SUCCESS_EMOJI} IP changer stopped gracefully.")
    print_colored(CYAN, f"Log file saved at: {LOG_FILE}")
    sys.exit(0)


def input_thread():
    """Handle user input during execution"""
    global is_running
    while is_running:
        try:
            cmd = input().strip().lower()
            if cmd == 's':
                show_statistics()
            elif cmd == 'l':
                show_recent_logs()
            elif cmd == 'q':
                handle_exit_signal(None, None)
        except (EOFError, KeyboardInterrupt):
            break


def main():
    global is_running, start_time

    print_banner()
    signal.signal(signal.SIGINT, handle_exit_signal)
    # 🔹 Start Tor service
    start_tor_service()

    # Create log directory and file
    create_log_directory()

    print_colored(GREEN, f"{SUCCESS_EMOJI} Log directory created at: {LOG_DIR}")
    print_colored(GREEN, f"{SUCCESS_EMOJI} Today's log file: {LOG_FILE}")
    print()

    try:
        interval_input = input(f"{YELLOW}Enter Tor IP change interval in seconds (default 10): {NC}")
        interval = int(interval_input) if interval_input else 10
        if interval <= 0:
            interval = 10
    except ValueError:
        interval = 10

    print_colored(GREEN, f"\n{SUCCESS_EMOJI} Starting Enhanced Tor IP changer every {interval} seconds...")
    interactive_menu()
    print("-" * 60)

    is_running = True
    start_time = datetime.now()

    # Start input handling thread
    input_handler = threading.Thread(target=input_thread, daemon=True)
    input_handler.start()

    # Perform initial IP change
    print_colored(CYAN, "🚀 Performing initial IP change...")
    ipchanger()

    while is_running:
        try:
            time.sleep(interval)
            if is_running:  # Check again in case it was changed during sleep
                ipchanger()
        except KeyboardInterrupt:
            handle_exit_signal(None, None)


if __name__ == "__main__":
    check_root()
    setup()


    main()
