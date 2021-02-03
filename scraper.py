from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import datetime 

# Define Headless Driver
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={user_agent}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

# driver = webdriver.Chrome('/users/krynen/desktop/selenium/browsers/chromedriver')
driver = webdriver.Chrome('/users/krynen/desktop/selenium/browsers/chromedriver', options=options)

# Define Today
today = datetime.date.today().strftime('%-d %B %Y')

# Define and open CSV File
csv_file = open('portphillip_ad.csv', 'w+')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Number', 'Description', 'Lodged', 'Address', 'Documents', 'Date Scraped'])

driver.get('https://eservices.portphillip.vic.gov.au/ePathway/Production/Web/GeneralEnquiry/EnquiryLists.aspx')
print('Starting Port Phillip Ad scraper...')
print()

# Define and Click Buttons
advertising = driver.find_element_by_id('ctl00_MainBodyContent_mDataList_ctl03_mDataGrid_ctl02_ctl00')
advertising.click()

next = driver.find_element_by_id('ctl00_MainBodyContent_mContinueButton')
next.click()

# Define Application Variables
number = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[1]/a')
description = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[3]/div')
address = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[2]/div')
documents = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[1]/a')
lodged = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[4]/span')

# Write to CSV File
page_items = len(number)
current_page = driver.find_element_by_id('ctl00_MainBodyContent_mPagingControl_pageNumberLabel')
print('Getting ' + current_page.text)
with open('portphillip_ad.csv', 'w+'):
    for i in range(page_items):
        csv_writer.writerow([number[i].text, description[i].text, lodged[i].text, address[i].text, documents[i].get_attribute('href'), today])

# Defining Append File Function
def append_file():
    next_page = driver.find_element_by_id('ctl00_MainBodyContent_mPagingControl_nextPageHyperLink')
    next_page.click()
    current_page = driver.find_element_by_id('ctl00_MainBodyContent_mPagingControl_pageNumberLabel')
    print('Getting ' + current_page.text)
    number = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[1]/a')
    description = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[3]/div')
    address = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[2]/div')
    documents = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[1]/a')
    lodged = driver.find_elements_by_xpath('//*[@id="ctl00_MainBodyContent_group_11"]/table/tbody/tr/td/table/tbody/tr/td[4]/span')
    with open('portphillip_ad.csv', 'a+'):
        for i in range(page_items):
            csv_writer.writerow([number[i].text, description[i].text, lodged[i].text, address[i].text, documents[i].get_attribute('href'), today])

# Append File Loop
for i in range(10000):
    try:
        append_file()
    except:
        print()
        print('Scraper finished. No more pages to get.')
        break

# Close and Save
csv_file.close()
driver.close()
