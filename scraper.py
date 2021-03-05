import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"

import scraperwiki
import requests
from datetime import datetime
from bs4 import BeautifulSoup

today = datetime.today()

urlt = 'https://www.banyule.vic.gov.au/Planning-building/Review-local-planning-applications/Planning-applications-on-public-notice?dlv_OC%20CL%20Public%20Works%20and%20Projects=(pageindex=1)'
rt = requests.get(urlt)
soupt = BeautifulSoup(rt.content, 'lxml')
max_page = int(soupt.find('div', class_='seamless-pagination-info right').text.split('of ')[1])

for i in range(1, max_page + 1):
    try:
        print(f'Getting page {i}')
        url = f'https://www.banyule.vic.gov.au/Planning-building/Review-local-planning-applications/Planning-applications-on-public-notice?dlv_OC%20CL%20Public%20Works%20and%20Projects=(pageindex={i})'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        rows = soup.find_all('div', class_='list-item-container item-no-date')

        for row in rows:
            record = {}
            record['address'] = row.find(
                'h2', class_='list-item-title').text.split(' - ')[0].strip()
            record['date_scraped'] = today.strftime("%d-%m-%Y")
            record['council_reference'] = row.find(
                'h2', class_='list-item-title').text.split(' - ')[1].strip()
            record['info_url'] = str(row.find('a')).split('"')[1]
            on_notice_to_raw = row.find('p').text.split(': ')[1]
            record['on_notice_to'] = datetime.strptime(
                on_notice_to_raw, '%d %B %Y').strftime('%Y-%m-%d')

            scraperwiki.sqlite.save(
                unique_keys=['council_reference'], data=record, table_name="data")

    except:
        print('Scraper finished.')
        break
