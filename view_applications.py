#!/usr/bin/env python3
"""
View Stored Applications
Shows all processed job applications in a readable format
"""

import json
import requests
from datetime import datetime

def view_applications():
    """View all stored applications"""
    
    print("📋 Stored Job Applications")
    print("=" * 60)
    
    try:
        # Get applications from API
        response = requests.get('http://localhost:5000/api/applications')
        data = response.json()
        
        applications = data.get('applications', [])
        total = data.get('total', 0)
        
        print(f"📊 Total Applications Stored: {total}")
        print()
        
        if not applications:
            print("❌ No applications found. Try processing some jobs first!")
            return
        
        for i, app in enumerate(applications, 1):
            print(f"📝 Application #{i}")
            print(f"   🏢 Company: {app.get('company', 'N/A')}")
            print(f"   📋 Position: {app.get('position', 'N/A')}")
            print(f"   🆔 Job ID: {app.get('job_id', 'N/A')}")
            print(f"   🔗 URL: {app.get('application_url', 'N/A')}")
            print(f"   📅 Prepared: {app.get('prepared_at', 'N/A')}")
            print(f"   📊 Status: {app.get('status', 'N/A')}")
            
            # Job Analysis
            analysis = app.get('job_analysis', {})
            print(f"   🎯 Experience Level: {analysis.get('experience_level', 'N/A')}")
            print(f"   🔧 Technologies: {', '.join(analysis.get('technologies', []))}")
            
            # Tailored Resume
            resume = app.get('tailored_resume', {})
            print(f"   💼 Experience Emphasis: {resume.get('experience_emphasis', 'N/A')}")
            
            # Cover Letter Preview
            cover_letter = app.get('cover_letter', '')
            if cover_letter:
                preview = cover_letter[:100] + "..." if len(cover_letter) > 100 else cover_letter
                print(f"   📄 Cover Letter: {preview}")
            
            print("-" * 60)
        
        # Also show processing status
        print("\n🔄 Processing Status:")
        status_response = requests.get('http://localhost:5000/api/application-status')
        status_data = status_response.json()
        
        print(f"   📊 Selected Jobs: {status_data.get('selected_jobs_count', 0)}")
        print(f"   ⏳ Is Processing: {status_data.get('is_processing', False)}")
        
        processing_status = status_data.get('processing_status', {})
        print(f"   ✅ Completed: {len([s for s in processing_status.values() if s.get('status') == 'completed'])}")
        print(f"   ❌ Errors: {len([s for s in processing_status.values() if s.get('status') == 'error'])}")
        
        # Show all job IDs that were processed
        if processing_status:
            print(f"\n📋 All Processed Job IDs:")
            for job_id, status in processing_status.items():
                status_text = status.get('status', 'unknown')
                print(f"   - {job_id}: {status_text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

def view_application_details(job_id):
    """View detailed information for a specific application"""
    
    print(f"🔍 Detailed Application for Job ID: {job_id}")
    print("=" * 60)
    
    try:
        # Get processing status
        response = requests.get('http://localhost:5000/api/application-status')
        data = response.json()
        
        processing_status = data.get('processing_status', {})
        
        if job_id not in processing_status:
            print(f"❌ Job ID {job_id} not found in processing status")
            return
        
        job_status = processing_status[job_id]
        
        if job_status.get('status') == 'completed':
            app = job_status.get('application', {})
            
            print(f"🏢 Company: {app.get('company', 'N/A')}")
            print(f"📋 Position: {app.get('position', 'N/A')}")
            print(f"🔗 Application URL: {app.get('application_url', 'N/A')}")
            print(f"📅 Prepared: {app.get('prepared_at', 'N/A')}")
            
            # Job Analysis
            analysis = app.get('job_analysis', {})
            print(f"\n📊 Job Analysis:")
            print(f"   🎯 Experience Level: {analysis.get('experience_level', 'N/A')}")
            print(f"   🔧 Technologies: {', '.join(analysis.get('technologies', []))}")
            print(f"   📋 Skills: {', '.join(analysis.get('skills', []))}")
            print(f"   📝 Responsibilities: {', '.join(analysis.get('responsibilities', []))}")
            
            # Tailored Resume
            resume = app.get('tailored_resume', {})
            print(f"\n📝 Tailored Resume:")
            print(f"   💼 Experience Emphasis: {resume.get('experience_emphasis', 'N/A')}")
            if 'skills' in resume:
                print(f"   🎯 Skills: {', '.join(resume.get('skills', [])[:5])}...")
            
            # Cover Letter
            cover_letter = app.get('cover_letter', '')
            if cover_letter:
                print(f"\n📄 Cover Letter:")
                print(cover_letter)
        
        elif job_status.get('status') == 'error':
            print(f"❌ Error: {job_status.get('error', 'Unknown error')}")
        
        else:
            print(f"⏳ Status: {job_status.get('status', 'Unknown')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Flask app. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # View specific application
        job_id = sys.argv[1]
        view_application_details(job_id)
    else:
        # View all applications
        view_applications() 