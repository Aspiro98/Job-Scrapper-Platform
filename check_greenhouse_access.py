#!/usr/bin/env python3
"""
Check which companies in COMPANIES have valid Greenhouse job boards
"""
import requests
from run_multi_company_spider import COMPANIES

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

def has_greenhouse_access(url):
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            return False
        text = resp.text.lower()
        for keyword in GREENHOUSE_KEYWORDS:
            if keyword.lower() in text:
                return False
        # Heuristic: look for Greenhouse job board widget
        if 'greenhouse' in text and ('job board' in text or 'open positions' in text or 'apply' in text):
            return True
        # If there are job postings or job-listing elements
        if 'data-mapped' in text or 'opening' in text or 'job-title' in text:
            return True
        return True  # If page loads and no error keywords, assume accessible
    except Exception as e:
        print(f"❌ Error checking {url}: {e}")
        return False

def main():
    print(f"Checking Greenhouse access for {len(COMPANIES)} companies...")
    accessible = []
    inaccessible = []
    for company, url in COMPANIES.items():
        print(f"Checking {company}...", end=' ')
        if has_greenhouse_access(url):
            print("✅ ACCESSIBLE")
            accessible.append(company)
        else:
            print("❌ NOT ACCESSIBLE")
            inaccessible.append(company)
    print(f"\nSummary:")
    print(f"✅ Accessible: {len(accessible)} companies")
    print(f"❌ Not accessible: {len(inaccessible)} companies")
    print(f"\nAccessible companies:")
    for c in accessible:
        print(f"  - {c}")
    print(f"\nNot accessible companies:")
    for c in inaccessible:
        print(f"  - {c}")

if __name__ == "__main__":
    main() 