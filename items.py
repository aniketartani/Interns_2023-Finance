# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsscraperItem(scrapy.Item):
    headline = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
    publishedDate = scrapy.Field()
    extractedDate = scrapy.Field()
    extractedTime = scrapy.Field() 
    source = scrapy.Field()