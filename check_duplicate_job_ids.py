#!/usr/bin/env python3
"""
Check for Duplicate Job IDs
Identifies duplicate job IDs in scraped_data.json that could cause automation issues
"""

import json
from collections import defaultdict
from typing import Dict, List, Any

def check_duplicate_job_ids():
    """Check for duplicate job IDs in scraped data"""
    
    print("🔍 Checking for Duplicate Job IDs in scraped_data.json")
    print("=" * 60)
    
    try:
        # Load scraped data
        with open('scraped_data.json', 'r') as f:
            data = json.load(f)
        
        print(f"📊 Total records in scraped_data.json: {len(data)}")
        
        # Filter for jobs with opening_title (actual job postings)
        jobs = [job for job in data if 'opening_title' in job]
        print(f"📋 Total job postings: {len(jobs)}")
        
        # Check for duplicate job IDs
        job_id_counts = defaultdict(list)
        for job in jobs:
            job_id = job.get('id')
            if job_id:
                job_id_counts[job_id].append(job)
        
        # Find duplicates
        duplicates = {job_id: jobs_list for job_id, jobs_list in job_id_counts.items() if len(jobs_list) > 1}
        
        if duplicates:
            print(f"\n❌ Found {len(duplicates)} duplicate job IDs!")
            print("=" * 60)
            
            for job_id, jobs_list in duplicates.items():
                print(f"\n🆔 Duplicate Job ID: {job_id}")
                print(f"   📊 Number of jobs with this ID: {len(jobs_list)}")
                print(f"   📋 Jobs with this ID:")
                
                for i, job in enumerate(jobs_list, 1):
                    company = job.get('company_name', 'Unknown')
                    title = job.get('opening_title', 'Unknown')
                    url = job.get('opening_link', 'No URL')
                    job_board = job.get('job_board', 'Unknown')
                    
                    print(f"      {i}. Company: {company}")
                    print(f"         Title: {title}")
                    print(f"         Job Board: {job_board}")
                    print(f"         URL: {url}")
                    print()
            
            print("⚠️  This could cause automation to open the wrong company's job page!")
            print("💡 Solution: Fix job ID generation logic in scrapers to ensure uniqueness")
            
        else:
            print(f"\n✅ No duplicate job IDs found!")
            print("🎉 Job ID uniqueness is maintained")
        
        # Check for other potential issues
        print(f"\n🔍 Additional Checks:")
        print("=" * 40)
        
        # Check for jobs without IDs
        jobs_without_id = [job for job in jobs if not job.get('id')]
        if jobs_without_id:
            print(f"❌ Found {len(jobs_without_id)} jobs without IDs:")
            for job in jobs_without_id[:5]:  # Show first 5
                print(f"   - {job.get('company_name', 'Unknown')}: {job.get('opening_title', 'Unknown')}")
            if len(jobs_without_id) > 5:
                print(f"   ... and {len(jobs_without_id) - 5} more")
        else:
            print(f"✅ All jobs have IDs")
        
        # Check for jobs without URLs
        jobs_without_url = [job for job in jobs if not job.get('opening_link')]
        if jobs_without_url:
            print(f"❌ Found {len(jobs_without_url)} jobs without URLs:")
            for job in jobs_without_url[:5]:  # Show first 5
                print(f"   - {job.get('company_name', 'Unknown')}: {job.get('opening_title', 'Unknown')}")
            if len(jobs_without_url) > 5:
                print(f"   ... and {len(jobs_without_url) - 5} more")
        else:
            print(f"✅ All jobs have URLs")
        
        # Check for jobs without company names
        jobs_without_company = [job for job in jobs if not job.get('company_name')]
        if jobs_without_company:
            print(f"❌ Found {len(jobs_without_company)} jobs without company names:")
            for job in jobs_without_company[:5]:  # Show first 5
                print(f"   - Title: {job.get('opening_title', 'Unknown')}")
                print(f"     URL: {job.get('opening_link', 'No URL')}")
            if len(jobs_without_company) > 5:
                print(f"   ... and {len(jobs_without_company) - 5} more")
        else:
            print(f"✅ All jobs have company names")
        
        # Show company distribution
        print(f"\n📊 Company Distribution:")
        print("=" * 40)
        company_counts = defaultdict(int)
        for job in jobs:
            company = job.get('company_name', 'Unknown')
            company_counts[company] += 1
        
        # Sort by count (descending)
        sorted_companies = sorted(company_counts.items(), key=lambda x: x[1], reverse=True)
        
        print(f"🏢 Top 10 companies by job count:")
        for i, (company, count) in enumerate(sorted_companies[:10], 1):
            print(f"   {i:2d}. {company}: {count} jobs")
        
        if len(sorted_companies) > 10:
            print(f"   ... and {len(sorted_companies) - 10} more companies")
        
        # Show job board distribution
        print(f"\n🌐 Job Board Distribution:")
        print("=" * 40)
        job_board_counts = defaultdict(int)
        for job in jobs:
            job_board = job.get('job_board', 'Unknown')
            job_board_counts[job_board] += 1
        
        for job_board, count in job_board_counts.items():
            print(f"   📋 {job_board}: {count} jobs")
        
        return duplicates
        
    except FileNotFoundError:
        print("❌ scraped_data.json not found!")
        print("💡 Run the scraper first to generate job data")
        return {}
    except Exception as e:
        print(f"❌ Error checking duplicate job IDs: {e}")
        return {}

def suggest_fixes(duplicates: Dict[str, List[Dict[str, Any]]]):
    """Suggest fixes for duplicate job ID issues"""
    
    if not duplicates:
        print("\n✅ No fixes needed - no duplicate job IDs found!")
        return
    
    print(f"\n🔧 Suggested Fixes:")
    print("=" * 40)
    
    print("1. **Fix Job ID Generation Logic**")
    print("   - Update the job ID generation in your scrapers")
    print("   - Ensure job IDs include company name and job board")
    print("   - Example: f'{company_name}_{job_board}_{job_id}'")
    
    print("\n2. **Clean and Re-scrape**")
    print("   - Delete scraped_data.json")
    print("   - Re-run the scraper with fixed ID logic")
    print("   - This will ensure all jobs have unique IDs")
    
    print("\n3. **Update Application System**")
    print("   - Consider using a composite key for job selection")
    print("   - Include company name in job selection logic")
    
    print("\n4. **Immediate Workaround**")
    print("   - For testing, manually verify the job URL before automation")
    print("   - Check that the opened page matches the expected company")

if __name__ == "__main__":
    duplicates = check_duplicate_job_ids()
    suggest_fixes(duplicates) 