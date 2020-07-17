from ininal import IninalScraper
import time

if __name__ == "__main__":
    _in = IninalScraper()
    while True:
        pg = _in.get_transactions_page()
        if pg:
            print("session status : OK")
            time.sleep(600)
        else:
            print("session ended !!")