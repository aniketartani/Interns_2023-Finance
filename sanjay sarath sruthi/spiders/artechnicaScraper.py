import scrapy
from datetime import datetime
from newspaper import Article
import json
from scrapy.crawler import CrawlerProcess

class ArtechnicascraperSpider(scrapy.Spider):
    name = "artechnicaScraper"
    allowed_domains = ["arstechnica.com"]
    start_urls = ["https://arstechnica.com/gadgets/","https://arstechnica.com/information-technology/"]
    current_date = str(datetime.now().date())
    current_time = str(datetime.now().time())
    fileName1 = 'artec' + current_date + "_" + current_time + '.json'
    fileName2 = 'artec' + current_date + "_" + current_time + '.csv'
    
    
    def parse(self, response):
        artechnewsUrls=response.xpath('//li[@class="tease article "]')
        for eachurl in artechnewsUrls:
            newsurl = eachurl.css('a').attrib['href']
            # yield  {'url': newsurl}
            yield response.follow(newsurl,callback=self.parse_news_article)
    def parse_news_article(self,response):
        url=response.url
        article = Article(url)
        article.download()
        article.parse()
        content = article.text
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        date_format = '%b %d, %Y %I:%M %p %Z'
        date_string=response.css('time.date::text').get()
        yield{'headline':response.xpath('//h1/text()').get(),
            'publishedDate':datetime.strptime(date_string, date_format).date(),
            'category':'tech',
            'extractedDate' : current_date,
            'extractedTime': current_time,
            'source': 'arstechnica.com',
            'content':content,
        
              }
            
            






