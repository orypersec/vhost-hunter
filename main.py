import argparse
from vhost_hunter.vhost_enum import enum_vhosts
from vhost_hunter.utils import save_results

def main():
    parser = argparse.ArgumentParser(description="Virtual Host Enumeration Tool")
    parser.add_argument("-d", "--domain", required=True, help="Target domain, e.g., example.com")
    parser.add_argument("-w", "--wordlist", default="wordlists/default-wordlist.txt", help="Path to a wordlist file containing subdomains (default: wordlist/default-wordlist.txt)")
    parser.add_argument("--https", action="store_true", help="Use HTTPS (default is HTTP)")
    parser.add_argument("-o", "--output", help="Path to the output file to save the discovered virtual hosts")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of threads for concurrent scanning (default: 10)")
    

    args = parser.parse_args()

    discovered_vhosts = enum_vhosts(args.domain, args.wordlist, args.https, num_threads=args.threads)

    if args.output:
        save_results(discovered_vhosts, args.output)
        print(f"[+] Results saved to: {args.output}")

if __name__ == "__main__":
    main()
