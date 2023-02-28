from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import logging


from classes.JobProvider import JobProvider
from db.models.Job import Job
from db.db import session


class Elbit(JobProvider):
    available_for_scrape = 'True'

    def __init__(self):
        super().__init__()
        self.all_jobs = []
        self.next_page = ''
        self.uniqueCode = 'Elbt'

        self.base_url = 'https://elbitsystemscareer.com/'
        self.categoryClass = "item-practice"
        self.categories = []

    def begin_scrape(self):
        self.get_categories()
        self.scrape_all_categories()
        # remove save to db 
        self.save_to_db()
        return self.all_jobs


    def get_categories(self):
        source = requests.get(
            self.base_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text

        soup = BeautifulSoup(source, 'html.parser')
        categories = soup.find_all('div', class_=self.categoryClass)

        for category in categories:
            self.categories.append(category.find('a').get('href'))

    def scrape_all_categories(self):
        for category in self.categories: 
            print("starting to scrape:  " + category)
            self.scrape_category(category)

    def scrape_category(self, link):
        self.scrape_page(link)
        # If there is more than one page
        while(self.next_page):
            print(self.next_page)
            self.scrape_page(self.next_page)
                

    def scrape_page(self, link):
        pageSource = requests.get(link, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text
        pageSoup = BeautifulSoup(pageSource, 'html.parser')

        jobCategory = pageSoup.find('h1', class_='page-title').text
        pageJobs = pageSoup.find_all('tr', class_='job-row')
        
        for job in pageJobs:
            try:
                jobColumns = job.find_all('td')

                jobLink = 'https://elbitsystemscareer.com' + \
                    job.find('a').get('href')
                jobTitle = job.find('a').string
                jobCode = self.uniqueCode + jobColumns[1].string
                jobRegion = jobColumns[2].string
                jobCity = jobColumns[3].contents[0].replace(' ', '')
            except Exception:
                logging.error('error while scraping a single vacancy - Elbit')

            jobObject = {
                'title': jobTitle,
                'category': jobCategory,
                'code': jobCode,
                'link': jobLink,
                'region': jobRegion,
                'city': jobCity,
                'last_updated':time.time()
            }

            # Add to db
            # try:
            #     job = Job(jobTitle, jobCategory, jobCode,
            #             jobLink, jobRegion, jobCity,time.time())
            #     session.add(job)
            #     session.commit()
            # except Exception as err:
            #     # Send to logger**
            #     print(err)
            #     session.rollback()
            # 
            # 
            # 
            # 
            # 
            # 

            # Inside job description page
            # For now not in use
            #
            # jdSource = requests.get(jobLink, headers={
            #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text
            # jdSoup = BeautifulSoup(jdSource, 'html.parser')
            # jdJobBoxes = jdSoup.find_all('div', class_="box-job")

            # for jb in jdJobBoxes:
            #     jbJobBoxHeader = jb.find('h2').text.lstrip()
            #     jbJobBoxDvis = jb.find_all('div')
            #     jbJobBoxText = []
            #     for div in jbJobBoxDvis:
            #         jbJobBoxText.append(div.text)
            #     jobObject[jbJobBoxHeader] = jbJobBoxText

            # Add to global job array
            self.all_jobs.append(jobObject)

        # Class of next button if available: 'next back-steps enabled'
        try:
            self.next_page = pageSoup.find(
                'a', 'next back-steps enabled').get('href')
        except Exception:
            self.next_page = ''
        # print(allJobs)

        # Export to CSV later DB
        # allJobsDf = pd.DataFrame(self.all_jobs)
        # allJobsDf.to_csv('jobs.csv', encoding='utf-8-sig')
        print('Ending page')
