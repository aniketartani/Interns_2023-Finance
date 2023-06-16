import scrapy
from datetime import datetime
from newspaper import Article
import json
from scrapy.crawler import CrawlerProcess
from datetime import datetime
from dateutil import parser


class BusinessinsiderspiderSpider(scrapy.Spider):
    name = "BusinessInsiderSpider"
    allowed_domains = ["www.businessinsider.in"]
    start_urls = ["https://www.businessinsider.in/tech?r=US","https://www.businessinsider.in/business","https://www.businessinsider.in/stock-market"]
    current_date = str(datetime.now().date())
    current_time = str(datetime.now().time())

    def parse(self, response):
        BussInsidernewsUrls=response.xpath('//a[@class="list-title-link"]')
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
        date_string = response.xpath("//span[@class='Date']/text()").get()
        date_object = parser.parse(date_string)

        
        yield{'headline':article.title,
            'publishedDate':date_object.date(),
            'category':'tech',
            'extractedDate' : current_date,
            'extractedTime': current_time,
            'source': 'www.businessinsider.in',
            'content':content,
        
              }
            
            


       
    
            
