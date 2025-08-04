#!/usr/bin/env python3
"""
Load Resume Data
Load resume data from saved file
"""

import json
from application_system import application_system

def load_resume():
    """Load resume data from saved file"""
    
    try:
        with open('my_resume_data.json', 'r') as f:
            resume_data = json.load(f)
        
        application_system.resume_data = resume_data
        
        print("✅ Resume data loaded successfully!")
        print(f"👤 Name: {resume_data.get('name', 'N/A')}")
        print(f"📧 Email: {resume_data.get('email', 'N/A')}")
        print(f"🔧 Skills: {len(resume_data.get('skills', []))} skills")
        
        skills = resume_data.get('skills', [])
        if skills:
            print(f"   Skills: {', '.join(skills[:5])}{'...' if len(skills) > 5 else ''}")
        
        return True
        
    except FileNotFoundError:
        print("❌ my_resume_data.json not found!")
        return False
    except Exception as e:
        print(f"❌ Error loading resume: {e}")
        return False

if __name__ == "__main__":
    load_resume() 