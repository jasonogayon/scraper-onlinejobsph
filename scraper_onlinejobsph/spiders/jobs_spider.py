import scrapy
import re
import datetime



class JobsSpider(scrapy.Spider):
    name = "jobs"

    base_url = "https://www.onlinejobs.ph"
    search_page = "/jobseekers/jobsearch"


    # Keywords Interested In a Post Title
    keywords = [
        'automation',
        'developer',
        'programmer',
        'blockchain',
        'scraper',
        'excel ',
        'illustration',
        'cartoon',
        'artist',
        'python',
        'javascript',
        'cypress',
        'tester',
        'game',
        'robomotion'
    ]
    search_keywords = '|'.join(keywords)

    # Exclusions Not Interested In a Post Title
    exclusions = [
        'virtual assistant',
        'magento',
        'social media',
        'angular',
        'php',
        'female'
    ]
    search_exclusions = '|'.join(exclusions)


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





    def __init__(self, offset='', **kwargs):

        self.start_urls = []
        self.offset = int(offset)

        if self.offset < 2:
            start = 0
        else:
            start = (self.offset * 25)
        end = start + 25

        # Generate Multiple Pages to Scrape
        for i in range(start, end):
            self.start_urls.append(''.join([self.base_url, self.search_page, '/', str(i * 30)]))
        super().__init__(**kwargs)



    def parse(self, response):
        today = datetime.date.today()
        period = today - datetime.timedelta(self.offset)

        jobs = response.css(self.list_posts)


        for job in jobs:
            # Only Scrape Posts that are for Today or Yesterday
            date = job.css(self.post_date).get(default='')
            if re.search(str(period.day) + ',', self.clean(date).lower()):

                # Scrape Desired Information
                role = job.css(self.post_role).get(default='')
                client = job.css(self.post_client).get(default='')
                salary = job.css(self.post_salary).get(default='')
                desc = job.css(self.post_desc).get(default='')
                url = self.base_url + job.css(self.post_url)[0].attrib['href']

                keywords_in_post = re.search(self.search_keywords, role.lower());
                exclusions_in_post = re.search(self.search_exclusions, role.lower());

                if keywords_in_post and not exclusions_in_post:
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