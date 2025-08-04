#!/usr/bin/env python3
"""
Test Improved Automation
Test the enhanced form automation with better field detection and manual interaction
"""

from application_system import application_system
import json

def test_improved_automation():
    """Test the improved automation system"""
    
    print("🤖 Testing Improved Form Automation")
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
    
    # Process applications with improved automation
    print(f"\n🚀 Processing applications with improved automation...")
    print("-" * 50)
    print(f"🔧 New features:")
    print(f"   - Better form field detection")
    print(f"   - Multiple filling methods (direct, click, JavaScript)")
    print(f"   - Fields made editable for manual interaction")
    print(f"   - Enhanced debugging and logging")
    print(f"   - Read-only/disabled field handling")
    
    try:
        # Process the application
        results = application_system.process_applications()
        
        if results['processed'] > 0:
            application = results['applications'][0]
            print(f"✅ Application prepared successfully!")
            print(f"   🏢 Company: {application.get('company', 'N/A')}")
            print(f"   📋 Position: {application.get('position', 'N/A')}")
            print(f"   📄 Cover Letter: {len(application.get('cover_letter', ''))} characters")
            print(f"   🔗 URL: {application.get('application_url', 'N/A')}")
            
            # Test improved form automation
            print(f"\n🤖 Testing improved form automation...")
            print("-" * 50)
            
            automation_result = application_system.automate_form_filling(
                test_job.get('id'), 
                application,
                keep_browser_open=True,
                delay_seconds=45  # Increased delay for testing
            )
            
            if automation_result["success"]:
                filled_fields = automation_result.get('filled_fields', [])
                total_visible_fields = automation_result.get('total_visible_fields', 0)
                field_debug = automation_result.get('field_detection_debug', [])
                
                print(f"✅ Form automation successful!")
                print(f"📝 Filled {len(filled_fields)} fields: {filled_fields}")
                print(f"📊 Total visible fields on page: {total_visible_fields}")
                
                if field_debug:
                    print(f"🔍 Field detection debug (first 5 fields):")
                    for i, field in enumerate(field_debug, 1):
                        print(f"   {i}. {field['tag']} - name: '{field['name']}', id: '{field['id']}'")
                
                if len(filled_fields) == 0:
                    print(f"⚠️  No fields were filled automatically")
                    print(f"💡 This is normal for some job sites with complex forms")
                    print(f"✅ You can still manually fill and submit the form")
                else:
                    print(f"✅ Fields were filled successfully")
                    print(f"🔧 All fields should now be editable for manual modification")
                
                print(f"\n📋 Manual Interaction Instructions:")
                print(f"   - All form fields should be editable")
                print(f"   - You can modify any filled values")
                print(f"   - You can fill any remaining empty fields")
                print(f"   - Submit the form when ready")
                print(f"   - Browser will close automatically after 45 seconds")
                
            else:
                print(f"⚠️ Form automation failed: {automation_result.get('error', 'Unknown error')}")
                print(f"💡 You can still manually fill the form")
        else:
            print(f"❌ Application preparation failed")
    
    except Exception as e:
        print(f"❌ Error during application processing: {e}")
    
    print(f"\n🎉 Improved automation testing completed!")
    print(f"💡 The automation now includes:")
    print(f"   - Better field detection with multiple selectors")
    print(f"   - Multiple filling methods for better compatibility")
    print(f"   - Fields made editable for manual interaction")
    print(f"   - Enhanced debugging and error handling")
    print(f"   - Read-only/disabled field removal")

if __name__ == "__main__":
    test_improved_automation() 