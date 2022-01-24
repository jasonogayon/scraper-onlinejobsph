import scrapy
import re
import datetime



class JobsSpider(scrapy.Spider):
    name = "jobs"

    base_url = "https://www.onlinejobs.ph"
    search_page = "/jobseekers/jobsearch"


    # Generate Multiple Pages to Scrape
    start_urls = []
    for i in range(15):
        start_urls.append(''.join([base_url, search_page, '/', str(i * 30)]))

    # Keywords Interested In a Post Title
    keywords = [
        'developer',
        'programmer',
        'blockchain',
        'scraper',
        'excel ',
        'illustration',
        'cartoon',
        'artist',
        'python',
    ]
    search_keywords = '|'.join(keywords)

    # Element Selectors
    list_posts = "div.jobpost-cat-box"
    post_date = "p em::text"
    post_role = "h4::text"
    post_client = "p::text"
    post_salary = "dl.no-gutters dd::text"
    post_desc = "div.desc::text"
    post_url = "a"




    # Method to Clean Scraped Text
    def clean(self, text):
        text = text.encode("ascii", "ignore")
        text = text.decode()
        return text.replace("\n",'').replace("\r",' ').strip()



    def parse(self, response):
        current = datetime.datetime.now()
        jobs = response.css(self.list_posts)


        for job in jobs:
            # Only Scrape Posts that are for Today
            date = job.css(self.post_date).get(default='')
            if re.search(str(current.day) + ',', self.clean(date).lower()):

                # Scrape Desired Information
                role = job.css(self.post_role).get(default='')
                client = job.css(self.post_client).get(default='')
                salary = job.css(self.post_salary).get(default='')
                desc = job.css(self.post_desc).get(default='')
                url = self.base_url + job.css(self.post_url)[0].attrib['href']

                if re.search(self.search_keywords, role.lower()):
                    yield {
                        'role': self.clean(role),
                        'client': self.clean(client),
                        'salary': self.clean(salary),
                        'desc': self.clean(desc),
                        'date': date,
                        'url': url,
                    }




# To run:
# scrapy crawl jobs -o jobs.json