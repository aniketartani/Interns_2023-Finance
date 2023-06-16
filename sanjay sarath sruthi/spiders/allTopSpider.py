import scrapy
from datetime import datetime
from newspaper import Article
from newsScraper.items import NewsscraperItem


class AlltopnewsSpiderSpider(scrapy.Spider):
    name = "allTopSpider"
    start_urls = ["https://alltop.com/tech"]
    current_date = str(datetime.now().date())
    current_time = str(datetime.now().time())
    fileName1 = '/Users/sanjay/Documents/Code/Python/scrapy_python/newsScraper/newsScraper/extractedData/' + 'allTop' + current_date + "_" + current_time + '.json'
    #fileName2 = '/Users/sanjay/Documents/Code/Python/scrapy_python/newsScraper/newsScraper/extractedData/' + 'allTop' + current_date + "_" + current_time + '.csv'
    custom_settings = {
        'FEEDS': { 
            fileName1 : {'format': 'json', 'overwrite': True},
            #fileName2 : {'format': 'csv', 'overwrite': True}
            }
        }
    def parse(self, response):
        try:
            news_item = NewsscraperItem()

            articles_divisions = response.css('div.col-xs-12.col-md-4')
            
            for articles_division in articles_divisions:
                source = articles_division.css('p a::text').get()
                if source in ['The Verge', 'New York Times Technology', 'CNBC Tech', 'Engadget', 'Motherboard',
                            'The Next Web', 'Ars Techica', 'Wired']:
                    news_urls_html = articles_division.css('a.one-line-ellipsis')
                    for news_url_html in news_urls_html:

                        current_datetime = datetime.now
                        current_date = datetime.now().date()
                        current_time = datetime.now().time()

                        url = news_url_html.attrib['href']
                        article = Article(url)
                        article.download()
                        article.parse()
                        title = article.title
                        text = article.text
                        category = 'tech'
                        publish_date = article.publish_date
                        if publish_date is not None:
                            publish_date = publish_date.date()
                        else:
                            publish_date = current_date
                        
                        
                        news_item['headline'] = title
                        news_item['source'] = source
                        news_item['category'] = category
                        news_item['publishedDate'] = publish_date
                        news_item['extractedDate'] = current_date
                        news_item['extractedTime'] = current_time
                        news_item['content'] = text
                        
                        yield news_item
        except:
            yield{}
