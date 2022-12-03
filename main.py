import requests
from bs4 import BeautifulSoup
from classes import Elbit


elbit = Elbit.Elbit()
url = 'https://elbitsystemscareer.com/'
categoryClass = "item-practice"

source = requests.get(
    url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}).text

soup = BeautifulSoup(source, 'html.parser')

categories = soup.find_all('div', class_=categoryClass)

for i in range(3):
    print(i)
    elbit.scrapeCategory(categories[i])
