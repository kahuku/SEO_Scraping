import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.google.com/search?q="
BOTTOM_ID = "botstuff"

class KeywordScraper:
    def __init__(self, keyword):
        self.keyword = keyword
        self.url = self.getURL()
        self.soup = self.getHTML()

    def getURL(self):
        keywords = self.keyword.split(" ")
        url = BASE_URL
        for i in range(len(keywords)):
            url += keywords[i]
            if i < len(keywords) - 1:
                url += "+"
        return url

    def getHTML(self):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}
        content = requests.get(self.url, headers=headers).text
        return BeautifulSoup(content, "html.parser")

    def getRelatedSearches(self):
        bottomDiv = self.soup.find("div", id=BOTTOM_ID)
        links = bottomDiv.find_all("a")
        for link in links:
            print(link["href"])


if __name__ == "__main__":
    keyword = input("Keyword: ")
    scraper = KeywordScraper(keyword)
    scraper.getRelatedSearches()