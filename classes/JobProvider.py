class JobProvider:
    def __init__(self):
        self.base_url = None
# FIXME: decide on the interface of this class, and have all other classes implement it
#   Suggestion:
#   - this class should have method to generate an array of Job listing (new class to create)
#   - generally, this class handles only with scraping the website to get the raw data

