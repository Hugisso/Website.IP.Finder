import socket
import requests
import sys
import os

if os.name == "nt":
    os.system("")

# --- Colours (ANSI) ---
class C:
    RESET = "\033[0m"
    BOLD  = "\033[1m"
    CYAN  = "\033[96m"
    GREEN = "\033[92m"
    RED   = "\033[91m"
    YELLOW= "\033[93m"
    GRAY  = "\033[90m"


def print_banner():
    print(C.CYAN + C.BOLD + r"""
__        __     _              _             ___  ____    _____                _           
\ \      / /___ | |__   ___ (_)| |_   ___    |_ _||  _ \  |  ___|(_)  ____   _ | |  ___  ____ 
 \ \ /\ / // _ \| '_ \ / __|| || __| / _ \    | | | |_) | | |_   | | | '_ \ / _` | / _ \| '__|
  \ V  V /|  __/| |_) |\__ \| || |_ |  __/    |_| |  __/  |  _|  | | | | | | (_| ||  __/| |   
   \_/\_/  \___||_.__/ |___/|_| \__| \___|(_)|_ _||_|  (_)|_|    |_| |_| |_|\__,_| \___||_|
""" + C.RESET)
    print(C.GRAY + "        Author: Hugolosq   |   Type 'exit' or 'q' to quit" + C.RESET)
    print(C.GRAY + "─" * 80 + C.RESET)


def find_ip_and_location(website: str):
    print()
    print(C.YELLOW + f"[*] Looking up: {website}" + C.RESET)

    try:
        ip_address = socket.gethostbyname(website)
    except socket.gaierror:
        print(C.RED + f"[!] Invalid or non-existent website: '{website}'" + C.RESET)
        return

    print(C.GREEN + f"[+] IP address: {ip_address}" + C.RESET)

    # Geolocation
    try:
        url = (f"http://ip-api.com/json/{ip_address}"
               f"?fields=status,message,country,regionName,city,lat,lon")
        response = requests.get(url, timeout=5)
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(C.RED + f"[!] Connection error: {e}" + C.RESET)
        return
    except Exception as e:
        print(C.RED + f"[!] Unexpected error: {e}" + C.RESET)
        return

    if data.get("status") == "success":
        print(C.CYAN + "\n--- Approximate location ---" + C.RESET)
        print(f"  Country : {data.get('country', 'Unknown')}")
        print(f"  Region  : {data.get('regionName', 'Unknown')}")
        print(f"  City    : {data.get('city', 'Unknown')}")
        lat, lon = data.get("lat"), data.get("lon")
        print(f"  Coords  : {lat}, {lon}")
        if lat is not None and lon is not None:
            print(f"  Map     : https://www.google.com/maps?q={lat},{lon}")
    else:
        print(C.RED + f"[!] API error: {data.get('message', 'Unknown error')}" + C.RESET)

    print(C.GRAY + "─" * 80 + C.RESET)


def main():
    print_banner()

    if len(sys.argv) > 1:
        find_ip_and_location(sys.argv[1])
        input(C.GRAY + "\nPress Enter to exit..." + C.RESET)
        return

    while True:
        try:
            website = input(C.BOLD + "\nEnter website (e.g. google.com): " + C.RESET).strip()
        except (KeyboardInterrupt, EOFError):
            print("\n" + C.GRAY + "Done" + C.RESET)
            break

        if website.lower() in ("exit", "q", "quit", ""):
            print(C.GRAY + "Done" + C.RESET)
            break

        find_ip_and_location(website)


if __name__ == "__main__":
    main()