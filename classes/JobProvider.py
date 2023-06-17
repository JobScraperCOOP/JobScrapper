from db.models.Job import Job
from db.db import session
import time
import logging

from selenium.webdriver.chrome.options import Options
from selenium import webdriver


class JobProvider:
    def __init__(self):
        self.base_url = None

    def get_job_entries(self):
        self.begin_scrape()

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

    def save_to_db(self):
        print("save to db function")
        try:
            for j in self.all_jobs:
                print(j)
                job = Job(j['title'], j['category'], j['code'],
                        j['link'], j['region'], j['city'],time.time())
                session.add(job)
                session.commit()
        except Exception as err:
            logging.error('Error while adding to db')
            print(err)
            session.rollback()
        

# FIXME: decide on the interface of this class, and have all other classes implement it
#   Suggestion:
#   - this class should have method to generate an array of Job listing (new class to create)
#   - generally, this class handles only with scraping the website to get the raw data
