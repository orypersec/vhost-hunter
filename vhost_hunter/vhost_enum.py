import threading
from queue import Queue
import requests

def enum_vhost_worker(domain, protocol, queue, discovered_vhosts):
    while not queue.empty():
        subdomain = queue.get()
        try:
            response = requests.get(f"{protocol}://{subdomain}.{domain}", headers={"Host": f"{subdomain}.{domain}"}, timeout=3)
            if response.status_code == 200:
                print(f"[+] Found virtual host: {subdomain}.{domain}")
                discovered_vhosts.append(f"{subdomain}.{domain}")
        except requests.exceptions.RequestException as e:
            pass
        queue.task_done()


def enum_vhosts(domain, wordlist, use_https, num_threads=10):
    protocol = "https" if use_https else "http"
    discovered_vhosts = []
    subdomain_queue = Queue()

    with open(wordlist, "r") as file:
        for line in file:
            subdomain = line.strip()
            subdomain_queue.put(subdomain)

    threads = []
    for _ in range(num_threads):
        worker = threading.Thread(target=enum_vhost_worker, args=(domain, protocol, subdomain_queue, discovered_vhosts))
        worker.setDaemon(True)
        worker.start()
        threads.append(worker)

    while any(t.is_alive() for t in threads):
        try:
            for t in threads:
                t.join(timeout=0.1)
        except KeyboardInterrupt:
            print("\n[!] Keyboard Interrupt detected. Exiting...")
            break

    return discovered_vhosts



