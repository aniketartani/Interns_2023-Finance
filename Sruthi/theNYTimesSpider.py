import scrapy
from datetime import datetime
from newspaper import Article
import json
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from dateutil import parser


class ThenytimesspiderSpider(scrapy.Spider):
    name = "theNYTimesSpider"
    allowed_domains = ["www.nytimes.com"]
    start_urls = ["https://www.nytimes.com/section/business","https://www.nytimes.com/section/technology"]


    def parse(self, response):
        BussInsidernewsUrls=response.css('.css-n0sicn a')
        for eachurl in BussInsidernewsUrls:
            newsurl = eachurl.attrib['href']
            yield response.follow(newsurl,callback=self.parse_news_article)
    
    def parse_news_article(self,response):
        url=response.url
        article = Article(url)
        article.download()
        article.parse()
        content = article.text
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        date_string = response.xpath('//time[@class="css-8blifj e16638kd2"]/span/text()').get()
        date_object = parser.parse(date_string)

        
        yield{'headline':article.title,
            'publishedDate':date_object.date(),
            'category':'tech',
            'extractedDate' : current_date,
            'extractedTime': current_time,
            'source': 'www.businessinsider.in',
            'content':content,
        
              }
    

