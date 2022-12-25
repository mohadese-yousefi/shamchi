#
import scrapy

class BlogSpider(scrapy.Spider):
    name = 'chishi'
    start_urls = ['https://chishi.ir/cat/nutrition/cooking/']
    result_file = open('result.csv', 'w+')

    def parse(self, response):
        for title in response.css('.post-title'):
            self.result_file.write(f"{title.css('::text').get()},{title.css('::attr(href)').get()}\n")
        
        

        for next_page in response.css('.pagination a::attr("href")'):
            #import pudb; pudb.set_trace()
            yield response.follow(next_page.get(), self.parse)
