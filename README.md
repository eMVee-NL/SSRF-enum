# SSRF-enum

A high-precision automation tool designed to exploit Server-Side Request Forgery (SSRF) vulnerabilities using the `file://` protocol wrapper. This script leverages mathematical length filtering to reliably map out **hidden local files** and **nested directory structures** on a target server while completely eliminating common false positives caused by dynamic reflective web page reflections.

---

## Disclaimer
**Illegal activities are strictly prohibited.** This tool is developed and distributed solely for **educational purposes**, **Capture The Flag (CTF) challenges**, and **authorized security assessments** conducted with explicit, written permission from the system owner. The author (`eMVee`) assumes no liability for misuse, collateral damage, or illegal exploitation of this software.

---

## Key Features

* **File & Directory Discovery:** Specifically designed to hunt down files (using customizable extensions like `.php`) as well as local backend directory paths.
* **Fully Recursive Scanning Mode:** When a subfolder is discovered, the automation routing dynamically dives deeper into that branch, recursively fuzzing the entire local subdirectory tree.
* **Mathematical Baseline Calibration:** Eliminates false positives by performing a unique initial calibration request using a random UUID payload. It evaluates structural baseline response length, isolating changes to actual content delivery rather than reflecting the input text string.
* **Error & Network Crash Filtering:** Integrates rigid phrase exclusions to drop common loopback error wrappers (e.g., cURL rejections or missing file handlers), delivering an exceptionally clean output log.

---

## Usage

### Installation
Ensure you have Python 3 and the required dependencies installed:
```bash
pip install requests
```

### Execution
Run the script directly via your terminal:
```bash
python3 SSRF-enum.py
```

### Interactive Prompts
Upon launch, you will be prompted to supply the core configuration variables:
1. **Target SSRF URL:** The web address exposing the vulnerability (e.g., `http://10.0.2.21`).
2. **Vulnerable Parameter:** The specific POST field handling the URL payload injection (e.g., `report_url`).
3. **Wordlist Path:** Path to your scanning dictionary (e.g., `/usr/share/wordlists/dirb/common.txt`).
4. **Remote Directory Path:** The internal base directory you wish to map (e.g., `/var/www/html/`).
5. **File Extension:** The extension to append when hunting files (e.g., `.php` or leave empty for dictionary-exact folder hunting, it is allowed to use `/` as well for folders).
6. **Project Name:** Identifying string used to generate your output report.

---

## Reporting
All successfully identified items across every execution branch are compiled and dynamically exported. Reports are saved in your working directory adhering to a standardized timestamping classification architecture:
`yyyymmddhhmm-Output-<project_name>.txt`


## Screenshots

### Folder enumeration
<img width="928" height="796" alt="afbeelding" src="https://github.com/user-attachments/assets/23913f2c-322a-4bd7-af91-2a00462bb5af" />

### File enumeration
<img width="907" height="565" alt="afbeelding" src="https://github.com/user-attachments/assets/1932749e-5e33-435b-92e7-5c1c910d9197" />
