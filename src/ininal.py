import re
import requests
import json
from collections import namedtuple
from bs4 import BeautifulSoup
import traceback


def parse_creds(file):
    try:
        with open(file, encoding='utf8') as data:
            return json.load(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    except AttributeError:
        raise AttributeError("Unknown argument")
    except FileNotFoundError:
        raise FileNotFoundError("JSON file wasn't found")


def parse_cookie_file(cookies_file):
    cookies = {}
    for line in cookies_file.split("\n"):
        if not re.match(r'^\#', line):
            lineFields = line.strip().split('\t')
            cookies[lineFields[5]] = lineFields[6]
    return cookies


class IninalScraper:
    def __init__(self):
        config = parse_creds("creds.json")
        self.cookies = parse_cookie_file(config.cookies_file)
        self.card_token = config.card_token

    def get_transactions_page(self):
        url = f"https://onis.ininal.com/kart/hesap-hareketleri-filtre?token={self.card_token}"
        try:
            r = requests.get(url, cookies=self.cookies)
            if not "Hesap açın" in r.text:
                return r.text
            else:
                return None
        except Exception as e:
            print(f"An exception occured in 'get_transactions_page': {e}")
            traceback.print_exc()
            return None

    def get_all_transactions(self, start_date, end_date):
        if not start_date: start_date = "2013-06-16"
        if not end_date: end_date = "2020-12-31"
        url = f"https://onis.ininal.com/kart/hesap-hareketleri-filtre?token={self.card_token}&startDate={start_date}&endDate={end_date}"
        transactions = []
        try:
            r = requests.get(url, cookies=self.cookies)
            if not "Kayıt Bulunamadı" in r.text:
                soup = BeautifulSoup(r.text, "html.parser")
                page_count = int(soup.find_all('a')[-1].text)

                for pg in range(1, (page_count + 1)):
                    pg_url = f"{url}&page={pg}"
                    r = requests.get(pg_url, cookies=self.cookies)
                    soup = BeautifulSoup(r.text, "html.parser")
                    page_transacitons = [list_item for list_item in soup.find_all('li')[1:(-1 - page_count)]]

                    for tr in page_transacitons:
                        date = tr.find("div", {"class": "date"}).text.strip()
                        seller = tr.find("div", {"class": "seller"}).text
                        amount = tr.find("div", {"class": "amount"}).text.strip()
                        _type = tr.find("div", {"class": "type"}).text
                        reference = tr.find("div", {"class": "reference"}).text
                        tr_dict = {"date": date,
                                   "seller": seller,
                                   "amount": amount,
                                   "type": _type,
                                   "reference": reference}
                        transactions.append(tr_dict)
                return transactions
            else:
                return None
        except Exception as e:
            print(f"An exception occured : {e}")
            traceback.print_exc()
            return None
