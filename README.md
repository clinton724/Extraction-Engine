# ELEN4002A/ELEN4012A - Web Scraping System For Big Data Applications

## Instructions on how to run the code
- Download the folder zip file
- Open the code on a terminal if using linux or mac. Alternatively open the code via Visual Studio
- Ensure that you have Python 3.8+ installed
- Run the command `pip3 install -r requirements.txt` to install all the dependencies
- Run `pip3 freeze > requirements.txt`
- cd into the cryptocurrency folder
- cd into the spiders folder and run `scrapy crawl getUrls` to run the web crawler
- Run `scrapy crawl rawData` to run the web scraper