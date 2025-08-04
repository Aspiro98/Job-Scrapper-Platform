#!/usr/bin/env python3
"""
Test script to demonstrate the application system
"""

from application_system import application_system
import json

def test_application_system():
    """Test the application system with sample data"""
    
    print("🧪 Testing Application System")
    print("=" * 50)
    
    # Set up sample resume data
    application_system.resume_data = {
        'skills': ['python', 'javascript', 'react', 'node.js', 'aws', 'docker', 'sql', 'git'],
        'experience': '5 years software development',
        'education': 'Computer Science degree'
    }
    
    # Load sample jobs
    jobs = application_system.load_jobs()
    if not jobs:
        print("❌ No jobs found")
        return
    
    # Select first 2 jobs for testing
    test_jobs = jobs[:2]
    job_ids = [job['id'] for job in test_jobs]
    
    print(f"📋 Testing with {len(test_jobs)} jobs:")
    for job in test_jobs:
        print(f"  - {job['opening_title']} at {job['company_name']}")
    
    print(f"\n🔄 Selecting jobs...")
    success = application_system.select_jobs(job_ids)
    
    if not success:
        print("❌ Failed to select jobs")
        return
    
    print(f"✅ Selected {len(application_system.selected_jobs)} jobs")
    
    # Process applications
    print(f"\n🔄 Processing applications...")
    results = application_system.process_applications()
    
    print(f"\n📊 Results:")
    print(f"  Total jobs: {results['total_jobs']}")
    print(f"  Processed: {results['processed']}")
    print(f"  Errors: {len(results['errors'])}")
    
    if results['applications']:
        print(f"\n📝 Sample Application:")
        app = results['applications'][0]
        print(f"  Company: {app['company']}")
        print(f"  Position: {app['position']}")
        print(f"  Technologies: {app['job_analysis']['technologies']}")
        print(f"  Experience Level: {app['job_analysis']['experience_level']}")
        print(f"  Tailored Skills: {app['tailored_resume']['skills'][:3]}...")
        print(f"  Cover Letter Preview: {app['cover_letter'][:100]}...")
    
    if results['errors']:
        print(f"\n❌ Errors:")
        for error in results['errors']:
            print(f"  - {error}")
    
    print(f"\n✅ Application system test completed!")

if __name__ == "__main__":
    test_application_system() 