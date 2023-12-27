import requests
import argparse
import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


parser = argparse.ArgumentParser(
    description="Example: python3 script.py 13371337 1")
parser.add_argument("id", help="strawpoll.me poll ID")
parser.add_argument(
    "option", help="Poll checkbox number (1 for 1st option, 2 for 2nd, ...)")

parser.add_argument("-f", help="Voting frequency (in ms) (Default: 200ms)")
parser.add_argument("-m", help="Max threads (Default: 16)")
parser.add_argument("-p", action='store_true',
                    help="Use proxies (if the poll is doing an IP Check) - WARNING: Slow!")

args = parser.parse_args()
chrome_options = Options()

motd = ""


def prepare(args, motd):
    page = requests.get("https://proxy-daily.com").text
    page = page[page.find("centeredProxyList freeProxyStyle"):]
    page = page[page.find(">") + 1:]
    page = page[:page.find("</div>")]
    proxies = page.split("\n")

    # for i in proxies:
    #     vote(i, args)

    vote("54.144.134.157:80", args)
# modal-title
# Vote successful


def vote(proxy, args):

    options = Options()
    options.add_argument(f'--proxy-server={proxy}')

    url = "https://www.strawpoll.com/" + args.id

    print("Connecting to: " + url)
    # page = requests.get(url, headers=headers).text

    driver = webdriver.Chrome(options=options)

    # Load webpage
    driver.get(url)

    time.sleep(2)

    # Find the button using its id, name or xpath and then click it
    # Example, finding button by id:
    button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".strawpoll-options.text-lg.sm\\:text-base"))
    )
    buttons = button.find_elements(
        By.CSS_SELECTOR, ".cursor-pointer.h-5.w-5.disabled\\:opacity-50.custom-radio")

    buttons[0].click()

    time.sleep(3)

    vote = driver.find_elements(
        By.CSS_SELECTOR, ".strawpoll-button-primary.button.text-sm.custom-button.px-8")[1]

    vote.click()

    time.sleep(20)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    text = soup.get_text()

    pos = text.find("Vote successful")
    if pos != -1:
        print("success")
    else:
        print("fail")


prepare(args, motd)
