# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime, timedelta
from scrapy.exceptions import DropItem

class NewsscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        current_date = adapter['extractedDate']
        published_date = adapter['publishedDate']
        diff = current_date - published_date
        difference_in_days = diff.days
        if difference_in_days <= 2:
            ## Strip all whitespaces from strings
            field_names = adapter.field_names()
            no_strip_keys = ['extractedDate','extractedTime','content','publishedDate']
            for field_name in field_names:
                if field_name not in no_strip_keys:
                    value = adapter.get(field_name)
                    adapter[field_name] = value.strip()
        
            ## Category & Product Type --> switch to lowercase
            lowercase_keys = ['category']
            for lowercase_key in lowercase_keys:
                value = adapter.get(lowercase_key)
                adapter[lowercase_key] = value.lower()
            return item
        else:
            raise DropItem("Not the latest article")
        

import mysql.connector
class SaveToMySQLPipeline:

    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'sanjay@123',
            database = 'newsArticle'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS newsArticles(
            id int NOT NULL auto_increment, 
            headline text,
            category VARCHAR(255),
            content text,
            publishedDate DATE,
            extractedDate DATE,
            extractedTime TIME,
            source text,
            PRIMARY KEY (id)
        )
        """)
        '''
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS newsArticles(
            id int NOT NULL auto_increment, 
            headline text,
            category VARCHAR(255),
            publishedDate DATE,
            extractedDate DATE,
            extractedTime TIME,
            PRIMARY KEY (id)
        )
        """)
        '''
        
    def process_item(self, item, spider):
        ## Define insert statement
        #query = "INSERT INTO newsArticles (headline, category, content, publishedDate, extractedDate, extractedTime, source) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        #self.cur.execute(query, (item['headline'],item['category'],item['content'],item['publishedDate'],item['extractedDate'],item['extractedTime'],item['source']))
        query = "INSERT INTO newsArticles (headline, category, publishedDate, extractedDate, extractedTime, source, content) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cur.execute(query, (item['headline'],item['category'],item['publishedDate'],item['extractedDate'],item['extractedTime'],item['source'],item['content']))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database
        days_ago = datetime.now() - timedelta(days=3)
        days_ago = days_ago.strftime('%Y-%m-%d')
        sql_query = "DELETE FROM newsArticles WHERE publishedDate < %s"
        self.cur.execute(sql_query, (days_ago,))
        self.conn.commit()
        self.cur.close()
        self.conn.close()

import os
class SaveAsTxtFiles:
    def __init__(self):
        folder_name = os.path.join('/Users/sanjay/Documents/Code/Python/scrapy_python/newsScraper/newsScraper/extractedData', (str(datetime.now().date()) + "_" + str(datetime.now().time())))
        os.mkdir(folder_name)
        self.folder_name = folder_name

    def save_file(self, item, spider):
        fn = item['source'] + ".txt"
        file_name = os.path.join(self.folder_name, fn)
        content = ""
        adapter = ItemAdapter(item)
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            content += str(field_name) + " : " + str(value) + "\n"
        with open(file_name, 'w') as file:
            file.write(content)
        return item
