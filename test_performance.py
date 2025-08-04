#!/usr/bin/env python3
"""
Performance test script to compare fast vs accurate date estimation modes
"""

import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.utils.job_date_estimator import JobDateEstimator

def test_performance():
    """Test performance difference between fast and accurate modes"""
    print("🚀 Performance Test: Fast vs Accurate Date Estimation")
    print("=" * 60)
    
    # Test data
    test_jobs = [
        {'title': 'Software Engineer', 'company': 'Google', 'location': 'Mountain View'},
        {'title': 'Data Scientist', 'company': 'Meta', 'location': 'San Francisco'},
        {'title': 'Product Manager', 'company': 'Apple', 'location': 'Cupertino'},
        {'title': 'Frontend Developer', 'company': 'Netflix', 'location': 'Los Gatos'},
        {'title': 'DevOps Engineer', 'company': 'Amazon', 'location': 'Seattle'},
        {'title': 'UX Designer', 'company': 'Microsoft', 'location': 'Redmond'},
        {'title': 'Backend Engineer', 'company': 'Uber', 'location': 'San Francisco'},
        {'title': 'Machine Learning Engineer', 'company': 'OpenAI', 'location': 'San Francisco'},
        {'title': 'Full Stack Developer', 'company': 'Airbnb', 'location': 'San Francisco'},
        {'title': 'Mobile Developer', 'company': 'Snapchat', 'location': 'Los Angeles'},
    ]
    
    # Test Fast Mode (Pattern Analysis Only)
    print("\n📊 Testing FAST MODE (Pattern Analysis Only)")
    print("-" * 40)
    
    fast_estimator = JobDateEstimator(use_external_apis=False)
    start_time = time.time()
    
    for i, job in enumerate(test_jobs, 1):
        result = fast_estimator.estimate_job_date(
            job['title'], 
            job['company'], 
            job['location']
        )
        print(f"  {i:2d}. {job['title']} at {job['company']}: {result['posted_date_display']} ({result['confidence']})")
    
    fast_time = time.time() - start_time
    print(f"\n⏱️  Fast Mode Time: {fast_time:.2f} seconds")
    print(f"📈 Average per job: {fast_time/len(test_jobs):.3f} seconds")
    
    # Test Accurate Mode (External APIs)
    print("\n📊 Testing ACCURATE MODE (External APIs)")
    print("-" * 40)
    print("⚠️  This will take much longer due to HTTP requests...")
    
    accurate_estimator = JobDateEstimator(use_external_apis=True)
    start_time = time.time()
    
    for i, job in enumerate(test_jobs, 1):
        result = accurate_estimator.estimate_job_date(
            job['title'], 
            job['company'], 
            job['location']
        )
        print(f"  {i:2d}. {job['title']} at {job['company']}: {result['posted_date_display']} ({result['confidence']})")
    
    accurate_time = time.time() - start_time
    print(f"\n⏱️  Accurate Mode Time: {accurate_time:.2f} seconds")
    print(f"📈 Average per job: {accurate_time/len(test_jobs):.3f} seconds")
    
    # Performance comparison
    print("\n📊 PERFORMANCE COMPARISON")
    print("=" * 40)
    speedup = accurate_time / fast_time if fast_time > 0 else float('inf')
    print(f"🚀 Fast Mode is {speedup:.1f}x faster than Accurate Mode")
    print(f"⚡ Fast Mode: {fast_time:.2f}s total, {fast_time/len(test_jobs):.3f}s per job")
    print(f"🎯 Accurate Mode: {accurate_time:.2f}s total, {accurate_time/len(test_jobs):.3f}s per job")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS")
    print("=" * 40)
    print("✅ Use FAST MODE for:")
    print("   • Quick browsing and filtering")
    print("   • Large job datasets")
    print("   • Real-time web interface")
    print("   • Initial job exploration")
    
    print("\n✅ Use ACCURATE MODE for:")
    print("   • Detailed job analysis")
    print("   • Small, focused job searches")
    print("   • When exact posting dates are critical")
    print("   • Research and reporting")
    
    print("\n🔄 Caching:")
    print("   • Results are cached automatically")
    print("   • Subsequent requests are instant")
    print("   • Clear cache to refresh estimates")

def test_caching():
    """Test caching performance"""
    print("\n🔄 Testing Caching Performance")
    print("=" * 40)
    
    estimator = JobDateEstimator(use_external_apis=False)
    
    # First request (no cache)
    start_time = time.time()
    result1 = estimator.estimate_job_date("Software Engineer", "Google", "Mountain View")
    first_time = time.time() - start_time
    
    # Second request (cached)
    start_time = time.time()
    result2 = estimator.estimate_job_date("Software Engineer", "Google", "Mountain View")
    cached_time = time.time() - start_time
    
    print(f"⏱️  First request: {first_time:.3f} seconds")
    print(f"⏱️  Cached request: {cached_time:.3f} seconds")
    print(f"🚀 Caching speedup: {first_time/cached_time:.1f}x faster")
    
    if result1['estimated_date'] == result2['estimated_date']:
        print("✅ Cache working correctly - same results")
    else:
        print("❌ Cache issue - different results")

if __name__ == "__main__":
    test_performance()
    test_caching() 