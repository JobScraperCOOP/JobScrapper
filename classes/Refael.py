from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

import pandas as pd
from db.Job import Job
from db.db import session


class Refael:
    def __init__(self):
        self.allJobs = []
        self.nextPage = "https://career.rafael.co.il/search/1/"

        self.url = 'https://career.rafael.co.il/search/1/'
        self.browser = self.create_browser('../chromedriver')

    def create_browser(self, webdriver_path):
        # create a selenium object that mimics the browser
        browser_options = Options()

        # headless tag created an invisible browser
        # browser_options.add_argument("--headless")
        # browser_options.add_argument('--no-sandbox')
        browser_options.add_argument(
            "disable-blink-features=AutomationControlled")

        browser = webdriver.Chrome(
            webdriver_path, chrome_options=browser_options)
        print("Done Creating Browser")
        return browser

    def updateNextPage(self):
        prevPage = int(self.nextPage.split('/')[4])
        prevPage += 1
        self.nextPage = "https://career.rafael.co.il/search/" + str(prevPage)
        

    def scrapeAllJobs(self):
        self.scrapePage(self.url)
        # If there is more than one page
        while (self.nextPage):
            print("before scraping" + self.nextPage)
            self.scrapePage(self.nextPage)

    def scrapePage(self, url):
        self.browser.get(url)

        resultsXpath = "//*[@id='page-search-results']/div/div/div[2]/div[2]"
        results = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, resultsXpath)))

        items = results.find_elements(By.CLASS_NAME, "item")

        for item in items:
            title = item.find_element(By.TAG_NAME, 'h3').text
            link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')

            code = link.split('/')[4]
            if (code == ''):
                continue

            city = item.find_element(
                By.XPATH, '//div[1]/div[1]/ul/li[3]').text
            jobType = item.find_element(
                By.XPATH, '//div[1]/div[1]/ul/li[2]').text
            category = item.find_element(
                By.XPATH, '//div[1]/div[1]/ul/li[1]').text

            jobObject = {
                'Title': title,
                'Job Category': category,
                'Code': code,
                'Link': link,
                'Region': city,
                'City': city,
                'Last Updated': time.time()
            }

            self.allJobs.append(jobObject)
            try:
                job = Job(title, category, code,
                          link, city, city, time.time())
                session.add(job)
                session.commit()
            except Exception as err:
                # Send to logger**
                print(err)
                session.rollback()

        # Check if next page is available
        xpath_next_arrow = '//*[@id="page-search-results"]/div/div/div[2]/div[3]/nav/ul/li[last()]'
        
        class_of_next_arrow = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_next_arrow))).get_attribute('class')
        # class_of_next_arrow = self.browser.find_element(
        #     By.XPATH, xpath_next_arrow).get_attribute('class')


            
        print(class_of_next_arrow)
        if ('disabled' in class_of_next_arrow):
            print('Last page!!!')
            self.nextPage = ""
        else:
            self.updateNextPage()


