#!/usr/bin/env python3
"""
Test Automation with Browser Delay
Demonstrates the improved automation that keeps browser open for manual review
"""

from application_system import application_system
import json
import time

def test_automation_with_delay():
    """Test automation with browser delay for manual review"""
    
    print("🤖 Testing Automation with Browser Delay")
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
    
    # Process applications with automation
    print(f"\n🚀 Processing applications with automation and delay...")
    print("-" * 50)
    print(f"⏰ Browser will stay open for 30 seconds after filling the form")
    print(f"📝 You can review the filled form and submit manually")
    print(f"🔄 Press Ctrl+C to close browser early")
    
    try:
        results = application_system.process_applications()
        
        print(f"\n📊 Processing Results:")
        print(f"   ✅ Successfully processed: {results['processed']}/{results['total_jobs']}")
        print(f"   ❌ Errors: {len(results['errors'])}")
        print(f"   🤖 Automation attempts: {results.get('automation_attempts', 0)}")
        print(f"   ✅ Automation successful: {results.get('automation_success', 0)}")
        
        if results['applications']:
            application = results['applications'][0]
            automation = application.get('automation')
            
            if automation and automation.get('success'):
                print(f"\n🤖 Automation Results:")
                filled_fields = automation.get('filled_fields', [])
                print(f"   ✅ Automation successful!")
                print(f"   📝 Filled {len(filled_fields)} fields:")
                for field in filled_fields:
                    print(f"      - {field}")
                
                print(f"\n💡 Next Steps:")
                print(f"   📝 Review the filled form in the browser")
                print(f"   ✅ Submit the application manually")
                print(f"   🔄 Browser will close automatically after 30 seconds")
                print(f"   ⏹️  Press Ctrl+C to close browser early")
                
            else:
                print(f"\n⚠️ Automation failed or not attempted")
        
        print(f"\n🎉 Automation with delay test completed!")
        print(f"💡 The system now:")
        print(f"   - Fills out job application forms")
        print(f"   - Keeps browser open for manual review")
        print(f"   - Allows manual form submission")
        print(f"   - Provides time to verify filled data")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ User interrupted the process")
        print(f"🔄 Closing browser...")
        from form_automation import close_browser
        close_browser()
    except Exception as e:
        print(f"❌ Error during processing: {e}")

if __name__ == "__main__":
    test_automation_with_delay() 