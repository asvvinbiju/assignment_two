import scrapy

class Properties(scrapy.Spider):
    name = "properties"
    start_urls = ['https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723']

    count = 0
    limit = 1000

    def parse(self, response):
        all_properties = response.xpath('//li[@class="_1DNjI"]/a/@href')
        yield from response.follow_all(all_properties, callback=self.parse_properties)

        self.count += 1
        if self.count >= self.limit:
            return
    
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