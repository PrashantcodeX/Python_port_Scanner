import os
os.system('clear')

import socket
import threading
import time
from queue import Queue
import sys
from colorama import Fore, Style, init

# Initialize Colorama
init(autoreset=True)

# Banner for the tool
def print_banner():
    print(Fore.MAGENTA + """\

███████╗██████╗ ██████╗  ██████╗ ██████╗ 
██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
█████╗  ██████╔╝██████╔╝██║   ██║██████╔╝
██╔══╝  ██╔══██╗██╔══██╗██║   ██║██╔══██╗
███████╗██║  ██║██║  ██║╚██████╔╝██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
                                         

                                               
                                                
Welcome to ERROR - Online Port Scanner!""")
    print(Fore.GREEN + """
    MADE BY-  
    AYUSHMAN MISRA
    MOHIT MARWAH
    DRISHTI SINGHAL
    """)

# Threading setup
queue = Queue()
open_ports = []
closed_ports = []
scanning = True  # Global flag to manage the loading animation

# Function to scan a single port
def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            socket.setdefaulttimeout(1)  # Timeout for the connection
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)  # Port is open
            else:
                closed_ports.append(port)  # Port is closed
    except socket.error as e:
        print(Fore.RED + f"Error scanning port {port}: {e}")

# Thread function to process ports from the queue
def threader(ip):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port)
        queue.task_done()

# Loading animation
def loading_animation():
    symbols = ['-', '/', '|', '\\']
    idx = 0
    sys.stdout.write(Fore.CYAN + "Checking the ports... ")
    sys.stdout.flush()
    while scanning:
        sys.stdout.write(f"\b{symbols[idx % len(symbols)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.1)

# Main function to handle user input and scanning
def main():
    global scanning
    print_banner()  # Print the banner
    target_ip = input(Fore.YELLOW + "Enter the target IP address: ")
    
    # Validate IP address format
    if not validate_ip(target_ip):
        print(Fore.RED + "Invalid IP address format. Please enter a valid IP.")
        return

    try:
        start_port = int(input(Fore.YELLOW + "Enter the starting port number: "))
        end_port = int(input(Fore.YELLOW + "Enter the ending port number: "))
        num_threads = int(input(Fore.YELLOW + "Enter the number of threads (recommended 5-20): "))
    except ValueError:
        print(Fore.RED + "Please enter valid integer values for ports and threads.")
        return

    # Start loading animation in a separate thread
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()

    # Populate the queue with ports to scan
    for port in range(start_port, end_port + 1):
        queue.put(port)

    # Start threads for port scanning
    for _ in range(num_threads):
        thread = threading.Thread(target=threader, args=(target_ip,))
        thread.start()

    queue.join()  # Wait for all tasks in the queue to be completed

    # Stop the loading animation once scanning is complete
    scanning = False
    loading_thread.join()  # Ensure the loading animation thread finishes

    # Output open and closed ports
    if open_ports:
        print(Fore.GREEN + f"\nOpen ports detected on {target_ip}: {open_ports}")
    else:
        print(Fore.RED + f"\nNo open ports found on {target_ip}")

    if closed_ports:
        print(Fore.YELLOW + f"\nClosed ports on {target_ip}: {closed_ports}")

# Function to validate the IP address format
def validate_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not (0 <= int(part) <= 255):
            return False
    return True

if __name__ == "__main__":
    main()
