#!/usr/bin/env python3
"""
Test script to verify the web interface with posted date feature
"""

import requests
import json
import time

def test_web_interface():
    """Test the web interface with posted date feature"""
    print("🧪 Testing Web Interface with Posted Date Feature...")
    
    # Test the main API endpoint
    try:
        response = requests.get('http://localhost:5000/api/jobs', timeout=10)
        if response.status_code == 200:
            jobs = response.json()
            print(f"✅ API endpoint working - Found {len(jobs)} jobs")
            
            if jobs:
                # Check if posted date fields are present
                sample_job = jobs[0]
                posted_date_fields = [
                    'posted_date', 'posted_date_confidence', 
                    'posted_date_source', 'posted_date_display', 
                    'posted_date_color'
                ]
                
                missing_fields = [field for field in posted_date_fields if field not in sample_job]
                if missing_fields:
                    print(f"❌ Missing posted date fields: {missing_fields}")
                else:
                    print("✅ All posted date fields present")
                    print(f"   Sample job: {sample_job['title']}")
                    print(f"   Posted date: {sample_job['posted_date_display']}")
                    print(f"   Confidence: {sample_job['posted_date_confidence']}")
                    print(f"   Source: {sample_job['posted_date_source']}")
                    print(f"   Color: {sample_job['posted_date_color']}")
            else:
                print("⚠️ No jobs found in the system")
                
        else:
            print(f"❌ API endpoint returned status code: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the web server. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"❌ Error testing web interface: {e}")
    
    print("\n🎉 Web interface test completed!")
    print("💡 Open http://localhost:5000 in your browser to see the Posted Date column")

if __name__ == "__main__":
    test_web_interface() 