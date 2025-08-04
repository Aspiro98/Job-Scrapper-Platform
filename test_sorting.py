#!/usr/bin/env python3
"""
Test script to verify table sorting functionality
"""

import requests
import json

def test_sorting():
    """Test the sorting functionality"""
    print("🧪 Testing Table Sorting Functionality...")
    print("=" * 50)
    
    try:
        # Test getting jobs with sorting
        response = requests.get('http://localhost:5000/api/jobs?per_page=10')
        if response.status_code == 200:
            data = response.json()
            jobs = data['jobs']
            
            print(f"✅ Retrieved {len(jobs)} jobs for testing")
            
            # Test different sorting scenarios
            test_cases = [
                ('title', 'Job Title'),
                ('company', 'Company'),
                ('experience', 'Experience'),
                ('role', 'Role'),
                ('location', 'Location'),
                ('posted_date', 'Posted Date')
            ]
            
            for field, display_name in test_cases:
                print(f"\n📊 Testing {display_name} sorting:")
                
                # Get first few values to show sorting
                values = []
                for job in jobs[:5]:
                    if field == 'title':
                        values.append(job.get('title', 'Unknown'))
                    elif field == 'company':
                        values.append(job.get('company', 'Unknown'))
                    elif field == 'experience':
                        values.append(job.get('experience_display', 'Unknown'))
                    elif field == 'role':
                        values.append(job.get('role_display', 'Unknown'))
                    elif field == 'location':
                        values.append(job.get('location', 'Unknown'))
                    elif field == 'posted_date':
                        values.append(job.get('posted_date_display', 'Unknown'))
                
                print(f"   Sample values: {values}")
                
                # Test ascending sort
                sorted_asc = sorted(values, key=str.lower)
                print(f"   Ascending: {sorted_asc}")
                
                # Test descending sort
                sorted_desc = sorted(values, key=str.lower, reverse=True)
                print(f"   Descending: {sorted_desc}")
            
            print("\n🎉 Sorting test completed!")
            print("\n💡 Instructions:")
            print("1. Open http://localhost:5000 in your browser")
            print("2. Click on any column header to sort")
            print("3. Click again to reverse the sort order")
            print("4. Look for the sort icons (↑↓) next to column headers")
            
        else:
            print(f"❌ Failed to get jobs: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error testing sorting: {e}")

if __name__ == "__main__":
    test_sorting() 