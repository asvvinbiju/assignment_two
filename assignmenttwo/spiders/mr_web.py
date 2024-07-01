import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class MrWeb(scrapy.Spider):
    name = "mrweb"
    start_urls = ['https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723']
    properties_url = set()
    i = 0

    def __init__(self, *args, **kwargs):
        chrome_options = Options()
        chrome_options.binary_location = "/home/asvvinbiju/chrome/linux-114.0.5735.90/chrome-linux64/chrome"
        chrome_options.headless = False
        self.driver = webdriver.Chrome(service=ChromeService("/usr/local/bin/chromedriver"),options=chrome_options)
    
    def parse(self, response):
        self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
          
        wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="_2NPFF"]')))
        
        try:
            click_button = self.driver.find_element(By.CSS_SELECTOR, '[class="rui-apowA rui-htytx rui-UGVY0"]')
            if click_button:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", click_button)
        except:
            self.log("no")
            scrapy.Request(url=self.driver.current_url, callback=self.parse)
        else:
            self.log("yes")
            self.driver.execute_script("arguments[0].click();", click_button)
        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//figure[@class="_3UrC5"]/img')))
        except:
            pass
        time.sleep(5)
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[class="rui-apowA rui-htytx rui-UGVY0"]')))
        new_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8")
        all_properties = new_response.xpath('//a/@href').getall()
        for link in all_properties:
            if link.startswith('/item'):
                self.properties_url.add(f"https://www.olx.in{link}")
        for i in self.properties_url:
            yield scrapy.Request(url=i, callback=self.parse_properties)
        self.driver.quit()
        print(self.properties_url)
        print(len(self.properties_url))
        
    def parse_properties(self, response):
        property_id = response.xpath('//div[@class="_1-oS0"]/strong/text()').getall()
        propertyid = property_id[2].strip() if len(property_id) > 2 else None
        price = response.xpath('//section[@class="_8S0h4"]/span[@class="T8y-z"]/text()').get()
        currency = ""
        proprety_price = None
        if price:
            try:
                price_parts = price.split(maxsplit=1)
                currency = price_parts[0].strip()
                proprety_price = price_parts[1].strip()
            except:
                pass
        type = None
        bathrooms = None
        bedrooms = None
        details = response.xpath('//div[@class="_3nSm3"]/div/div')
        detail_type = details.xpath('//span[@class="_3V4pD"]/text()').getall()
        detail_ = details.xpath(f'//span[@class="B6X7c"]/text()').getall()
        for detail, value in zip(detail_type, detail_):
            if detail == "Type":
                type = value
            elif detail == "Bedrooms":
                bedrooms = value
            elif detail == "Bathrooms":
                bathrooms = value
        yield {
            "property_name": response.xpath('//h1[@class="_1hJph"]/text()').get(),
            "property_id": propertyid,
            "breadcrumbs": response.xpath('//ol[@class="rui-2Pidb"]/li/a/text()').getall(),
            "price": {
                "amount": proprety_price,
                "currency": currency,
            },
            "image_url": response.xpath('//div[@class="_23Jeb"]/figure/img/@src').get(),
            "description": response.xpath('//div[@class="rui-oN78c ok1RR"]/div/p/text()').get(),
            "seller_name": response.xpath('//div[@class="_1ibEV"]/div/a/@title').get(),
            "location": response.xpath('//div[@class="rui-oN78c"]/div/span/text()').get(),
            "property_type": type,
            "bathroom": bathrooms,
            "bedroom": bedrooms,
        }