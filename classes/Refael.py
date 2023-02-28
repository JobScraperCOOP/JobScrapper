from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import logging

from classes.JobProvider import JobProvider
from db.models.Job import Job
from db.db import session


class Refael(JobProvider):
    available_for_scrape = 'True'

    def __init__(self):
        super().__init__()
        self.all_jobs = []
        self.base_url = 'https://career.rafael.co.il/search/1/'
        self.next_page = self.base_url

        self.browser = self.create_browser('../chromedriver')

    def begin_scrape(self):
        self.scrape_all_jobs()

        self.save_to_db()

    def update_next_page(self):
        prevPage = int(self.next_page.split('/')[4])
        prevPage += 1
        self.next_page = "https://career.rafael.co.il/search/" + str(prevPage)

    def scrape_all_jobs(self):
        self.scrape_page(self.base_url)
        # If there is more than one page
        while (self.next_page):
            print("before scraping" + self.next_page)
            self.scrape_page(self.next_page)

    def scrape_page(self, url):
        self.browser.get(url)

        resultsXpath = "//*[@id='page-search-results']/div/div/div[2]/div[2]"
        results = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, resultsXpath)))

        items = results.find_elements(By.CLASS_NAME, "data")

        for item in items:
            try:
                title = item.find_element(By.TAG_NAME, 'h3').text
                link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')

                code = link.split('/')[4]
                if (code == ''):
                    print('no code')
                    continue

                city = item.find_element(
                    By.CSS_SELECTOR, "ul > li:nth-child(3)").text
                jobType = item.find_element(
                    By.CSS_SELECTOR, "ul > li:nth-child(2)").text
                category = item.find_element(
                    By.CSS_SELECTOR, "ul > li:nth-child(1)").text
                print(category)

                jobObject = {
                    'title': title,
                    'category': category,
                    'code': code,
                    'link': link,
                    'region': city,
                    'city': city,
                    'last_updated': time.time()
                }
                print(jobObject)
                self.all_jobs.append(jobObject)
            except Exception:
                # Add logger for known issues
                logging.error('Error while scraping data - Refael')
                print(Exception)
            # try:
            #     job = Job(title, category, code,
            #               link, city, city, time.time())
            #     session.add(job)
            #     session.commit()
            # except Exception as err:
            #     # Send to logger**
            #     print(err)
            #     session.rollback()

        # Check if next page is available
        xpath_next_arrow = '//*[@id="page-search-results"]/div/div/div[2]/div[3]/nav/ul/li[last()]'

        class_of_next_arrow = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_next_arrow))).get_attribute('class')
        # class_of_next_arrow = self.browser.find_element(
        #     By.XPATH, xpath_next_arrow).get_attribute('class')

        print(class_of_next_arrow)
        if ('disabled' in class_of_next_arrow):
            print('Last page!!!')
            self.next_page = ""
        else:
            self.update_next_page()
