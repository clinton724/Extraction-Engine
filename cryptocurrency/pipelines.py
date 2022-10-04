# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import date
import pymssql

user_name = 'designdb-admin@designdb'
password = 'Design2022'
serverName = 'designdb.database.windows.net'

class CryptocurrencyPipeline(object):
    def __init__(self):
        self.create_connection()
        
    def create_connection(self):
            self.conn = pymssql.connect(server=serverName, 
                            user=user_name, 
                            password=password, 
                            database='RawData')
            self.curr = self.conn.cursor()      

    def process_item(self, item, spider):
        self.curr.execute("""insert into urlMapping values (%s,%s,%s,%s)""", 
                          ( item['name'], item['rootURL'], item['historicalData'], item['market']))
        self.conn.commit()
        return item

class ScraperPipeline(object):
    def __init__(self):
        self.create_connection()
        
    def create_connection(self):
            self.conn = pymssql.connect(server=serverName, 
                            user=user_name, 
                            password=password, 
                            database='RawData')
            self.curr = self.conn.cursor()      

    def process_item(self, item, spider):
        current_date = str(date.today())
        itemDate = item['Date']
        coin = item['coin']
        self.curr.execute(f"SELECT DATEDIFF(day, {current_date}, {itemDate})")
        thirtyDaysAgo = self.curr.fetchone()
        self.conn.commit()
        print(type(current_date), " ", type(itemDate), " ", abs(thirtyDaysAgo[0]), " ", type(int(abs(thirtyDaysAgo[0]))) )
        if int(abs(thirtyDaysAgo[0])) >= 30: 
            self.curr.execute(f"delete from HistoricalData where Cryptocurrency = {coin} and Date = {current_date}")
            self.conn.commit()
        elif int(abs(thirtyDaysAgo[0])) == 0:
            self.curr.execute("""insert into HistoricalData values (%s,%s,%s,%s,%s,%s)""", 
                            ( item['coin'], item['Date'], item['Market_cap'], item['Volume'], item['Open'], item['Close']))
            self.conn.commit()
        return item
    
