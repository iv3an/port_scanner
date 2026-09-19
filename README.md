#  Network Port Scanner

A simple Python TCP port scanner that checks a target for open ports and displays the results in an easy-to-read terminal interface.

I built this project to practice **Python networking, sockets, TCP ports, and basic network reconnaissance**.

## Features

- Scan a custom range of TCP ports
- Accept IP addresses and hostnames
- Detect open ports
- Identify common services such as SSH, HTTP, HTTPS, and FTP
- Display scan progress with `tqdm`
- Show scan duration and a final summary
- Colored terminal output

## Built With

- `python`
- `socket`
- `tqdm`
- `datetime`
- `time`

## Usage

Install the required package:

```bash
pip install tqdm
```

Run the scanner:

```bash
python port_scanner.py
```

Then enter a target and port range:

```text
Enter target IP or hostname (or 'localhost'): localhost
Start port (e.g. 1): 1
End port (e.g. 1024): 1024
```

Example output:

```text
-------------------------------------------------------
SCAN SUMMARY
-------------------------------------------------------
Target        : 127.0.0.1
Ports scanned : 1024
Open ports    : 2
Time taken    : 4.21 seconds
-------------------------------------------------------

PORT      STATUS    SERVICE 
----------------------------------------
22        OPEN      SSH
80        OPEN      HTTP
```




## Future Improvements

- Multithreading for faster scans
- Banner grabbing
- Better service detection
- Export scan results to a file
- Command-line arguments


