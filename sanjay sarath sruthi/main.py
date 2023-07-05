import json
import requests
#from scrapy.crawler import CrawlerProcess

from flask import Flask, request, Response, render_template, session, redirect, url_for

app = Flask(__name__)

@app.route("/latestnews",methods=["GET"])
def scrape():
    spiders = ['cnbcSpider','ETSpider_1','ETSpider_2']
    output = []
    for spider in spiders:
        params = {
            'spider_name': spider,
            'start_requests': True,
        }
        response = requests.get('http://localhost:9080/crawl.json', params)
        data = json.loads(response.text)
        output.append(data)
    return output
       
if __name__ == '__main__':
    app.run(debug=True, port=2000)