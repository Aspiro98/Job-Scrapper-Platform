#!/usr/bin/env python3
"""
Test script to verify table layout and posted date display
"""

import json
import sys
import os
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample job data with posted dates for testing"""
    
    sample_jobs = [
        {
            "opening_title": "Customer Experience (CX) Automation Engineer",
            "location": "San Francisco, California",
            "opening_link": "https://example.com/job1",
            "source": "https://boards.greenhouse.io/embed/job_board?for=notion",
            "id": "30ietjt9xevrzzivez",
            "company_name": "notion",
            "description": "Sample job description",
            "posted_date": (datetime.now() - timedelta(days=3)).isoformat(),
            "posted_date_confidence": "medium",
            "posted_date_source": "LinkedIn",
            "posted_date_display": "3 days ago",
            "posted_date_color": "warning"
        },
        {
            "opening_title": "Enterprise Premium Support Agent, EMEA",
            "location": "Dublin, Ireland", 
            "opening_link": "https://example.com/job2",
            "source": "https://boards.greenhouse.io/embed/job_board?for=notion",
            "id": "8dizhjt6ey4pggb51p",
            "company_name": "notion",
            "description": "Sample job description",
            "posted_date": (datetime.now() - timedelta(days=7)).isoformat(),
            "posted_date_confidence": "low",
            "posted_date_source": "pattern_analysis",
            "posted_date_display": "1 week ago",
            "posted_date_color": "info"
        },
        {
            "opening_title": "Senior Software Engineer",
            "location": "Mountain View, CA",
            "opening_link": "https://example.com/job3",
            "source": "https://boards.greenhouse.io/embed/job_board?for=google",
            "id": "test123456",
            "company_name": "google",
            "description": "Sample job description",
            "posted_date": (datetime.now() - timedelta(days=1)).isoformat(),
            "posted_date_confidence": "high",
            "posted_date_source": "Indeed",
            "posted_date_display": "Yesterday",
            "posted_date_color": "success"
        }
    ]
    
    # Save sample data to a separate test file
    with open('test_scraped_data.json', 'w') as f:
        json.dump(sample_jobs, f, indent=2)
    
    print("⚠️  Note: Sample data saved to 'test_scraped_data.json' (not overwriting your real data)")
    
    print("✅ Sample data created with posted dates")
    print(f"📊 Created {len(sample_jobs)} sample jobs")
    
    for job in sample_jobs:
        print(f"   • {job['opening_title']} at {job['company_name']}")
        print(f"     Posted: {job['posted_date_display']} ({job['posted_date_source']})")

def test_table_layout():
    """Test the table layout by starting the web app"""
    print("\n🧪 Testing Table Layout...")
    print("1. Sample data has been created")
    print("2. Start the web app: python app.py")
    print("3. Open http://localhost:5000")
    print("4. Check that Posted Date column is properly displayed")
    print("5. Verify Action button doesn't overlap Posted Date")

if __name__ == "__main__":
    create_sample_data()
    test_table_layout() 