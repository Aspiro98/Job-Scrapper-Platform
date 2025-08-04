#!/usr/bin/env python3
"""
Test Single Job Application
"""

from application_system import application_system
import json

def test_single_job():
    """Test application processing with a single job"""
    
    print("🧪 Testing Single Job Application")
    print("=" * 40)
    
    # Load resume data first
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
    
    # Select just one job for testing
    test_job = jobs[0]  # First job
    job_id = test_job.get('id')
    
    print(f"🎯 Testing with job: {test_job.get('opening_title', 'Unknown')} at {test_job.get('company_name', 'Unknown')}")
    print(f"🆔 Job ID: {job_id}")
    
    # Select this single job
    success = application_system.select_jobs([job_id])
    
    if not success:
        print("❌ Failed to select job")
        return
    
    print(f"✅ Selected {len(application_system.selected_jobs)} job(s)")
    
    # Process the application
    print(f"\n🔄 Processing application...")
    results = application_system.process_applications()
    
    print(f"\n📊 Results:")
    print(f"   Total jobs: {results['total_jobs']}")
    print(f"   Processed: {results['processed']}")
    print(f"   Errors: {len(results['errors'])}")
    
    if results['applications']:
        app = results['applications'][0]
        print(f"\n📝 Application Details:")
        print(f"   🏢 Company: {app.get('company', 'N/A')}")
        print(f"   📋 Position: {app.get('position', 'N/A')}")
        
        analysis = app.get('job_analysis', {})
        print(f"   🎯 Experience Level: {analysis.get('experience_level', 'N/A')}")
        print(f"   🔧 Technologies: {', '.join(analysis.get('technologies', []))}")
        
        resume = app.get('tailored_resume', {})
        print(f"   💼 Experience Emphasis: {resume.get('experience_emphasis', 'N/A')}")
        print(f"   🔧 Skills: {len(resume.get('skills', []))} skills")
        
        cover_letter = app.get('cover_letter', '')
        if cover_letter:
            preview = cover_letter[:100] + "..." if len(cover_letter) > 100 else cover_letter
            print(f"   📄 Cover Letter: {preview}")

if __name__ == "__main__":
    test_single_job() 