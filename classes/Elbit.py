from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

from classes.JobProvider import JobProvider
from db.Job import Job
from db.db import session


class Elbit(JobProvider):
    def __init__(self):
        super().__init__()
        self.allJobs = []
        self.nextPage = ''
        
        self.base_url = 'https://elbitsystemscareer.com/'
        self.categoryClass = "item-practice"
        self.categories = []

        self.getCategories()


    def getCategories(self):
        source = requests.get(
            self.base_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text

        soup = BeautifulSoup(source, 'html.parser')
        categories = soup.find_all('div', class_=self.categoryClass)

        for category in categories:
            self.categories.append(category.find('a').get('href'))

    def scrapeAllCategories(self):
        for category in self.categories: 
            print("starting to scrape:  " + category)
            self.scrapeCategory(category)

    def scrapeCategory(self, link):
        self.scrapePage(link)
        # If there is more than one page
        while(self.nextPage):
            print(self.nextPage)
            self.scrapePage(self.nextPage)
                

    def scrapePage(self, link):
        pageSource = requests.get(link, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text
        pageSoup = BeautifulSoup(pageSource, 'html.parser')

        jobCategory = pageSoup.find('h1', class_='page-title').text
        pageJobs = pageSoup.find_all('tr', class_='job-row')
        
        for job in pageJobs:
            jobColumns = job.find_all('td')

            jobLink = 'https://elbitsystemscareer.com' + \
                job.find('a').get('href')
            jobTitle = job.find('a').string
            jobCode = jobColumns[1].string
            jobRegion = jobColumns[2].string
            jobCity = jobColumns[3].contents[0].replace(' ', '')

            jobObject = {
                'Title': jobTitle,
                'Job Category': jobCategory,
                'Code': jobCode,
                'Link': jobLink,
                'Region': jobRegion,
                'City': jobCity,
                'Last Updated':time.time()
            }

            # Add to db
            try:
                job = Job(jobTitle, jobCategory, jobCode,
                        jobLink, jobRegion, jobCity,time.time())
                session.add(job)
                session.commit()
            except Exception as err:
                # Send to logger**
                print(err)
                session.rollback()

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
            self.allJobs.append(jobObject)

        # Class of next button if available: 'next back-steps enabled'
        try:
            self.nextPage = pageSoup.find(
                'a', 'next back-steps enabled').get('href')
        except Exception:
            self.nextPage = ''
        # print(allJobs)

        # Export to CSV later DB
        allJobsDf = pd.DataFrame(self.allJobs)
        # allJobsDf.to_csv('jobs.csv', encoding='utf-8-sig')
        print('Ending page')
