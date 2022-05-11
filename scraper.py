import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.google.com/search?q="
BOTTOM_ID = "botstuff"
GOOGLE_BASE_URL = "https://www.google.com"

class Scraper:
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
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
                                 "like Gecko) Chrome/101.0.4951.54 Safari/537.36"}
        content = requests.get(self.url, headers=headers).text
        return BeautifulSoup(content, "html.parser")

    def getLinks(self):
        bottomDiv = self.soup.find("div", id=BOTTOM_ID)
        links = bottomDiv.find_all("a")
        links = [GOOGLE_BASE_URL + link["href"] for link in links]
        return links

    def getSearchesFromLinks(self, links):
        searches = []
        for link in links:
            try:
                unformattedSearch = link.split("search?q=")[1].split("&")[0]
                searchList = unformattedSearch.split("+")
                search = ""
                for i in range(len(searchList)):
                    search += searchList[i]
                    if (i < len(searchList) - 1) and (searchList[i] != "-"):
                         search += " "
                searches.append(search)
            except IndexError as e:
                pass
                # print(e)
        return searches

    def getRelatedSearches(self):
        links = self.getLinks()
        searches = self.getSearchesFromLinks(links)
        return searches if len(searches) > 0 else "No related searches found"

if __name__ == "__main__":
    keyword = input("Keyword: ")
    scraper = Scraper(keyword)
    print(scraper.getRelatedSearches())