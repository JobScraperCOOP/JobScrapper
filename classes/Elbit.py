from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from db.db import session
from db.Job import Job


class Elbit:
    def __init__(self):
        self.allJobs = []
        self.nextPage = ''

    def scrapeCategory(self, category):
        catLink = category.find('a').get('href')
        self.scrapePage(catLink)

        # If there is more than one page
        # while(self.nextPage):
        #     if (self.nextPage):
        #         print(self.nextPage)
        #         self.scrapePage(self.nextPage)
        for i in range(1):
            if (self.nextPage):
                self.scrapePage(self.nextPage)

    def scrapePage(self, catLink):
        pageSource = requests.get(catLink, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text
        pageSoup = BeautifulSoup(pageSource, 'html.parser')

        jobCategory = pageSoup.find('h1', class_='page-title').text
        pageJobs = pageSoup.find_all('tr', class_='job-row')
        # print('after find  '+ str(time.perf_counter()))
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
                'City': jobCity
            }

            # Add to db
            try:
                job = Job(jobTitle, jobCategory, jobCode,
                        jobLink, jobRegion, jobCity)
                session.add(job)
                session.commit()
            except Exception:
                # Send to logger**
                print(Exception)

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
        allJobsDf.to_csv('jobs.csv', encoding='utf-8-sig')
        print('Ending page')
