#!/usr/bin/env python3
"""
Test Job URL Verification
Verify that job selection opens the correct company's job page
"""

import json
from application_system import application_system

def test_job_url_verification():
    """Test that job selection opens the correct URLs"""
    
    print("🔍 Testing Job URL Verification")
    print("=" * 50)
    
    # Load resume data
    try:
        with open('my_resume_data.json', 'r') as f:
            resume_data = json.load(f)
        application_system.resume_data = resume_data
        print(f"✅ Resume loaded: {len(resume_data.get('skills', []))} skills")
    except Exception as e:
        print(f"❌ Error loading resume: {e}")
        return
    
    # Load jobs
    jobs = application_system.load_jobs()
    if not jobs:
        print("❌ No jobs found")
        return
    
    print(f"📋 Found {len(jobs)} jobs")
    
    # Group jobs by company for testing
    company_jobs = {}
    for job in jobs:
        company = job.get('company_name', 'Unknown')
        if company not in company_jobs:
            company_jobs[company] = []
        company_jobs[company].append(job)
    
    # Test a few companies
    test_companies = ['asana', 'notion', 'stripe', 'airbnb']
    
    print(f"\n🎯 Testing job URL verification for specific companies:")
    print("=" * 60)
    
    for company in test_companies:
        if company in company_jobs:
            company_job_list = company_jobs[company]
            print(f"\n🏢 Testing {company.upper()}:")
            print(f"   📊 Found {len(company_job_list)} jobs")
            
            # Test first job from this company
            test_job = company_job_list[0]
            job_id = test_job.get('id')
            job_title = test_job.get('opening_title', 'Unknown')
            job_url = test_job.get('opening_link', 'No URL')
            
            print(f"   🎯 Testing job: {job_title}")
            print(f"   🆔 Job ID: {job_id}")
            print(f"   🔗 Job URL: {job_url}")
            
            # Verify URL contains the correct company
            if company.lower() in job_url.lower():
                print(f"   ✅ URL verification: PASSED - URL contains '{company}'")
            else:
                print(f"   ❌ URL verification: FAILED - URL does not contain '{company}'")
                print(f"      Expected: {company}")
                print(f"      Found: {job_url}")
            
            # Test job selection
            print(f"   🔄 Testing job selection...")
            success = application_system.select_jobs([job_id])
            
            if success and len(application_system.selected_jobs) > 0:
                selected_job = application_system.selected_jobs[0]
                selected_company = selected_job.get('company_name', 'Unknown')
                selected_url = selected_job.get('opening_link', 'No URL')
                
                print(f"   📋 Selected job company: {selected_company}")
                print(f"   🔗 Selected job URL: {selected_url}")
                
                if selected_company.lower() == company.lower():
                    print(f"   ✅ Job selection: PASSED - Correct company selected")
                else:
                    print(f"   ❌ Job selection: FAILED - Wrong company selected")
                    print(f"      Expected: {company}")
                    print(f"      Selected: {selected_company}")
                
                if company.lower() in selected_url.lower():
                    print(f"   ✅ URL selection: PASSED - Correct URL selected")
                else:
                    print(f"   ❌ URL selection: FAILED - Wrong URL selected")
                    print(f"      Expected URL to contain: {company}")
                    print(f"      Selected URL: {selected_url}")
            else:
                print(f"   ❌ Job selection failed")
            
            print()
        else:
            print(f"\n⚠️  No jobs found for company: {company}")
    
    print("\n🎯 Summary:")
    print("=" * 30)
    print("✅ If all tests pass, automation should work correctly")
    print("❌ If any tests fail, there may still be duplicate job IDs")
    print("💡 Run check_duplicate_job_ids.py to verify ID uniqueness")

if __name__ == "__main__":
    test_job_url_verification() 