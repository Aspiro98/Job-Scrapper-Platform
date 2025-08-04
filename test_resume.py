#!/usr/bin/env python3
"""
Test Resume Loading
"""

import json
from application_system import application_system

print("🔍 Testing Resume Loading")
print("=" * 30)

# Load resume data
try:
    with open('my_resume_data.json', 'r') as f:
        resume_data = json.load(f)
    
    print(f"📄 Resume file loaded: {len(resume_data)} fields")
    print(f"👤 Name: {resume_data.get('name', 'N/A')}")
    print(f"🔧 Skills: {len(resume_data.get('skills', []))} skills")
    
    # Set to application system
    application_system.resume_data = resume_data
    
    print(f"✅ Set to application_system.resume_data")
    
    # Check if it's there
    if application_system.resume_data:
        print(f"✅ application_system.resume_data exists")
        print(f"👤 Name in system: {application_system.resume_data.get('name', 'N/A')}")
        print(f"🔧 Skills in system: {len(application_system.resume_data.get('skills', []))} skills")
    else:
        print(f"❌ application_system.resume_data is empty")
    
except Exception as e:
    print(f"❌ Error: {e}") 