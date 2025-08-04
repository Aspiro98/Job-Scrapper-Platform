#!/usr/bin/env python3
"""
Test Form Automation System
Demonstrates the new form automation capabilities
"""

from application_system import application_system
import json

def test_form_automation():
    """Test form automation with a real job"""
    
    print("🤖 Testing Form Automation System")
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
    
    # Test form field preview
    print(f"\n🔍 Testing form field preview...")
    print("-" * 40)
    
    try:
        preview_result = application_system.preview_form_fields(test_job.get('id'))
        
        if preview_result["success"]:
            form_elements = preview_result.get('form_elements', [])
            print(f"✅ Form preview successful!")
            print(f"📋 Found {len(form_elements)} form elements:")
            
            # Show first 10 form elements
            for i, element in enumerate(form_elements[:10], 1):
                print(f"   {i}. {element.get('type', 'unknown')} - {element.get('name', 'no-name')} (id: {element.get('id', 'no-id')})")
            
            if len(form_elements) > 10:
                print(f"   ... and {len(form_elements) - 10} more elements")
        else:
            print(f"❌ Form preview failed: {preview_result.get('error', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Error during form preview: {e}")
    
    # Test application preparation
    print(f"\n📝 Testing application preparation...")
    print("-" * 40)
    
    try:
        # Select the test job
        application_system.select_jobs([test_job.get('id')])
        
        # Process the application
        results = application_system.process_applications()
        
        if results['processed'] > 0:
            application = results['applications'][0]
            print(f"✅ Application prepared successfully!")
            print(f"   🏢 Company: {application.get('company', 'N/A')}")
            print(f"   📋 Position: {application.get('position', 'N/A')}")
            print(f"   📄 Cover Letter: {len(application.get('cover_letter', ''))} characters")
            print(f"   🔗 URL: {application.get('application_url', 'N/A')}")
            
            # Test form automation
            print(f"\n🤖 Testing form automation...")
            print("-" * 40)
            
            automation_result = application_system.automate_form_filling(
                test_job.get('id'), 
                application
            )
            
            if automation_result["success"]:
                filled_fields = automation_result.get('filled_fields', [])
                print(f"✅ Form automation successful!")
                print(f"📝 Filled {len(filled_fields)} fields:")
                for field in filled_fields:
                    print(f"   - {field}")
            else:
                print(f"⚠️ Form automation failed: {automation_result.get('error', 'Unknown error')}")
                print(f"💡 This is normal for many job sites that have anti-automation measures")
        else:
            print(f"❌ Application preparation failed")
    
    except Exception as e:
        print(f"❌ Error during application processing: {e}")
    
    print(f"\n🎉 Automation testing completed!")
    print(f"💡 The system now includes:")
    print(f"   - Form field detection and preview")
    print(f"   - Automatic form filling")
    print(f"   - Resume data mapping")
    print(f"   - Cover letter integration")
    print(f"   - Error handling and logging")

if __name__ == "__main__":
    test_form_automation() 