import sys
import scrapy
import time
import os
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
os.environ['HASHIDS_SALT'] = 'test_salt_for_development'

# Popular companies to scrape
COMPANIES = {
    'airbnb': 'https://boards.greenhouse.io/embed/job_board?for=airbnb',
    'stripe': 'https://boards.greenhouse.io/embed/job_board?for=stripe',
    'square': 'https://boards.greenhouse.io/embed/job_board?for=square',
    'robinhood': 'https://boards.greenhouse.io/embed/job_board?for=robinhood',
    'coinbase': 'https://boards.greenhouse.io/embed/job_board?for=coinbase',
    'databricks': 'https://boards.greenhouse.io/embed/job_board?for=databricks',
    'figma': 'https://boards.greenhouse.io/embed/job_board?for=figma',
    'notion': 'https://boards.greenhouse.io/embed/job_board?for=notion',
    'asana': 'https://boards.greenhouse.io/embed/job_board?for=asana',
    'dropbox': 'https://boards.greenhouse.io/embed/job_board?for=dropbox',
    'hubspot': 'https://boards.greenhouse.io/embed/job_board?for=hubspotjobs',
    'fastly': 'https://boards.greenhouse.io/embed/job_board?for=fastly',
    'spacex': 'https://boards.greenhouse.io/embed/job_board?for=spacex',
    'shelf': 'https://boards.greenhouse.io/embed/job_board?for=shelf',
    'remotecom': 'https://job-boards.greenhouse.io/embed/job_board?for=remotecom',
    'andurilindustries': 'https://boards.greenhouse.io/embed/job_board?for=andurilindustries',
    'journey': 'https://boards.greenhouse.io/embed/job_board?for=journey',
    'seatgeek': 'https://boards.greenhouse.io/embed/job_board?for=seatgeek',
    'honor': 'https://boards.greenhouse.io/embed/job_board?for=honor',
    'duolingo': 'https://boards.greenhouse.io/embed/job_board?for=duolingo',
    'dydx': 'https://boards.greenhouse.io/embed/job_board?for=dydx',
    'appliedintuition': 'https://boards.greenhouse.io/embed/job_board?for=appliedintuition',
    'tubitv': 'https://boards.greenhouse.io/embed/job_board?for=tubitv',
    'calendly': 'https://boards.greenhouse.io/embed/job_board?for=calendly',
    'flexport': 'https://boards.greenhouse.io/embed/job_board?for=flexport',
    'headway': 'https://boards.greenhouse.io/embed/job_board?for=headway',
    'cloudflare': 'https://boards.greenhouse.io/embed/job_board?for=cloudflare',
    'substack': 'https://boards.greenhouse.io/embed/job_board?for=substack',
    'checkr': 'https://boards.greenhouse.io/embed/job_board?for=checkr',
    'braze': 'https://boards.greenhouse.io/embed/job_board?for=braze',
    'wikimedia': 'https://boards.greenhouse.io/embed/job_board?for=wikimedia',
    'point72': 'https://boards.greenhouse.io/embed/job_board?for=point72',
    'life360': 'https://boards.greenhouse.io/embed/job_board?for=life360',
    'hazel': 'https://boards.greenhouse.io/embed/job_board?for=hazel',
    'axon': 'https://boards.greenhouse.io/embed/job_board?for=axon',
    'redpandadata': 'https://boards.greenhouse.io/embed/job_board?for=redpandadata',
    'earnin': 'https://boards.greenhouse.io/embed/job_board?for=earnin',
    'avalabsecosystem': 'https://boards.greenhouse.io/embed/job_board?for=avalabsecosystem',
    'lambda': 'https://boards.greenhouse.io/embed/job_board?for=lambda',
    'luminar': 'https://boards.greenhouse.io/embed/job_board?for=luminar',
    'aetherbiomachines': 'https://boards.greenhouse.io/embed/job_board?for=aetherbiomachines',
    'fountain': 'https://boards.greenhouse.io/embed/job_board?for=fountain',
    'semgrep': 'https://boards.greenhouse.io/embed/job_board?for=semgrep',
    'temporaltechnologies': 'https://job-boards.greenhouse.io/embed/job_board?for=temporaltechnologies'
}



def run_spider_for_company(company_name, careers_url):
    """Run spider for a specific company"""
    print(f"\n🔄 Scraping jobs for {company_name.upper()}...")
    print(f"URL: {careers_url}")
    
    # Use a single process for all spiders
    process = CrawlerProcess(get_project_settings())
    
    # Run both spiders for the company
    process.crawl(
        GreenhouseJobDepartmentsSpider,
        careers_page_url=careers_url,
        run_hash=f"{company_name}_{int(time.time())}"
    )
    
    process.crawl(
        GreenhouseJobsOutlineSpider,
        careers_page_url=careers_url,
        run_hash=f"{company_name}_{int(time.time())}"
    )
    
    return process

def main():
    """Main function to scrape multiple companies"""
    process = CrawlerProcess(get_project_settings())
    
    if len(sys.argv) > 1:
        # If specific companies provided
        companies_to_scrape = sys.argv[1:]
        for company in companies_to_scrape:
            if company in COMPANIES:
                print(f"\n🔄 Adding {company.upper()} to scraping queue...")
                careers_url = COMPANIES[company]
                
                # Add both spiders for the company
                process.crawl(
                    GreenhouseJobDepartmentsSpider,
                    careers_page_url=careers_url,
                    run_hash=f"{company}_{int(time.time())}"
                )
                
                process.crawl(
                    GreenhouseJobsOutlineSpider,
                    careers_page_url=careers_url,
                    run_hash=f"{company}_{int(time.time())}"
                )
            else:
                print(f"❌ Company '{company}' not found in our list")
    else:
        # Scrape all companies
        print("🚀 Starting multi-company job scraping...")
        print(f"📊 Total companies available: {len(COMPANIES)}")
        
        # Scrape all companies
        print(f"🎯 Scraping all {len(COMPANIES)} companies...")
        for company, careers_url in COMPANIES.items():
            print(f"\n🔄 Adding {company.upper()} to scraping queue...")
            
            # Add both spiders for the company
            process.crawl(
                GreenhouseJobDepartmentsSpider,
                careers_page_url=careers_url,
                run_hash=f"{company}_{int(time.time())}"
            )
            
            process.crawl(
                GreenhouseJobsOutlineSpider,
                careers_page_url=careers_url,
                run_hash=f"{company}_{int(time.time())}"
            )
    
    # Start all spiders at once
    print("\n🚀 Starting all spiders...")
    process.start()
    print("✅ Completed multi-company scraping!")

if __name__ == "__main__":
    main() 