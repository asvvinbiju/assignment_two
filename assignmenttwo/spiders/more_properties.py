import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time

class NewSpider(scrapy.Spider):
    name = "newspider"
    start_urls = ['https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723']
    
    visited_urls = set()

    def __init__(self, *args, **kwargs):
        chrome_options = Options()
        chrome_options.binary_location = "/home/asvvinbiju/chrome/linux-114.0.5735.90/chrome-linux64/chrome"
        chrome_options.headless = False
        self.driver = webdriver.Chrome(service=ChromeService("/usr/local/bin/chromedriver"),options=chrome_options)
    
    def parse(self, response):
        val = response.xpath('//span[@class="_2NPFF"]/text()')[1].get()
        self.driver.get(response.url)
        wait = WebDriverWait(self.driver, 10)
        try:
            # wait.until(
            #         EC.presence_of_element_located((By.CLASS_NAME, '_2cbZ2'))
            #     )
            wait.until(
                    EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
                )
            click_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
            )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", click_button)
            if val == ': Date Published':
                click_button.click()

            wait.until(
                EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
            )
            
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
        finally:
            try:
                new_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8")
                all_properties = new_response.xpath('//li[@class="_1DNjI"]/a/@href').getall()
                for link in all_properties:
                    self.visited_urls.add(f"https://www.olx.in/{link}")
                for i in self.visited_urls:
                    yield scrapy.Request(url=i, callback=self.parse_properties)
            except Exception as e:
                self.logger.error(f"Error Reading:{str(e)}")
            if len(self.visited_urls) >= 100:
                self.driver.quit()
                return
            yield scrapy.Request(url=self.driver.current_url, callback=self.parse)


    # def new_response(self, response):
    #     all_properties = response.xpath('//li[@class="_1DNjI"]/a/@href')
    #     yield from response.follow_all(all_properties, self.parse_properties)
    
    def parse_properties(self, response):
        self.visited_urls.add(response.url)
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