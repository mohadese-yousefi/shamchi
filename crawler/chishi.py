import os

import scrapy
import motor.motor_asyncio


DATABASE_URL = os.environ.get("DATABASE_URL")
client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client.shamchi

class BlogSpider(scrapy.Spider):
    name = 'chishi'
    start_urls = ['https://chishi.ir/cat/nutrition/cooking/']
    
    def detail_page(self, response, name, url):
        food_name = {}
        food_name['name'] = name
        food_name['url'] = url 
        ingradiants = []
        recipe = ''
        table = response.xpath('//tr//td/text()')
        for i in range(0, len(table), 2):
            ingradiants.append({"name":table[i].get()})
            ingradiants.append({"size":table[i+1].get()})

        for description in response.xpath('//p'): 
            recipe = '\n'.join(description.get())

        food_name['recipe'] = recipe 
        food_name['ingradients'] = ingradiants
        new_food = db["food"].insert_one(food_name)    

    def parse(self, response):
        for title in response.css('.post-title'):
            food_name = {"name":f"{title.css('::text').get()}",
                "url":f"{title.css('::attr(href)').get()}"}
            yield response.follow(title.css('::attr(href)').get(), self.detail_page, cb_kwargs=food_name) 
        
        

        for next_page in response.css('.pagination a::attr("href")'):
            #import pudb; pudb.set_trace()
            yield response.follow(next_page.get(), self.parse)
