import random
from time import sleep
import time
from selenium import webdriver
import sys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
class colors:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CBLACK = '\33[30m'
    CRED = '\33[31m'
    CGREEN = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE = '\33[36m'
    CWHITE = '\33[37m'


color_random = [colors.CBLUE, colors.CVIOLET, colors.CWHITE, colors.OKBLUE, colors.CGREEN, colors.WARNING,
                colors.CRED, colors.CBEIGE]
random.shuffle(color_random)



def entryy():
    x = color_random[0] + """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢤⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡾⠿⢿⡀⠀⠀⠀⠀⣠⣶⣿⣷⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣦⣴⣿⡋⠀⠀⠈⢳⡄⠀⢠⣾⣿⠁⠈⣿⡆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⠿⠛⠉⠉⠁⠀⠀⠀⠹⡄⣿⣿⣿⠀⠀⢹⡇⠀⠀⠀
⠀⠀⠀⠀⠀⣠⣾⡿⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⣰⣏⢻⣿⣿⡆⠀⠸⣿⠀⠀⠀
⠀⠀⠀⢀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣆⠹⣿⣷⠀⢘⣿⠀⠀⠀
⠀⠀⢀⡾⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⠋⠉⠛⠂⠹⠿⣲⣿⣿⣧⠀⠀
⠀⢠⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣿⣿⣿⣷⣾⣿⡇⢀⠀⣼⣿⣿⣿⣧⠀
⠰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⡘⢿⣿⣿⣿⠀
⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣷⡈⠿⢿⣿⡆
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠁⢙⠛⣿⣿⣿⣿⡟⠀⡿⠀⠀⢀⣿⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣶⣤⣉⣛⠻⠇⢠⣿⣾⣿⡄⢻⡇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣦⣤⣾⣿⣿⣿⣿⣆⠁

\n"""
    for c in x:
        print(c, end='')
        sys.stdout.flush()
        sleep(0.00001)

# ... (The code above remains the same)

from queue import Queue

def check_lfi_vulnerability(url, payload_queue):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    vulnerable_urls = []

    try:
        while not payload_queue.empty():
            payload = payload_queue.get()
            target_url = url + payload.strip()
            browser.get(target_url)
            print(colors.CGREEN + "Testing: " + payload.strip())
            if "root:x:0:0:root" in browser.page_source:
                vulnerable_urls.append(target_url)
                print(colors.CRED + "Vuln Url: " + target_url)

        browser.close()
    except NoSuchElementException:
        pass

    browser.quit()
    return vulnerable_urls

entryy()
target_url = input(colors.CRED + "Example Url : https://example.com/carx/page1=\nEnter the target URL: ")
num_threads = int(input("Enter the number of threads for scanning [opt for threads within 5-20 using more may overload resources]: "))

if num_threads <= 0:
    print("Invalid number of threads. Exiting...")
else:
    import concurrent.futures

    with open("lfi.txt", "r", encoding="UTF-8") as file:
        payloads = file.readlines()

    payload_queue = Queue()
    for payload in payloads:
        payload_queue.put(payload)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(check_lfi_vulnerability, target_url, payload_queue) for _ in range(num_threads)]

        vulnerable_urls = []
        for future in concurrent.futures.as_completed(futures):
            vulnerable_urls.extend(future.result())

    if vulnerable_urls:
        print("LFI Vulnerability Found")
        print("Vulnerable URLs:")
        for url in vulnerable_urls:
            print(url)
    else:
        print("No LFI Vulnerability Found")
