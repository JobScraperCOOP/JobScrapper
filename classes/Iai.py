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


class Iai(JobProvider):
    available_for_scrape = 'True'

    def __init__(self):
        super().__init__()
        self.all_jobs = []
        self.base_url = 'https://jobs.iai.co.il/jobs/'

        self.next_page = self.base_url + '?pg=1'

        self.browser = self.create_browser('../chromedriver')

    def begin_scrape(self):
        self.scrape_all_jobs()

        self.save_to_db()

    def update_next_page(self):
        prevPage = int(self.next_page.split('=')[1])
        prevPage += 1
        self.next_page = "https://jobs.iai.co.il/jobs/?pg=" + str(prevPage)
        print(self.next_page)

    def scrape_all_jobs(self):
        self.scrape_page(self.base_url)
        # If there is more than one page
        while (self.next_page):
            print(self.next_page)
            self.scrape_page(self.next_page)

    def scrape_page(self, url):
        self.browser.get(url)

        resultsXpath = "//*[@id='jobs-section']/div[3]/div/ul"
        results = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, resultsXpath)))
            
        items = results.find_elements(By.CLASS_NAME, "job-card")
        for item in items:
            try:
                title = item.find_element(By.TAG_NAME, 'h3').text
                link = item.find_element(
                    By.TAG_NAME, 'a').get_attribute('href')
                code = link.split('/')[4]
                city = item.find_element(
                    By.XPATH, '//div[1]/li/div/div[2]/ul/li[1]').text
                print(item.find_element(
                    By.XPATH, '//div[1]/li/div/div[2]/ul/li[1]').get_attribute('innerHTML'))
                jobType = item.find_element(
                    By.XPATH, '//div[1]/li/div/div[2]/ul/li[2]').text

                category = item.find_element(
                    By.XPATH, '//div[1]/li/div/div[2]/ul/li[3]').text
            except:
                logging.error('Error while scraping data - Iai')
                category = ""

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
        xpath_next_arrow = '//*[@id="jobs-section"]/div[3]/nav/ul/li[last()]'

        class_of_next_arrow = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath_next_arrow))).get_attribute('class')
        print(class_of_next_arrow)
        if ('disabled' in class_of_next_arrow):
            print('Last page!!!')
            self.next_page = ""
        else:
            self.update_next_page()
