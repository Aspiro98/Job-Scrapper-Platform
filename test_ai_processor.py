#!/usr/bin/env python3
"""
Test script for the AI Filter Processor
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

from scrapers.utils.ai_filter_processor import AIFilterProcessor

def test_ai_processor():
    """Test the AI processor with sample job data"""
    
    # API key is now stored directly in the AI processor code
    print("🔑 Using API key stored in AI processor code")
    
    # Sample job data
    sample_jobs = [
        {
            'title': 'Senior Software Engineer',
            'location': 'San Francisco, CA',
            'company': 'Anthropic PBC',
            'description': 'We are looking for a senior software engineer with 5+ years of experience in Python and machine learning.'
        },
        {
            'title': 'Product Manager',
            'location': 'New York, NY',
            'company': 'Google LLC',
            'description': 'Lead product strategy and development for our AI products.'
        },
        {
            'title': 'Data Scientist',
            'location': 'Remote',
            'company': 'OpenAI',
            'description': 'Join our data science team to work on cutting-edge AI research.'
        },
        {
            'title': 'Junior Developer',
            'location': 'Seattle, WA | Austin, TX',
            'company': 'Microsoft Corporation',
            'description': 'Entry-level position for recent graduates interested in software development.'
        },
        {
            'title': 'UX Designer',
            'location': 'London, UK',
            'company': 'Meta Platforms Inc.',
            'description': 'Design user experiences for our social media platforms.'
        }
    ]
    
    print("Testing AI Filter Processor with sample job data:")
    print("=" * 60)
    
    try:
        # Initialize AI processor
        ai_processor = AIFilterProcessor()
        print("✅ AI Processor initialized successfully")
        
        # Process each job
        processed_jobs = []
        for i, job in enumerate(sample_jobs, 1):
            print(f"\n--- Processing Job {i} ---")
            print(f"Title: {job['title']}")
            print(f"Location: {job['location']}")
            print(f"Company: {job['company']}")
            
            processed_job = ai_processor.process_job(job)
            processed_jobs.append(processed_job)
            
            print(f"AI Results:")
            print(f"  Experience: {processed_job.get('experience_level', 'unknown')}")
            print(f"  Role: {processed_job.get('role_category', 'other')}")
            print(f"  Company Normalized: {processed_job.get('company_normalized', 'unknown')}")
            print(f"  Location Info: {processed_job.get('location_info', {})}")
            print(f"  AI Processed: {processed_job.get('ai_processed', False)}")
        
        # Test hierarchical filters
        print(f"\n" + "=" * 60)
        print("Testing hierarchical filter generation:")
        
        filters = ai_processor.get_hierarchical_filters(processed_jobs)
        
        print(f"Companies: {filters['companies']}")
        print(f"Experience Levels: {filters['experience_levels']}")
        print(f"Role Categories: {filters['role_categories']}")
        print(f"Location Filters:")
        for country, data in filters['location_filters'].items():
            print(f"  {country}:")
            print(f"    States: {data['states']}")
            print(f"    Cities: {data['cities']}")
        
        # Test location matching
        print(f"\n" + "=" * 60)
        print("Testing location matching:")
        
        test_cases = [
            ("united states", ""),
            ("united states", "california"),
            ("united states", "san francisco"),
            ("remote", ""),
            ("united kingdom", ""),
            ("united kingdom", "england")
        ]
        
        for country, state in test_cases:
            matches = 0
            for job in processed_jobs:
                if ai_processor.matches_location_filter(job.get('location_info', {}), country, state):
                    matches += 1
            print(f"Country: '{country}', State: '{state}' → {matches} matches")
        
        print(f"\n" + "=" * 60)
        print("✅ AI Filter Processor test completed successfully!")
        print("🎉 Your AI-powered filtering system is working!")
        
    except Exception as e:
        print(f"❌ Error testing AI processor: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if the API key in ai_filter_processor.py is valid")
        print("2. Verify your internet connection")
        print("3. Check Groq service status: https://status.groq.com/")
        print("4. Get a new API key from: https://console.groq.com/")

if __name__ == "__main__":
    test_ai_processor() 