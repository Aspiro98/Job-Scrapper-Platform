#!/usr/bin/env python3
"""
Test script to verify posted date processing
"""

import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_posted_dates():
    """Test posted date processing with sample jobs"""
    
    # Load a few sample jobs from the data
    try:
        with open('scraped_data.json', 'r') as f:
            data = json.load(f)
        
        # Take first 5 jobs
        sample_jobs = data[:5]
        
        print("🧪 Testing Posted Date Processing...")
        print("=" * 50)
        
        for i, job in enumerate(sample_jobs, 1):
            if 'opening_title' in job:
                title = job.get('opening_title', 'Unknown')
                company = job.get('company_name', 'Unknown')
                location = job.get('location', 'Unknown')
                
                print(f"\n📋 Job {i}: {title}")
                print(f"   Company: {company}")
                print(f"   Location: {location}")
                
                # Check if posted date fields exist
                posted_fields = ['posted_date', 'posted_date_confidence', 'posted_date_source', 'posted_date_display']
                missing_fields = [field for field in posted_fields if field not in job]
                
                if missing_fields:
                    print(f"   ❌ Missing posted date fields: {missing_fields}")
                else:
                    print(f"   ✅ Posted: {job.get('posted_date_display', 'Unknown')}")
                    print(f"   📊 Confidence: {job.get('posted_date_confidence', 'Unknown')}")
                    print(f"   🔍 Source: {job.get('posted_date_source', 'Unknown')}")
        
        print(f"\n📊 Total jobs in data: {len(data)}")
        
    except Exception as e:
        print(f"❌ Error testing posted dates: {e}")

if __name__ == "__main__":
    test_posted_dates() 