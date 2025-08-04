import sys
import scrapy
import time
from scrapy.crawler import CrawlerProcess
from scrapers.spiders.greenhouse_jobs_outline_spider import (
    GreenhouseJobsOutlineSpider,
)
from scrapers.spiders.greenhouse_job_departments_spider import (
    GreenhouseJobDepartmentsSpider,
)
from scrapers.spiders.lever_jobs_outline_spider import LeverJobsOutlineSpider
from scrapers.utils import general as util
from scrapy.utils.project import get_project_settings

# Set required environment variable
import os
os.environ['HASHIDS_SALT'] = 'test_salt_for_development'

process = CrawlerProcess(get_project_settings())

# Example URL - you can change this or pass it as command line argument
if len(sys.argv) > 1:
    careers_page_url = sys.argv[1]
else:
    # Default example URL
    careers_page_url = "https://boards.greenhouse.io/embed/job_board?for=example"

run_hash = util.hash_ids.encode(int(time.time()))

print(f"Running spider for URL: {careers_page_url}")

if careers_page_url.split(".")[1] == "greenhouse":
    process.crawl(
        GreenhouseJobDepartmentsSpider,
        careers_page_url=careers_page_url,
        use_existing_html=False,
        run_hash=run_hash,
    )
    process.crawl(
        GreenhouseJobsOutlineSpider,
        careers_page_url=careers_page_url,
        use_existing_html=False,
        run_hash=run_hash,
    )
elif careers_page_url.split(".")[1] == "lever":
    process.crawl(
        LeverJobsOutlineSpider,
        careers_page_url=careers_page_url,
        use_existing_html=False,
        run_hash=run_hash,
    )
else:
    print("URL must be from greenhouse.io or lever.co domain")
    sys.exit(1)

process.start() 