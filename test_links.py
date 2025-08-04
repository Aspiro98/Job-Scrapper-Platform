#!/usr/bin/env python3
"""
Test script to verify job links are working correctly
"""

import requests
import json

def test_job_links():
    """Test job links to see if they work correctly"""
    
    print("🔗 Testing Job Links")
    print("=" * 50)
    
    # Get some job data
    try:
        response = requests.get("http://localhost:5000/api/jobs?per_page=5")
        jobs = response.json()['jobs']
        
        print(f"Testing {len(jobs)} job links:")
        print()
        
        for i, job in enumerate(jobs, 1):
            print(f"{i}. {job['title']} at {job['company']}")
            print(f"   Link: {job['link']}")
            
            # Test if the link is accessible
            try:
                link_response = requests.head(job['link'], timeout=5, allow_redirects=True)
                if link_response.status_code == 200:
                    print(f"   ✅ Link works (Status: {link_response.status_code})")
                else:
                    print(f"   ⚠️  Link returns status: {link_response.status_code}")
            except Exception as e:
                print(f"   ❌ Link error: {e}")
            
            print()
        
        # Test different types of jobs
        print("Testing different job types:")
        
        # Test engineering job
        response = requests.get("http://localhost:5000/api/jobs?role=engineering&per_page=1")
        if response.status_code == 200:
            eng_job = response.json()['jobs'][0]
            print(f"Engineering job: {eng_job['title']}")
            print(f"Link: {eng_job['link']}")
        
        # Test senior job
        response = requests.get("http://localhost:5000/api/jobs?experience=senior&per_page=1")
        if response.status_code == 200:
            senior_job = response.json()['jobs'][0]
            print(f"Senior job: {senior_job['title']}")
            print(f"Link: {senior_job['link']}")
        
        print(f"\n" + "=" * 50)
        print("✅ Job Link Test Completed!")
        
    except Exception as e:
        print(f"❌ Error testing job links: {e}")

if __name__ == "__main__":
    test_job_links() 