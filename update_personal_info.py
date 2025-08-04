#!/usr/bin/env python3
"""
Update Personal Information for Form Automation
Update your personal details that will be used in job application forms
"""

import json
from form_automation import JobFormAutomation

def update_personal_info():
    """Update personal information in form automation"""
    
    print("🔧 Update Personal Information for Job Application Automation")
    print("=" * 60)
    
    # Create a new automation instance to access default_personal_info
    automation = JobFormAutomation()
    
    print("\n📋 Current Personal Information:")
    print(f"   First Name: {automation.default_personal_info['first_name']}")
    print(f"   Last Name: {automation.default_personal_info['last_name']}")
    print(f"   Full Name: {automation.default_personal_info['full_name']}")
    print(f"   Email: {automation.default_personal_info['email']}")
    print(f"   Phone: {automation.default_personal_info['phone']}")
    print(f"   LinkedIn: {automation.default_personal_info['linkedin']}")
    print(f"   City: {automation.default_personal_info['city']}")
    print(f"   State: {automation.default_personal_info['state']}")
    print(f"   Country: {automation.default_personal_info['country']}")
    print(f"   Zip Code: {automation.default_personal_info['zip_code']}")
    
    print("\n🎓 Education Information:")
    print(f"   School: {automation.default_personal_info['school']}")
    print(f"   Degree: {automation.default_personal_info['degree']}")
    print(f"   Discipline: {automation.default_personal_info['discipline']}")
    print(f"   Graduation Year: {automation.default_personal_info['graduation_year']}")
    print(f"   GPA (Undergraduate): {automation.default_personal_info['gpa_undergraduate']}")
    print(f"   GPA (Graduate): {automation.default_personal_info['gpa_graduate']}")
    print(f"   GPA (Doctorate): {automation.default_personal_info['gpa_doctorate']}")
    print(f"   SAT Score: {automation.default_personal_info['sat_score']}")
    print(f"   ACT Score: {automation.default_personal_info['act_score']}")
    print(f"   GRE Score: {automation.default_personal_info['gre_score']}")
    
    print("\n🔐 Work Authorization:")
    print(f"   Work Authorization: {automation.default_personal_info['work_authorization']}")
    print(f"   Citizenship Status: {automation.default_personal_info['citizenship_status']}")
    print(f"   Security Clearance: {automation.default_personal_info['security_clearance']}")
    print(f"   Can Perform Essential Functions: {automation.default_personal_info['can_perform_essential_functions']}")
    
    print("\n📢 How Did You Hear About This Job:")
    print(f"   Source: {automation.default_personal_info['how_heard']}")
    print(f"   Other Specification: {automation.default_personal_info['how_heard_other']}")
    
    print("\n💼 Professional Information:")
    print(f"   Years of Experience: {automation.default_personal_info['years_experience']}")
    print(f"   Current Company: {automation.default_personal_info['current_company']} (from resume)")
    print(f"   Current Title: {automation.default_personal_info['current_title']} (from resume)")
    print(f"   Skills: {automation.default_personal_info['skills']} (from resume)")
    
    print("\n💡 To update your personal information:")
    print("   1. Open form_automation.py")
    print("   2. Find the 'default_personal_info' dictionary")
    print("   3. Update the values with your actual information")
    print("   4. Save the file")
    
    print("\n📝 Example of what to update:")
    print("   'first_name': 'Your First Name',")
    print("   'last_name': 'Your Last Name',")
    print("   'full_name': 'Your Full Name',")
    print("   'email': 'your.email@example.com',")
    print("   'phone': '(123) 456-7890',")
    print("   'linkedin': 'https://linkedin.com/in/yourprofile',")
    print("   'city': 'Your City',")
    print("   'state': 'Your State',")
    print("   'country': 'Your Country'")
    
    print("\n✅ After updating, the automation will use your correct personal information")
    print("   instead of trying to parse it from the resume.")

if __name__ == "__main__":
    update_personal_info() 