#!/usr/bin/env python3
"""
Check which companies in COMPANIES were actually scraped, and check accessibility of missing companies' URLs.
"""
import json
import requests
from run_multi_company_spider import COMPANIES

SCRAPED_FILE = 'scraped_data.json'

GREENHOUSE_KEYWORDS = [
    'This job board no longer exists',
    'Page Not Found',
    '404',
    'No jobs found',
    'does not have any active jobs',
    'not available',
    'not found',
    'error',
    'Oops!'
]

def is_url_accessible(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return False, f"HTTP {resp.status_code}"
        text = resp.text.lower()
        for keyword in GREENHOUSE_KEYWORDS:
            if keyword.lower() in text:
                return False, f"Keyword found: {keyword}"
        return True, "OK"
    except Exception as e:
        return False, str(e)

def main():
    # Load scraped data
    try:
        with open(SCRAPED_FILE, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading {SCRAPED_FILE}: {e}")
        return
    
    # Get set of companies in scraped data
    scraped_companies = set()
    for job in data:
        company = job.get('company_name') or job.get('company')
        if company:
            scraped_companies.add(company.lower())
    
    # Get set of companies in COMPANIES
    code_companies = set(COMPANIES.keys())
    
    # Print results
    print(f"\nCompanies in spider code: {len(code_companies)}")
    print(f"Companies actually scraped: {len(scraped_companies)}")
    
    print(f"\n✅ Companies scraped:")
    for c in sorted(scraped_companies):
        print(f"  - {c}")
    
    missing = sorted(code_companies - scraped_companies)
    print(f"\n❌ Companies in code but NOT scraped:")
    for c in missing:
        print(f"  - {c}")
    
    print(f"\n🔍 Checking accessibility of missing companies' URLs:")
    for c in missing:
        url = COMPANIES[c]
        print(f"Checking {c}: {url}")
        accessible, reason = is_url_accessible(url)
        if accessible:
            print(f"   ✅ Accessible")
        else:
            print(f"   ❌ Not accessible: {reason}")
            # Suggest user to update the URL manually
            print(f"   💡 Please check for an updated Greenhouse or careers URL for {c} and update COMPANIES.")
    
    print(f"\n✅ Companies in both code and scraped: {len(scraped_companies & code_companies)}")
    print(f"❌ Companies missing from scraped: {len(code_companies - scraped_companies)}")

if __name__ == "__main__":
    main() 