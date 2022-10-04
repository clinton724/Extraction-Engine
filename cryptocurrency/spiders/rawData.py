import scrapy
from ..items import ScraperItem
import pymssql
from dotenv import load_dotenv
import os

user_name = 'designdb-admin@designdb'
password = 'Design2022'
serverName = 'designdb.database.windows.net'

def connectionPool ():
            conn = pymssql.connect(server=serverName, 
                            user=user_name, 
                            password=password, 
                            database='RawData')
            return conn,conn.cursor()

connection, cursor = connectionPool() 


class getData(scrapy.Spider):
    name = "rawData"
    custom_settings = {'ITEM_PIPELINES': {'cryptocurrency.pipelines.ScraperPipeline': 300}}
    cursor.execute("select Cryptocurrency, historicalData_URL from urlMapping")
    data = cursor.fetchall()
    connection.commit()

    def start_requests(self):
            for index in self.data:
                yield scrapy.Request(url=index[1], callback=self.parse)
    
    def parse(self, response):
           items = ScraperItem()
           name = response.css("""body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > 
                    div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.md\:tw-col-span-2 > 
                    div.tw-flex.tw-text-gray-900.dark\:tw-text-white.tw-mt-2.tw-items-center > div::text""").get()
           rows = response.css("body > div.container > div.card-body > div > div > table > tbody > tr")
           
           for index in rows:
                Date = index.css("th::text").extract()
                Market_cap = index.css("td:nth-child(2)::text").extract()
                Volume = index.css("td:nth-child(3)::text").extract()
                Open = index.css("td:nth-child(4)::text").extract()
                Close = index.css("td:nth-child(5)::text").extract()
                temp1 = Market_cap[0].split("\n")
                temp2 = Volume[0].split("\n")
                temp3 = Open[0].split("\n")
                temp4 = Close[0].split("\n")
                temp0 = name.split("\n")
                coin = temp0[1]
                Date = Date[0]
                Market_cap = temp1[1]
                Volume = temp2[1]
                Open = temp3[1]
                Close = temp4[1]
                items['coin'] = coin
                items['Market_cap'] = Market_cap
                items['Date'] = Date
                items['Volume'] = Volume
                items['Open'] = Open
                items['Close'] = Close
                yield items