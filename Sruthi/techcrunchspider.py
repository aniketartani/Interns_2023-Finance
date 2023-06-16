import scrapy
from datetime import datetime
from scrapy_splash import SplashRequest



class TechcrunchspiderSpider(scrapy.Spider):
    name = "techcrunchspider"
    allowed_domains = ["techcrunch.com"]
    start_urls = ["https://techcrunch.com/"]

    def parse(self, response):
    
        NewsUrls =r=response.css('a.post-block__title__link')
        for r in NewsUrls:
            newsurl=r.attrib['href']
            yield SplashRequest(NewsUrls, self.parse_news_article, 'render.html', {'wait': 5})
            # yield response.follow(newsurl,callback=self.parse_news_article)
    def parse_news_article(self,response):
        newsArticle = ""
        article = response.xpath('//div[@class="article-content"]')
        content = article.css('p')
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        for c in content:
            for i in c.css('::text'):
                newsArticle += i.get()
            newsArticle += '\n'
        published_date = response.css('.article__byline time::attr(datetime)').get()
        content_type = response.css('.article__meta .article__meta-item:nth-child(2) a::text').get()
        
        yield{'headline':response.css('h1::text').get(),
            #   'category': response.xpath('//a[contains(@class, "article__primary-category__link gradient-text gradient-text--green-gradient")]::text').get(),
            'publishedDate':published_date,
            'category':content_type,
            'content':content,
            'extractedDate' : current_date,
            'extractedTime': current_time,
            'source': 'techcrunch.com',
        
              
              }
            
            


