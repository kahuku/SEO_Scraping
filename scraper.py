import requests
from bs4 import BeautifulSoup
import re
import argparse
import json
import random
import sys

BASE_URL = "https://www.google.com/search?q="
PAGE_URL = "&start="
BOTTOM_ID = "botstuff"
BODY_ID = "center_col"
GOOGLE_BASE_URL = "https://www.google.com"

parser = argparse.ArgumentParser("python3 manual_tsting.py")
parser.add_argument('--user-agent', default="Random",
                    help="User agent to send in the web request. 'Random' for random order"
                         " of preset user agents, 'Rotate' for rotating order")
parser.add_argument('--pages', default=2, help="Number of pages of search results to scrape")

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

def getUserAgent():
    index = BasicScraper.getIndex()
    agents = []
    with open("user_agents.json") as data:
        agents = json.load(data)["data"]
    agent = agents[index % len(agents)]
    # print(agent)
    return agent

class BasicScraper:
    index = -1

    def __init__(self, keyword, pages):
        self.keyword = keyword
        self.pages = pages
        self.urls = self.getURLs()
        self.soups = self.getSoups()

    @staticmethod
    def getIndex():
        if 'args' in locals():
            if args.user_agent == "Random":
                return random.randint(0, sys.maxsize)
            else:
                BasicScraper.index += 1
                return BasicScraper.index
        else:
            return random.randint(0, sys.maxsize)

    def setPages(self, pages):
        self.pages = pages

    def getURL(self, page):
        keywords = self.keyword.split(" ")
        url = BASE_URL
        for i in range(len(keywords)):
            url += keywords[i]
            if i < len(keywords) - 1:
                url += "+"
        url += PAGE_URL
        url += str(10 * page)
        return url

    def getURLs(self):
        urls = []
        for i in range(self.pages):
            urls.append(self.getURL(i))
        return urls

    def getSoup(self, url):
        userAgent = getUserAgent()
        headers = {"User-Agent": userAgent}
        content = requests.get(url, headers=headers).text
        return BeautifulSoup(content, "html.parser")

    def getSoups(self):
        soups = []
        for i in range(len(self.urls)):
            soups.append(self.getSoup(self.urls[i]))
        return soups

    def getLinks(self, id):
        links = []
        for soup in self.soups:
            div = soup.find("div", id=id)
            if div is not None:
                aTags = div.find_all("a")
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
            else:
                # print(soup)
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
    args = parser.parse_args()

    keyword = input("Keyword: ").lower()
    site = input("Site: ").lower()

    scraper = BasicScraper(keyword, args.pages)

    print(scraper.getRelatedSearches())
    print()
    print(scraper.getSearchResults())
    print(len(scraper.getSearchResults()))
    print()
    print(scraper.getRanking(site))
