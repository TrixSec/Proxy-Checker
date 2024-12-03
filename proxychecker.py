import asyncio
import time
import aiohttp
import argparse
from rich.console import Console
from rich.progress import Progress
from termcolor import colored

banner = """
██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝     ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝      ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║       ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝        ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
"""
PROXYCHECKER_VERSION = "1.0"
AUTHOR = "Trix Cyrus"
COPYRIGHT = "Copyright © 2024 Trixsec Org"

def print_banner():
    print(colored(banner, 'cyan'))
    print(colored(f"Proxy Checker Version: {PROXYCHECKER_VERSION}", 'yellow')) 
    print(colored(f"Made by {AUTHOR}", 'yellow'))
    print(colored(COPYRIGHT, 'yellow'))

async def check_proxy(proxy, proxy_type, test_url, timeout, semaphore):
    async with semaphore:
        start_time = time.time()
        proxy_url = f"{proxy_type}://{proxy}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    test_url,
                    proxy=proxy_url,
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as response:
                    if response.status == 200:
                        response_time = int((time.time() - start_time) * 1000)
                        return proxy, response_time
        except (aiohttp.ClientError, asyncio.TimeoutError):
            pass
    return None

async def main(proxies, proxy_type, test_url, timeout, max_threads, output_file):
    semaphore = asyncio.Semaphore(max_threads)
    working_proxies = []

    console = Console()
    with Progress(console=console, expand=True) as progress:
        task_id = progress.add_task("[cyan]Testing proxies...", total=len(proxies))

        async def process_proxy(proxy):
            result = await check_proxy(proxy, proxy_type, test_url, timeout, semaphore)
            if result:
                proxy_address, response_time = result
                working_proxies.append(proxy_address)  
                console.log(f"[green]Working proxy: {proxy_address} ({response_time}ms)[/green]") 
            progress.update(task_id, advance=1)

        tasks = [process_proxy(proxy) for proxy in proxies]
        await asyncio.gather(*tasks)

    if working_proxies:
        with open(output_file, "w") as f:
            f.write("\n".join(working_proxies))
        console.log(f"[bold green]Saved {len(working_proxies)} working proxies to {output_file}[/bold green]")
    else:
        console.log("[bold red]No working proxies found.[/bold red]")

if __name__ == "__main__":
    print_banner()  
    parser = argparse.ArgumentParser(description="Proxy Checker Script")
    parser.add_argument("--proxy-file", required=True, help="File containing proxy list (ip:port per line)")
    parser.add_argument("--type", type=str, default="http", choices=["http", "socks4", "socks5"], 
                        help="Proxy type (default: http)")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout for each proxy check (default: 10 seconds)")
    parser.add_argument("--threads", type=int, default=5, help="Number of concurrent threads to use for proxy checks (default: 5)")
    parser.add_argument("--output-file", type=str, default="proxy_output.txt", help="File to save working proxies (default: proxy_output.txt)")
    args = parser.parse_args()

    with open(args.proxy_file, 'r') as file:
        proxies = [line.strip() for line in file]

    try:
        asyncio.run(main(proxies, args.type, "https://httpbin.org/ip", args.timeout, args.threads, args.output_file))
    except KeyboardInterrupt:
        print("\nProcess interrupted. Exiting...")

