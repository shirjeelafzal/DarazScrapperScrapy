import scrapy
from scrapy.http import Request
import pdb
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pdb
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import os
from ..items import DarazItem
import base64
import time

class CategoriesspiderSpider(scrapy.Spider):
    page_no = 2
    img_counter=1
    name = "categoriesspider"
    allowed_domains = ["www.daraz.pk"]
    start_urls = ["https://www.daraz.pk/"]

    def start_requests(self):
        self.path = "E:/MeissaSoft/DarazScrapper/chromedriver-win64/chromedriver.exe"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.service = ChromeService(self.path)
        self.driver = webdriver.Chrome(
            service=self.service, options=chrome_options)
        url = "https://www.daraz.pk/"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.maximize_window()
        wait = WebDriverWait(self.driver, 20)
        all_links = self.driver.find_elements(
            By.CSS_SELECTOR, '.lzd-site-menu-sub .lzd-site-menu-sub-item .lzd-site-menu-grand .lzd-site-menu-grand-item a')
        # for link in all_links:
        yield Request(url=all_links[0].get_attribute('href'), callback=self.parse_details)

    def parse_details(self, response):
        self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 5)
        cards = self.driver.find_elements(By.CSS_SELECTOR, '.gridItem--Yd0sa')
        for card in cards:
            items = DarazItem()
            product_name = card.find_element(
                By.CSS_SELECTOR, '.title--wFj93 a').text
            product_price = card.find_element(
                By.CSS_SELECTOR, '.price--NVB62 span').text
            
            # product_image = card.find_element(By.CSS_SELECTOR, '.mainPic--ehOdr img')
            # image_url = product_image.get_attribute('src')
            # pdb.set_trace()
            items['product_name'] = product_name
            items['product_price'] = product_price
            # items['image_urls'] = [self.convert_base64_to_img(image_url)]
            yield items

        # element = self.driver.find_element(
        #     By.CSS_SELECTOR, 'li.ant-pagination-item a[href*="page='+str(CategoriesspiderSpider.page_no)+'"]')
        # next_page_link = element.get_attribute('href')
        # if next_page_link is not None:
        #     CategoriesspiderSpider.page_no = CategoriesspiderSpider.page_no+1
        #     yield scrapy.Request(next_page_link, callback=self.parse_details)
        # else:
        #     CategoriesspiderSpider.page_no = 2
    # def convert_base64_to_img(self,base64_url):
    #     if ',' in base64_url:
    #         _, img_b = base64_url.split(',', 1)
    #         img_b64=img_b.replace(' ', '+')
    #         image_data= img_b64.replace('data:image/png;base64,', '')
    #         image=str(image_data)+"===" #adding padding
    #     else:
    #         img_b64=base64_url.replace(' ', '+')
    #         image_data= img_b64.replace('data:image/png;base64,', '')
    #         image=str(image_data)+"===" #adding padding
    #     image_name = f'{self.img_counter}.jpg'
    #     with open(os.path.join('images', image_name), 'wb') as img_file:
    #         img_file.write(base64.b64decode(image))
    #     self.img_counter+=1

