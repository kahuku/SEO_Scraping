# SEO_Scraping
 
### TO DO
* Protection from getting blocked
  * delaying speed
  * rotating proxies
* More robust error handling and descriptive error messages
* More efficient testing
  * Add capability for testing all functions of one site in a row for fewer requests

### Usage
```angular2html
$ python3 scraper.py --help
usage: python3 scraper.py [-h] [--user-agent USER_AGENT] [--pages PAGES]

optional arguments:
  -h, --help            show this help message and exit
  --user-agent USER_AGENT
                        User agent to send in the web request. 'Random' for
                        random order of preset user agents, 'Rotate' for
                        rotating order
  --pages PAGES         Number of pages of search results to scrape
```