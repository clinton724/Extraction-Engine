import scrapy
from ..items import CryptocurrencyItem
import sys
import pymssql
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


class UrlSpider(scrapy.Spider):
    
    name = "getUrls"
    start_urls = ['https://www.coingecko.com']
    custom_settings = {'ITEM_PIPELINES': {'cryptocurrency.pipelines.CryptocurrencyPipeline': 300}}
    cursor.execute("delete from urlMapping")
    connection.commit()

    def parse(self, response):
        """ Contract to check presence of fields in scraped items
        @scrapes name rootURL historicalData market
        """
        for index in response.css("""body > div.container > div.gecko-table-container > div.coingecko-table 
                        > div.position-relative > div > table > tbody > tr:nth-child(n+1) > td.py-0.coin-name.cg-sticky-col.cg-sticky-third-col.px-0 
                        > div > div.tw-flex-auto > a::attr('href')"""):
             url = response.urljoin(index.get())
             yield scrapy.Request(url=url, callback=self.parseInnerPage)
        
        nextPage = response.css("body > div.container > div.gecko-table-container > div.coingecko-table > div.row.no-gutters.tw-flex.flex-column.flex-lg-row.tw-justify-center.mt-2 > nav > ul > li.page-item.next > a::attr('href')").get()    
        if nextPage is not None:
          nextPage = response.urljoin(nextPage)
          yield scrapy.Request(url=nextPage, callback=self.parse)
          

    def parseInnerPage(self, response):
       
       items = CryptocurrencyItem()
       name = response.css("""body > div.container > div.tw-grid.tw-grid-cols-1.lg\:tw-grid-cols-3.tw-mb-4 > 
                    div.tw-col-span-3.md\:tw-col-span-2 > div > div.tw-col-span-2.md\:tw-col-span-2 > 
                    div.tw-flex.tw-text-gray-900.dark\:tw-text-white.tw-mt-2.tw-items-center > div::text""").get()
       historicalData_raw = response.css("#navigationTab > li:nth-child(4) > a::attr('href')").get()
       historicalData = response.urljoin(historicalData_raw)
       market_raw = response.css("#navigationTabMarketsChoice::attr('href')").get()
       market = response.urljoin(market_raw)
       rootURL = response.url
       temp = name.split("\n")
       name = temp[1]
       items['name'] = name
       items['rootURL'] = rootURL
       items['historicalData'] = historicalData
       items['market'] = market
       yield items