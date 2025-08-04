#!/usr/bin/env python3
"""
Test script for job date estimation functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.utils.job_date_estimator import JobDateEstimator
from datetime import datetime

def test_date_estimation():
    """Test the date estimation functionality"""
    print("🧪 Testing Job Date Estimation...")
    
    # Initialize the estimator
    estimator = JobDateEstimator()
    
    # Test cases
    test_jobs = [
        {
            'title': 'Senior Software Engineer',
            'company': 'Google',
            'location': 'Mountain View, CA'
        },
        {
            'title': 'Data Scientist',
            'company': 'Meta',
            'location': 'San Francisco, CA'
        },
        {
            'title': 'Product Manager',
            'company': 'Apple',
            'location': 'Cupertino, CA'
        },
        {
            'title': 'Frontend Developer',
            'company': 'Netflix',
            'location': 'Los Gatos, CA'
        }
    ]
    
    for i, job in enumerate(test_jobs, 1):
        print(f"\n📋 Test {i}: {job['title']} at {job['company']}")
        print(f"   Location: {job['location']}")
        
        try:
            result = estimator.estimate_job_date(
                job['title'], 
                job['company'], 
                job['location']
            )
            
            print(f"   ✅ Estimated Date: {result.get('estimated_date')}")
            print(f"   📊 Confidence: {result.get('confidence')}")
            print(f"   🔍 Source: {result.get('source')}")
            print(f"   📅 Display: {estimator.format_date_for_display(result.get('estimated_date'))}")
            print(f"   🎨 Color: {estimator.get_confidence_color(result.get('confidence'))}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🎉 Date estimation test completed!")

def test_date_formatting():
    """Test date formatting functionality"""
    print("\n🧪 Testing Date Formatting...")
    
    estimator = JobDateEstimator()
    from datetime import timedelta
    now = datetime.now()
    
    # Test different date scenarios
    test_dates = [
        now,  # Today
        now - timedelta(hours=1),  # 1 hour ago
        now - timedelta(days=1),  # Yesterday
        now - timedelta(days=3),  # 3 days ago
        now - timedelta(days=7),  # 1 week ago
        now - timedelta(days=14),  # 2 weeks ago
        now - timedelta(days=30),  # 1 month ago
        None,  # Unknown
    ]
    
    for date in test_dates:
        formatted = estimator.format_date_for_display(date)
        print(f"   {date} → {formatted}")

if __name__ == "__main__":
    test_date_estimation()
    test_date_formatting() 