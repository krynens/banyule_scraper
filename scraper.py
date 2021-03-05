from bs4 import BeautifulSoup
from datetime import datetime
import datetime
import requests
import scraperwiki
import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"


today = datetime.today()
url = f'https://www.melbourne.vic.gov.au/building-and-development/property-information/planning-building-registers/Pages/town-planning-permits-register-search-results.aspx?AdvertisingOnly=on&page={i}'

for i in range(1, 50):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')

        table = soup.find('tbody')
        rows = table.find_all('tr', class_='detail')

        for row in rows:
            record = {}
            record['address'] = row.find('td', class_='column2').text
            date_received_raw = row.find('td', class_='column3').text
            record['date_received'] = datetime.strptime(
                date_received_raw, "%d/%m/%Y").strftime("%d-%m-%Y")
            record['date_scraped'] = today.strftime("%d-%m-%Y")
            record['description'] = row.find('td', class_='column4').text
            record['council_reference'] = row.find('td', class_='column1').text
            record['info_url'] = 'https://www.melbourne.vic.gov.au' + \
                str(row.find('td', class_='column1')).split('"')[5]

            scraperwiki.sqlite.save(
                unique_keys=['council_reference'], data=record, table_name="data")

    except:
        print('Scraper finished.')
        break
