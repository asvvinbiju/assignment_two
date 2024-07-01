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
    name = "testmrweb"
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
        while self.i < 5:
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
            # time.sleep(5)
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[class="rui-apowA rui-htytx rui-UGVY0"]')))
            # for i in self.properties_url:
            #     yield scrapy.Request(url=i, callback=self.parse_properties)
            self.i += 1
        new_response = HtmlResponse(url=self.driver.current_url, body=self.driver.page_source, encoding="utf-8")
        all_properties = new_response.xpath('//a/@href').getall()
        for link in all_properties:
            if link.startswith('/item'):
                self.properties_url.add(f"https://www.olx.in{link}")
        self.driver.quit()
        print(self.properties_url)
        print(len(self.properties_url))