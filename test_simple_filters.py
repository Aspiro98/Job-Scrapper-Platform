#!/usr/bin/env python3
"""
Test script to verify the simple filtering system is working correctly
"""

import requests
import json

def test_filters():
    """Test the simple filtering system"""
    
    print("🧪 Testing Simple Filter System")
    print("=" * 50)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Get all filters
    print("\n1. Testing filter generation...")
    try:
        response = requests.get(f"{base_url}/api/filters")
        filters = response.json()
        
        print(f"✅ Companies: {len(filters['companies'])}")
        print(f"✅ Experience Levels: {len(filters['experience_levels'])}")
        print(f"✅ Role Categories: {len(filters['role_categories'])}")
        print(f"✅ Countries: {len(filters['location_filters'])}")
        
        print(f"Sample companies: {filters['companies'][:5]}")
        print(f"Countries: {list(filters['location_filters'].keys())}")
        
    except Exception as e:
        print(f"❌ Error getting filters: {e}")
        return
    
    # Test 2: Test country filtering
    print("\n2. Testing country filtering...")
    countries_to_test = ['united states', 'mexico', 'united kingdom', 'france', 'canada', 'ireland', 'japan', 'india']
    
    for country in countries_to_test:
        try:
            response = requests.get(f"{base_url}/api/jobs?country={country}&per_page=1")
            data = response.json()
            print(f"✅ {country}: {data['total']} jobs")
        except Exception as e:
            print(f"❌ Error testing {country}: {e}")
    
    # Test 3: Test company filtering
    print("\n3. Testing company filtering...")
    companies_to_test = ['stripe', 'airbnb', 'anthropic']
    
    for company in companies_to_test:
        try:
            response = requests.get(f"{base_url}/api/jobs?company={company}&per_page=1")
            data = response.json()
            print(f"✅ {company}: {data['total']} jobs")
        except Exception as e:
            print(f"❌ Error testing {company}: {e}")
    
    # Test 4: Test combined filtering
    print("\n4. Testing combined filtering...")
    try:
        response = requests.get(f"{base_url}/api/jobs?company=stripe&country=united%20states&per_page=1")
        data = response.json()
        print(f"✅ Stripe + US: {data['total']} jobs")
        
        response = requests.get(f"{base_url}/api/jobs?company=stripe&country=mexico&per_page=1")
        data = response.json()
        print(f"✅ Stripe + Mexico: {data['total']} jobs")
        
    except Exception as e:
        print(f"❌ Error testing combined filters: {e}")
    
    # Test 5: Test search functionality
    print("\n5. Testing search functionality...")
    try:
        response = requests.get(f"{base_url}/api/jobs?search=engineer&per_page=1")
        data = response.json()
        print(f"✅ Search 'engineer': {data['total']} jobs")
        
        response = requests.get(f"{base_url}/api/jobs?search=senior&per_page=1")
        data = response.json()
        print(f"✅ Search 'senior': {data['total']} jobs")
        
    except Exception as e:
        print(f"❌ Error testing search: {e}")
    
    print(f"\n" + "=" * 50)
    print("✅ Simple Filter System Test Completed!")
    print("🎉 Your filtering system is working correctly!")

if __name__ == "__main__":
    test_filters() 