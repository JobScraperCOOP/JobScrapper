from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


class Elbit:
    def __init__(self):
        self.allJobs = []
        self.nextPage = ''

    def scrapeCategory(self, category):
        catLink = category.find('a').get('href')
        self.scrapePage(catLink)
        print(self.nextPage)

    def scrapePage(self, catLink):
        pageSource = requests.get(catLink, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text
        pageSoup = BeautifulSoup(pageSource, 'html.parser')

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

            jobObject = {'Title': jobTitle,
                         'Code': jobCode,
                         'Link': jobLink,
                         'Region': jobRegion,
                         'City': jobCity}


            
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


