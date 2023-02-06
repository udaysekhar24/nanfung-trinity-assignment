import os
import sys
import math
import logging
import pandas as pd
from bs4 import BeautifulSoup
import requests
import calendar
from datetime import datetime

RUN_DATE = datetime.today().strftime('%Y-%m-%d')
# Logging setup
logger = logging.getLogger(__name__)
logs_path = 'logs'
log_file_path = "{dir}/{filename}_{date}.log".format(date=RUN_DATE,
                                                     filename=os.path.splitext(os.path.basename(__file__))[0],
                                                     dir=logs_path)
if not os.path.exists(logs_path):
    os.makedirs(logs_path)

MAX_NUM_PAGES = 3
FETCH_SIZE = 40
PARENT_URL = "https://www.michaelkors.co.uk/handbags/view-all-handbags/_/N-10qbalf"
TARGET_DIR = 'processed/products'
DEFAULT_FILE_FORMAT = 'csv'
DEFAULT_TARGET = 'dev'


class Product(object):

    def __init__(self):
        self.product_brand = ''
        self.product_name = ''
        self.price = ''
        self.timestamp_ms = calendar.timegm(datetime.utcnow().utctimetuple())


class Assignment2Task:

    max_pages = MAX_NUM_PAGES
    env = DEFAULT_TARGET
    file_format = DEFAULT_FILE_FORMAT
    product_count = None

    def setup(self):
        # Setup starts
        arg_dict = dict()
        if len(sys.argv) > 2:
            for arg in sys.argv:
                arg_dict[arg.split('=')[0]] = arg.split("=")[1]
            if arg_dict.get("env"):
                env = arg_dict["env"]
                if env == "prod":
                    self.max_pages = int('inf')
            if arg_dict.get("format"):
                self.file_format = arg_dict["format"]
        logger.info("Running for target: " + str(self.env))
        logger.info("File format: " + str(self.file_format))
        # Setup ends

    @staticmethod
    def fetch_data(start):
        pagination_url_part = "&No={start}&Nrpp={size}"
        page_url = PARENT_URL + pagination_url_part.format(start=start, size=FETCH_SIZE)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0", }
        response = requests.get(page_url, headers=headers, timeout=120, allow_redirects=False)
        return response.content

    def parse_html(self, stream):
        try:
            soup = BeautifulSoup(stream, features="html.parser")
            if not self.product_count:
                try:
                    self.product_count = int(soup.find('div', class_='product-count-wrapper').span.get_text())
                    self.max_pages = math.ceil(self.product_count/FETCH_SIZE)
                    logger.info("************* Product count: " + str(self.product_count) + "*****************")
                except Exception as e:
                    logger.error("Could not find product count")

            product_lst = list()
            for panel in soup.find_all('ul', class_='description-panel text-left'):
                new_product = Product()
                new_product.product_brand = panel.find_next('li', class_='product-brand-container').a.get_text()
                new_product.product_name = panel.find_next('li', class_='product-name-container').a.get('title')
                new_product.price = panel.find_next('span', class_='ada-link productAmount').get_text()

                product_lst.append(new_product.__dict__)
            return product_lst
        except Exception as e:
            raise

    def run(self):
        logger.info("^^^^~~~~~~^^^^ Here are the dragons ^^^^~~~~~~^^^^")
        self.setup()
        logger.info("Web scraping " + str(self.max_pages) + " pages with fetch size " + str(FETCH_SIZE) + " from " + PARENT_URL)
        start = 0
        file_counter = 1
        while True:
            try:
                logger.info("For page start: " + str(start))

                logger.info(">>>> Fetching content")
                html_body = self.fetch_data(start=start)

                logger.info(">>>> Scraping")
                product_lst = self.parse_html(html_body)
                product_df = pd.DataFrame(product_lst)

                logger.info(">>>> Storing")
                target_path = TARGET_DIR + '/' + datetime.today().strftime('%Y-%m-%d')
                file_name = target_path + '/' + str(file_counter) + '.' + self.file_format
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                product_df.to_csv(file_name, index=None)
                file_counter = file_counter + 1
                start = start + FETCH_SIZE
                if start > self.product_count:
                    logger.info("Task completed.")
                    exit(0)

            except Exception as e:
                logger.warning("Failed for page start " + str(start) + str(e.__str__()))




