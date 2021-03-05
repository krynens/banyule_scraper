import os
import csv
import scrapy
import datetime
import scraperwiki
from planning.items import MorphioScraperItem
from scrapy.loader import ItemLoader
from scrapy.selector import Selector

os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"

today = datetime.date.today().strftime('%-d %B %Y')


class Melbourne(scrapy.Spider):
    name = 'melbourne'
    start_urls = ['https://www.melbourne.vic.gov.au/building-and-development/property-information/planning-building-registers/Pages/town-planning-permits-register-search-results.aspx?AdvertisingOnly=on']

    def parse(self, response):
        for applications in response.css('tr.detail'):
            l = ItemLoader(item=MorphioScraperItem(), selector=applications)

            record['council_reference'] = l.add_css('council_reference', 'a::text')
            record['date_lodged'] = l.add_xpath('date_lodged', './/td[2]')
            record['address'] = l.add_xpath('address', './/td[3]')
            record['description'] = l.add_xpath('description', './/td[4]')
            record['info_url'] = l.add_xpath('info_url', './/td/a/@href')

            yield l.load_item()

        next_page = response.xpath('//div/p[2]/a[5]').attrib['href']
        if next_page:
            yield response.follow(next_page, callback=self.parse)


scraperwiki.sqlite.save(unique_keys=['council_reference'], data=record, table_name="data")
