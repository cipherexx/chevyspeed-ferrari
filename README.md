# chevyspeed-ferrari
## **Gitscrape by cipherexx**
This is a tool built with scrapy that can be used to scrape **.csv** or **.xlsx** files from a given list of github repositories.



## Dependencies

 1. Scrapy
 Installation: 
 `pip install scrapy`
2. Pandas
 Installation:
 `pip install pandas`

## Usage
After downloading the files, switch to the outer gitscrape directory and run
`scrapy crawl scrapxl`
The spider will then crawl to each one of the websites provided in repos.csv, and check it against submission_format.csv. This is currently set as per a given challenge but can be changed to meet needs in spiders/scrap.py. A log of the ongoing process is made at spider_log.log and can be used to check which websites were crawled, whether they were valid links, whether they contained csv or excel files and check if any matches were found. 

Found matches are saved to outputfiles/full and their URLs are written to valid_urls.txt. As is the default in scrapy, the file names are a SHA-1 hash of their URLs.

## Speed and Thoroughness

The configuration of the files has been done with a completionist perspective, which would mean that the user may find the scraping to be particularly slow when it comes to yielding downloaded files. This has been done intentionally in order to ensure that files are not skipped. However, even with this setting, the scraper may miss a file or two. 

If you wish for the scraper to run faster, at the cost of thoroughness, open settings.py and find the line
 `DOWNLOAD_DELAY = 1.51`
 and reduce the number for desired output.  The output slowly degrades till 0.5 where you can get an approximate efficiency of 85%. Going below 0.5 is not recommended for this particular tool.
 Another way to increase speed is to increase the number of concurrent requests. Find the line
  `CONCURRENT_REQUESTS = 28` 
  and increase it as needed. However please note that a high number of requests can cause huge traffic on the website and is unethical. (~~It is also an easy way to accidentally launch a DDoS Attack~~) 

## Known Issues

At the time of uploading this, there are a few known issues as follows:
1. The last file to turn out positive is not downloaded or written to valid_urls.txt since scrapy closes the connection as soon as it is done crawling.
2. There is a lot of repetition in spider_log.log. This is actually a result of the tool running through websites multiple times to avoid skipping files and because of retrying in case of unprecedented HTTP responses.
3. The tool is set to ignore robots.txt which is unethical. 
