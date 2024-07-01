import scrapy
from ..items import GitscrapeItem
import pandas as pd
from datetime import datetime
class GitSpider(scrapy.Spider):
    

    name='scrapxl'
    with open('repos.csv') as source:
         start_urls = [line.strip()for line in source]

    csv_array=[['page_url','url','2000-01-01T10:10:10.000Z']]
    # temp_page_url=""
    # temp_url=""
    # temp_date=""
    # csv_count=0
    check_arr=['ex.com']
    with open("valid_urls.txt","w") as g:
        g.write("")
        g.close()

    def parse(self,response):
        #  items=GitscrapeItem()

         if "github.com" in response.url or "githubusercontent.com" in response.url :
            self.logger.info(f"Valid Github URL:{response.url}")
            links=response.css('.Link--primary::attr(href)').getall()
            # csv_count=0
            # csv_succ_count=0
            og_url=response.url
            for link in links:
                file_URL=response.urljoin(link)
                if "tree" in file_URL:
                    yield response.follow(file_URL, callback=self.parse)
                file_extension = file_URL.split('.')[-1]
                if file_extension in ['csv','xlsx']:
                    # csv_count+=1
                    blob_URL=file_URL
                    file_URL=file_URL.replace('blob/','')
                    file_URL=file_URL.replace('github.com','raw.githubusercontent.com')
                    if file_extension=='csv':
                            self.logger.info(f"CSV File found at {file_URL}")
                            try:
                                dl_df=pd.read_csv(file_URL)
                                cr_df=pd.read_csv('submission_format.csv')
                                if (cr_df['respondent_id'].equals(dl_df['respondent_id'])):
                                    if (cr_df['h1n1_vaccine'].equals(dl_df['h1n1_vaccine'])):
                                            self.logger.info(f"CSV satisfying all criteria found at:{file_URL}")
                                            # csv_succ_count+=1
                                            # self.temp_page_url=og_url
                                            # self.temp_url=file_URL
                                            meta={'pageURL':og_url, 'fileURL':file_URL}
                                            yield response.follow(blob_URL, callback=self.extractTime, meta=meta)
                                else: self.logger.info(f"CSV at:{file_URL} does not satisfy all criteria. Skipping..")
                            except Exception as e: self.logger.info(f"CSV at {file_URL} could not be processed and threw exception{str(e)}. It does not meet submission criteria.")
                    if file_extension=='xlsx':
                            self.logger.info(f"XLSX File found at {file_URL}")
                            try:
                                dl_df=pd.read_excel(file_URL)
                                cr_df=pd.read_csv('submission_format.csv')
                                if (cr_df['respondent_id'].equals(dl_df['respondent_id'])):
                                    if (cr_df['h1n1_vaccine'].equals(dl_df['h1n1_vaccine'])):
                                            self.logger.info(f"XLSX satisfying all criteria found at:{file_URL}")
                                            # csv_succ_count+=1
                                            # self.temp_page_url=og_url
                                            # self.temp_url=file_URL
                                            meta={'pageURL':og_url, 'fileURL':file_URL}
                                            yield response.follow(blob_URL, callback=self.extractTime, meta=meta)
                                else: self.logger.info(f"XLSX at:{file_URL} does not satisfy all criteria. Skipping..")
                            except Exception as e: self.logger.info(f"XLSX at {file_URL} could not be processed and threw exception{str(e)}. It does not meet submission criteria.")

            



         else:
            if "github" not in response.url:
                self.logger.info(f"Invalid URL:{response.url}")
         yield response.follow(response.url, callback=self.check)
    def extractTime(self, response):
        # tempd=response.css('').extract()
        # self.temp_date=tempd[0][11:]
        # self.logger.info(f"date captured as {self.temp_date} ")
        # self.csv_array.append([self.temp_page_url, self.temp_url, self.temp_date])
         # Extract the JSON data from the script tag
        script_content = str(response.css('script[type="application/json"]::text').extract())
        key='createdAt'
        key_pos = script_content.find(key)
            
            # Check if the key is found
                # Calculate the position where the value starts (after the key and the colon)
        value_start_pos = key_pos + len(key) + 3  
        date_temp = script_content[value_start_pos:value_start_pos + 24]
        self.logger.info(f"uniqdate:{date_temp}, for {response.meta['pageURL']}")
        # self.temp_date=date_temp
        self.csv_array.append([response.meta['pageURL'],response.meta['fileURL'], date_temp])
        yield response.follow(response.meta['pageURL'], callback=self.check)
                


    def check(self,response):
              items=GitscrapeItem()
            #   links=response.css('.Link--primary::attr(href)').getall()
            #   if all(link in self.checked_burl or 'tree' in link for link in links):
              if(len(self.csv_array)==1): self.logger.info(f"No CSV or XLSX Files found at {response.url}")
                # if(len(self.csv_array)==2):
                #     self.logger.info(f"Only one file satisfying conditions at {self.temp_page_url}, Saving..")
                #     # self.logger.info(f"uniqurl {self.temp_url}, Saving..")
                #     with open("valid_urls.txt","a") as f:
                #         f.write(f"{self.temp_url}\n")
                #         f.close()
                #     items['file_urls']=[self.temp_url]
                #     self.csv_array=[['page_url','url','2000-01-01T10:10:10.000Z']]
                #     yield items
              if(len(self.csv_array)>1):
                    most_recent_date=None
                    most_recent_url=""
                    page_url=""
                    # self.logger.info(f"uniqarray{self.csv_array}")
                    for entry in self.csv_array:
                        url1,url2,date_str=entry
                        date=datetime.fromisoformat(date_str.replace("Z","+00:00"))
                        
                        if most_recent_date is None or date>most_recent_date:
                            most_recent_date=date
                            most_recent_url=url2
                            page_url=url1

                    
                    if(most_recent_url != ""):
                     if (most_recent_url not in self.check_arr):
                        self.check_arr.append(most_recent_url)
                        self.logger.info(f"{len(self.csv_array)-1} csv/xlsx files satisfying conditions were found at {page_url}. Most recent one is at {most_recent_url} and was uploaded on {most_recent_date}. Saving..")
                        with open("valid_urls.txt","a") as f:
                            f.write(f"{most_recent_url}\n")
                            f.close()
                        items['file_urls']=[most_recent_url]
                        self.csv_array=[['page_url','url','2000-01-01T10:10:10.000Z']]
                        # self.csv_count=0
                        yield items
            #   self.csv_count=0
              yield response.follow(response.url, callback=self.parse)
                