# Proxy Checker

**Current Version**: 1.0
**Author**: Trix Cyrus  
**Copyright**: © 2024 Trixsec Org  
**Maintained**: Yes

A Python script to check the validity of proxies by testing them against a test URL. It supports HTTP, SOCKS4, and SOCKS5 proxy types and displays the working proxies along with their response time in milliseconds.

## Features:
- Test proxies from a provided list.
- Supports HTTP, SOCKS4, and SOCKS5 proxies.
- Concurrent proxy testing using asyncio for faster processing.
- Displays the working proxies along with the response time.
- Saves the valid proxies to a text file in `ip:port` format.

## Requirements:
- Python 3.7 or higher
- Dependencies can be installed from `requirements.txt`.

## Installation

1. Clone the repository or download the script.

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script with the following command:

   ```bash
   python proxy_checker.py --proxy-file <proxy_list.txt> --type http --timeout 10 --threads 5 --output-file working_proxies.txt
   ```

### Arguments:
- `--proxy-file`: The file containing a list of proxies (format: `ip:port` per line).
- `--type`: The proxy type (`http`, `socks4`, `socks5`).
- `--timeout`: The timeout duration (in seconds) for each proxy check (default: 10 seconds).


- `--threads`: The number of concurrent threads to use (default: 5).
- `--output-file`: The file to save working proxies (default: `proxy_output.txt`).

### Example Usage:

```bash
python proxy_checker.py --proxy-file proxies.txt --type http --timeout 10 --threads 500 --output-file working_proxies.txt

or 

python proxy_checker.py --proxy-file proxies.txt  --threads 500 
```

### Test Run

![Proxy-Checker](https://github.com/TrixSec/Proxy-Checker/blob/main/demo/testrun.jpg?raw=true)
