import requests
from bs4 import BeautifulSoup
from classes import Elbit,Iai,Refael
import time


elbit = Elbit.Elbit()
elbit.scrapeAllCategories()
print("Done with elbit:")
print(time.process_time())


iai = Iai.Iai()
iai.scrapeAllJobs()
print("Done with iai:")
print(time.process_time())


# refael = Refael.Refael()
# refael.scrapeAllJobs()
# print("Done with refael:")
# print(time.process_time())







