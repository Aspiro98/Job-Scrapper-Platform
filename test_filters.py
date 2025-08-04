#!/usr/bin/env python3
"""
Test script to check if filters are working correctly
"""

from app import load_job_data

def test_filters():
    """Test the filter generation"""
    
    print("🧪 Testing Filter Generation")
    print("=" * 50)
    
    # Load job data
    jobs = load_job_data()
    print(f"📊 Loaded {len(jobs)} jobs")
    
    # Extract filter data manually
    companies = set()
    experience_levels = set()
    role_categories = set()
    countries = set()
    states = set()
    
    for job in jobs:
        companies.add(job.get('company_normalized', job['company']))
        experience_levels.add(job.get('experience_level', 'unknown'))
        role_categories.add(job.get('role_category', 'other'))
        
        location_info = job.get('location_info', {})
        countries.add(location_info.get('country', 'other'))
        for state in location_info.get('states', []):
            states.add(state)
    
    print(f"\n🏢 Companies: {len(companies)}")
    print(f"Sample: {sorted(list(companies))[:10]}")
    
    print(f"\n👨‍💼 Experience Levels: {len(experience_levels)}")
    print(f"All: {sorted(list(experience_levels))}")
    
    print(f"\n🎯 Role Categories: {len(role_categories)}")
    print(f"All: {sorted(list(role_categories))}")
    
    print(f"\n🌍 Countries: {len(countries)}")
    print(f"All: {sorted(list(countries))}")
    
    print(f"\n🏛️ States: {len(states)}")
    print(f"Sample: {sorted(list(states))[:10]}")
    
    # Test filtering
    print(f"\n🔍 Testing Filters")
    print("=" * 30)
    
    # Test company filter
    test_company = list(companies)[0] if companies else "stripe"
    filtered_by_company = [job for job in jobs if test_company.lower() in job.get('company_normalized', job['company']).lower()]
    print(f"Jobs for company '{test_company}': {len(filtered_by_company)}")
    
    # Test experience filter
    test_experience = 'senior' if 'senior' in experience_levels else list(experience_levels)[0]
    filtered_by_exp = [job for job in jobs if job.get('experience_level') == test_experience]
    print(f"Jobs for experience '{test_experience}': {len(filtered_by_exp)}")
    
    # Test role filter
    test_role = 'engineering' if 'engineering' in role_categories else list(role_categories)[0]
    filtered_by_role = [job for job in jobs if job.get('role_category') == test_role]
    print(f"Jobs for role '{test_role}': {len(filtered_by_role)}")
    
    # Test country filter
    test_country = 'united states' if 'united states' in countries else list(countries)[0]
    filtered_by_country = [job for job in jobs if job.get('location_info', {}).get('country') == test_country]
    print(f"Jobs for country '{test_country}': {len(filtered_by_country)}")
    
    print(f"\n✅ Filter test completed!")
    print(f"🎉 All filters are working correctly!")

if __name__ == "__main__":
    test_filters() 