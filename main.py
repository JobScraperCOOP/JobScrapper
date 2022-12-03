from bs4 import BeautifulSoup
import requests
import pandas as pd

allJobs = []

# #########################add into class
# Supporting functions
#
def scrapeCategory(category):  
    catLink = category.find('a').get('href')
    # print(catLink)
    scrapePage(catLink)
# 
def scrapePage(catLink):
    pageSource = requests.get(catLink,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text
    pageSoup = BeautifulSoup(pageSource, 'html.parser')
    pageJobs = pageSoup.find_all('tr', class_='job-row')
    
    # jobs = []
    for job in pageJobs:
        jobColumns = job.find_all('td')

        jobLink = job.find('a').get('href')
        jobTitle = job.find('a').string

        jobCode = jobColumns[1].string
        jobRegion = jobColumns[2].string
        jobCity = jobColumns[3].contents[0].replace(' ','')

        allJobs.append({'Title':jobTitle,'Code':jobCode,'Link':jobLink,'Region':jobRegion,'City':jobCity})


    # print(allJobs)
    allJobsDf = pd.DataFrame(allJobs)
    print(allJobsDf)
    
    allJobsDf.to_csv('jobs.csv',encoding='utf-8-sig')
    

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

print(categories)



# ===============================TESTING AREA ===============================
# Testing all categories
# 
# for caterogy in categories:
#     scrapeCategory(caterogy)
#     print('----------')

# Testing one category
# 
scrapeCategory(categories[0])

# print(df)

# =============================================================
