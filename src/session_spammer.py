from ininal import IninalScraper
import time

if __name__ == "__main__":
    _in = IninalScraper()
    while True:
        pg = _in.get_transactions_page()
        if pg:
            print("session status : OK")
        else:
            print("session ended !!")
        time.sleep(600)