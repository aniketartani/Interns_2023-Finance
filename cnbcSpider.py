import scrapy
from datetime import datetime
from newsScraper.items import NewsscraperItem

class CnbcspiderSpider(scrapy.Spider):
    name = 'cnbcSpider'
    allowed_domains = ['www.cnbc.com']
    start_urls = ['https://www.cnbc.com/technology/']

    current_date = str(datetime.now().date())
    current_time = str(datetime.now().time())
    fileName1 = '/Users/sanjay/Documents/Code/Python/scrapy_python/newsScraper/newsScraper/extractedData/' + 'cnbc' + current_date + "_" + current_time + '.json'
    #fileName2 = '/Users/sanjay/Documents/Code/Python/scrapy_python/newsScraper/newsScraper/extractedData/' + 'cnbc' + current_date + "_" + current_time + '.csv'
    custom_settings = {
        'FEEDS': { 
            fileName1 : {'format': 'json', 'overwrite': True},
            #fileName2 : {'format': 'csv', 'overwrite': True}
           }
        }
    def parse(self, response):
        cnbcTechNews = response.css('div.Card-titleContainer')
        #print(len(cnbcTechNews))
        for cnbcTechNew in cnbcTechNews:
            newsurl = cnbcTechNew.css('div a').attrib['href']
            yield response.follow(newsurl,callback=self.parse_news_article)

    def parse_news_article(self,response):
        try:
            news_item = NewsscraperItem()
            newsArticle = ""
            article = response.css('div.ArticleBody-articleBody')
            content = article.css('p')
            for c in content:
                for i in c.css('::text'):
                    newsArticle += i.get()
                newsArticle += '\n'
            
            header = response.css('div.ArticleHeader-headerContentContainer')
            category = header.css('div a::text').get()
            headline = header.css('div div h1::text').get()
            
            time = response.css('time')
            published_date = time[0].css('time::text').get()
            date_value = published_date.split("Published ")[1]
            p_date = datetime.strptime(date_value, "%a, %b %d %Y").date()
            current_date = datetime.now().date()
            current_time = datetime.now().time()
            #difference = datetime.strptime(current_date, '%Y-%m-%d').date() - datetime.strptime(p_date, '%Y-%m-%d').date()
            #difference_in_days = difference.days
            news_item['headline'] = headline
            news_item['category'] = category
            news_item['content'] = newsArticle
            news_item['publishedDate'] = p_date
            news_item['extractedDate'] = current_date
            news_item['extractedTime'] = current_time
            news_item['source'] = 'www.cnbc.com'
            yield news_item
        except:
            yield {}