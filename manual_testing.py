import argparse
import json

import scraper as Scraper

parser = argparse.ArgumentParser("python3 manual_tsting.py")
parser.add_argument('--related', default=False, help="Find related search terms")
parser.add_argument('--results', default=False, help="Return links from first page of Google search")
parser.add_argument('--cases', default=-1, help="How many cases of each test to run")

def toDict(dataList):
    dict = {}
    for entry in dataList:
        dict[entry["siteName"]] = entry["info"]
    return dict

if __name__ == "__main__":
    args = parser.parse_args()
    args.cases = int(args.cases)

    dataList = []
    with open("dict.json") as data:
        dataList = json.load(data)["data"]

    dataDict = toDict(dataList)
    keys = list(dataDict.keys())

    if args.related:
        print("RELATED SEARCHES:")
        if args.cases == -1:
            for key in keys:
                scraper = Scraper.BasicScraper(key)
                print(scraper.getRelatedSearches())
        else:
            for i in range(args.cases):
                scraper = Scraper.BasicScraper(keys[i])
                print(scraper.getRelatedSearches())
        print()

    if args.results:
        print("SEARCH RESULTS:")
        if args.cases == -1:
            for key in keys:
                scraper = Scraper.BasicScraper(key)
                print(scraper.getSearchResults())
        else:
            for i in range(args.cases):
                scraper = Scraper.BasicScraper(keys[i])
                print(scraper.getSearchResults())