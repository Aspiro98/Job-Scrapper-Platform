#!/usr/bin/env python3
"""
Check Stored Applications
Shows the current state of applications stored in memory
"""

from application_system import application_system
import json

def check_stored_applications():
    """Check what applications are currently stored in memory"""
    
    print("📋 Current Application System State")
    print("=" * 60)
    
    # Check selected jobs
    print(f"🎯 Selected Jobs: {len(application_system.selected_jobs)}")
    if application_system.selected_jobs:
        print("   Selected job titles:")
        for i, job in enumerate(application_system.selected_jobs, 1):
            print(f"   {i}. {job.get('opening_title', 'Unknown')} at {job.get('company_name', 'Unknown')}")
    print()
    
    # Check processing status
    processing_status = application_system.processing_status
    print(f"🔄 Processing Status: {len(processing_status)} jobs processed")
    
    if processing_status:
        print("   Processing details:")
        completed = 0
        errors = 0
        
        for job_id, status in processing_status.items():
            status_text = status.get('status', 'unknown')
            if status_text == 'completed':
                completed += 1
                app = status.get('application', {})
                print(f"   ✅ {job_id}: {app.get('position', 'Unknown')} at {app.get('company', 'Unknown')}")
            elif status_text == 'error':
                errors += 1
                error_msg = status.get('error', 'Unknown error')
                print(f"   ❌ {job_id}: {error_msg}")
            else:
                print(f"   ⏳ {job_id}: {status_text}")
        
        print(f"\n📊 Summary:")
        print(f"   ✅ Completed: {completed}")
        print(f"   ❌ Errors: {errors}")
        print(f"   📋 Total: {len(processing_status)}")
        
        # Show detailed application info
        if completed > 0:
            print(f"\n📝 Completed Applications:")
            for job_id, status in processing_status.items():
                if status.get('status') == 'completed':
                    app = status.get('application', {})
                    print(f"\n   🏢 {app.get('company', 'Unknown')}")
                    print(f"   📋 {app.get('position', 'Unknown')}")
                    print(f"   🆔 Job ID: {app.get('job_id', 'Unknown')}")
                    print(f"   🔗 URL: {app.get('application_url', 'N/A')}")
                    print(f"   📅 Prepared: {app.get('prepared_at', 'N/A')}")
                    
                    # Job Analysis
                    analysis = app.get('job_analysis', {})
                    print(f"   🎯 Experience: {analysis.get('experience_level', 'N/A')}")
                    print(f"   🔧 Technologies: {', '.join(analysis.get('technologies', []))}")
                    
                    # Cover Letter Preview
                    cover_letter = app.get('cover_letter', '')
                    if cover_letter:
                        preview = cover_letter[:100] + "..." if len(cover_letter) > 100 else cover_letter
                        print(f"   📄 Cover Letter: {preview}")
                    
                    print("   " + "-" * 40)
    else:
        print("   No jobs have been processed yet.")
    
    print()
    print("💡 Note: Applications are stored in memory during the Flask app session.")
    print("   They will be lost when the Flask app restarts.")
    print("   To persist them, we need to save them to a file or database.")

def save_applications_to_file():
    """Save current applications to a JSON file"""
    
    processing_status = application_system.processing_status
    completed_applications = []
    
    for job_id, status in processing_status.items():
        if status.get('status') == 'completed':
            completed_applications.append(status.get('application'))
    
    if completed_applications:
        filename = f"stored_applications_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(completed_applications, f, indent=2)
        
        print(f"💾 Saved {len(completed_applications)} applications to {filename}")
        return filename
    else:
        print("❌ No completed applications to save")
        return None

if __name__ == "__main__":
    from datetime import datetime
    
    check_stored_applications()
    
    # Ask if user wants to save applications
    print("\n💾 Would you like to save the applications to a file? (y/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['y', 'yes']:
            save_applications_to_file()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!") 