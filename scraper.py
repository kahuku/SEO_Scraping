import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.google.com/search?q="
BOTTOM_ID = "botstuff"
BODY_ID = "center_col"
GOOGLE_BASE_URL = "https://www.google.com"

def getSearchesFromLinks(links):
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

def getNonGoogleLinks(links):
    return [link for link in links if not "google" in link]

class Scraper:
    def __init__(self, keyword):
        self.keyword = keyword
        self.url = self.getURL()
        self.soup = self.getSoup()

    def getURL(self):
        keywords = self.keyword.split(" ")
        url = BASE_URL
        for i in range(len(keywords)):
            url += keywords[i]
            if i < len(keywords) - 1:
                url += "+"
        return url

    def getSoup(self):
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, "
                                 "like Gecko) Chrome/101.0.4951.54 Safari/537.36"}
        content = requests.get(self.url, headers=headers).text
        return BeautifulSoup(content, "html.parser")

    def getLinks(self, id):
        div = self.soup.find("div", id=id)
        aTags = div.find_all("a")
        links = []
        for link in aTags:
            try:
                if link["href"][0] == "/":
                    links.append(GOOGLE_BASE_URL + link["href"])
                elif link["href"][0] == "#":
                    pass
                else:
                    links.append(link["href"])
            except Exception as e:
                pass
        return links

    def getRelatedSearches(self):
        links = self.getLinks(BOTTOM_ID)
        searches = getSearchesFromLinks(links)
        return searches if len(searches) > 0 else "No related searches found"

    def getSearchResults(self):
        return getNonGoogleLinks(self.getLinks(BODY_ID))

if __name__ == "__main__":
    keyword = input("Keyword: ")
    scraper = Scraper(keyword)
    print(scraper.getRelatedSearches())
    print()
    scraper.getSearchResults()
