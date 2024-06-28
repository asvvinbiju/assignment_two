import scrapy

class Properties(scrapy.Spider):
    name = "properties"
    start_urls = ['https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723']

    def parse(self, response):
        all_properties = response.xpath('//li[@class="_1DNjI"]/a/@href')
        yield from response.follow_all(all_properties, callback=self.parse_properties)
    
    def parse_properties(self, response):
        yield {
            "property_name": response.xpath('//h1[@class="_1hJph"]/text()').get()
        }