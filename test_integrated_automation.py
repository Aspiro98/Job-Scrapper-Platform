#!/usr/bin/env python3
"""
Test Integrated Automation System
Verifies that automation is triggered automatically during application processing
"""

from application_system import application_system
import json

def test_integrated_automation():
    """Test that automation is triggered automatically during processing"""
    
    print("🤖 Testing Integrated Automation System")
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
    
    # Find a job with a good URL for testing
    test_job = None
    for job in jobs:
        if job.get('opening_link') and 'greenhouse' in job.get('opening_link', ''):
            test_job = job
            break
    
    if not test_job:
        print("❌ No suitable test job found with URL")
        return
    
    print(f"🎯 Testing with job: {test_job.get('opening_title', 'Unknown')} at {test_job.get('company_name', 'Unknown')}")
    print(f"🔗 URL: {test_job.get('opening_link', 'N/A')}")
    
    # Select the job
    print(f"\n🎯 Selecting job for processing...")
    application_system.select_jobs([test_job.get('id')])
    print(f"✅ Selected {len(application_system.selected_jobs)} job(s)")
    
    # Process applications (this should now trigger automation automatically)
    print(f"\n🚀 Processing applications with integrated automation...")
    print("-" * 50)
    
    try:
        results = application_system.process_applications()
        
        print(f"\n📊 Processing Results:")
        print(f"   ✅ Successfully processed: {results['processed']}/{results['total_jobs']}")
        print(f"   ❌ Errors: {len(results['errors'])}")
        print(f"   🤖 Automation attempts: {results.get('automation_attempts', 0)}")
        print(f"   ✅ Automation successful: {results.get('automation_success', 0)}")
        
        if results['applications']:
            application = results['applications'][0]
            print(f"\n📝 Application Details:")
            print(f"   🏢 Company: {application.get('company', 'N/A')}")
            print(f"   📋 Position: {application.get('position', 'N/A')}")
            print(f"   📄 Cover Letter: {len(application.get('cover_letter', ''))} characters")
            print(f"   🔗 URL: {application.get('application_url', 'N/A')}")
            
            # Check if automation was performed
            automation = application.get('automation')
            if automation:
                print(f"\n🤖 Automation Results:")
                if automation.get('success'):
                    filled_fields = automation.get('filled_fields', [])
                    print(f"   ✅ Automation successful!")
                    print(f"   📝 Filled {len(filled_fields)} fields:")
                    for field in filled_fields:
                        print(f"      - {field}")
                else:
                    print(f"   ❌ Automation failed: {automation.get('error', 'Unknown error')}")
            else:
                print(f"\n⚠️ No automation results found")
        
        if results['errors']:
            print(f"\n❌ Errors:")
            for error in results['errors']:
                print(f"   - {error}")
        
        print(f"\n🎉 Integrated automation test completed!")
        print(f"💡 The system now automatically:")
        print(f"   - Analyzes job descriptions with AI")
        print(f"   - Prepares tailored applications")
        print(f"   - Attempts form automation for each job")
        print(f"   - Provides detailed results and statistics")
        
    except Exception as e:
        print(f"❌ Error during processing: {e}")

if __name__ == "__main__":
    test_integrated_automation() 