import requests
from bs4 import BeautifulSoup
import re

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

class BasicScraper:
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
        for a in aTags:
            try:
                if a["href"][0] == "/":
                    links.append(GOOGLE_BASE_URL + a["href"])
                elif a["href"][0] == "#":
                    pass
                elif a["href"] not in links:
                    links.append(a["href"])
            except Exception as e:
                pass
        return links

    def getRelatedSearches(self):
        links = self.getLinks(BOTTOM_ID)
        searches = getSearchesFromLinks(links)
        return searches if len(searches) > 0 else "No related searches found"

    def getSearchResults(self):
        return getNonGoogleLinks(self.getLinks(BODY_ID))

    def formatRanking(self, site, rank, result=None):
        site = site[0].upper() + site[1:]
        if (rank > 0):
            return site + "'s ranking for search term '" + self.keyword + "': " + str(rank) + " (" + result + ")"
        else:
            return site + " does not appear in the search results for search term '" + self.keyword + "'"

    def getRanking(self, site):
        searchResults = self.getSearchResults()
        i = 1
        for result in searchResults:
            try:
                domains = re.search('https?://([A-Za-z_0-9.-]+).*', result).group(1)
                if site in domains:
                    return self.formatRanking(site, i, result)
                i += 1
            except AttributeError as e:
                pass
                # print(e)
        return self.formatRanking(site, -1)

if __name__ == "__main__":
    keyword = input("Keyword: ").lower()
    site = input("Site: ").lower()

    scraper = BasicScraper(keyword)

    print(scraper.getRelatedSearches())
    print()
    print(scraper.getSearchResults())
    print()
    print(scraper.getRanking(site))
