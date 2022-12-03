from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

allJobs = []
nextPage = ''

def scrapeCategory(category):
    catLink = category.find('a').get('href')
    scrapePage(catLink)
    print(nextPage)



def scrapePage(catLink):
    pageSource = requests.get(catLink, headers={
                              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text
    pageSoup = BeautifulSoup(pageSource, 'html.parser')

    pageJobs = pageSoup.find_all('tr', class_='job-row')
    # print('after find  '+ str(time.perf_counter()))
    for job in pageJobs:
        jobColumns = job.find_all('td')

        jobLink = 'https://elbitsystemscareer.com' + job.find('a').get('href')
        jobTitle = job.find('a').string

        jobCode = jobColumns[1].string
        jobRegion = jobColumns[2].string
        jobCity = jobColumns[3].contents[0].replace(' ', '')

        jobObject = {'Title': jobTitle, 'Code': jobCode,
                     'Link': jobLink, 'Region': jobRegion, 'City': jobCity}


        # Inside job description page
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
        allJobs.append(jobObject)

    # Class of next button if available: 'next back-steps enabled'
    try:
        nextPage = pageSoup.find('a', 'next back-steps enabled').get('href')
    except Exception:
        nextPage = ''
    # print(allJobs)

    # Export to CSV later DB
    # allJobsDf = pd.DataFrame(allJobs)
    # allJobsDf.to_csv('jobs.csv',encoding='utf-8-sig')
    print('Ending page')
######


# Parameters
#

url = 'https://elbitsystemscareer.com/'
categoryClass = "item-practice"

#
source = requests.get(
    url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text

soup = BeautifulSoup(source, 'html.parser')

categories = soup.find_all('div', class_=categoryClass)

# print(categories)


# ===============================TESTING AREA ===============================
# Testing all categories
#
# for caterogy in categories:
#     scrapeCategory(caterogy)
#     print('----------')

# Testing one category
#
for i in range(3):
    print(i)
    scrapeCategory(categories[i])

# print(df)

# =============================================================
