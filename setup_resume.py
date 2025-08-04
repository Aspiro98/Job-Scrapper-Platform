#!/usr/bin/env python3
"""
Setup Resume Data
Helps you add your resume information to the application system
"""

from application_system import application_system
import json

def setup_resume_data():
    """Interactive setup for resume data"""
    
    print("📝 Resume Setup for Job Application System")
    print("=" * 50)
    print("This will help you add your resume information so the system can")
    print("tailor your applications for each job.")
    print()
    
    resume_data = {}
    
    # Personal Information
    print("👤 Personal Information:")
    resume_data['name'] = input("Full Name: ").strip()
    resume_data['email'] = input("Email: ").strip()
    resume_data['phone'] = input("Phone: ").strip()
    resume_data['location'] = input("Location (City, State): ").strip()
    resume_data['linkedin'] = input("LinkedIn URL (optional): ").strip()
    print()
    
    # Skills
    print("🔧 Technical Skills:")
    print("Enter your technical skills (one per line, press Enter twice when done):")
    skills = []
    while True:
        skill = input("Skill: ").strip()
        if not skill:
            break
        skills.append(skill)
    resume_data['skills'] = skills
    print()
    
    # Experience
    print("💼 Work Experience:")
    experience_years = input("Years of experience: ").strip()
    resume_data['experience_years'] = experience_years
    
    print("Enter your work experience (one line summary):")
    experience_summary = input("Experience: ").strip()
    resume_data['experience_summary'] = experience_summary
    print()
    
    # Education
    print("🎓 Education:")
    degree = input("Degree: ").strip()
    school = input("School/University: ").strip()
    graduation_year = input("Graduation Year: ").strip()
    
    resume_data['education'] = {
        'degree': degree,
        'school': school,
        'graduation_year': graduation_year
    }
    print()
    
    # Additional Information
    print("📋 Additional Information:")
    resume_data['summary'] = input("Professional Summary (2-3 sentences): ").strip()
    
    # Languages
    languages = input("Languages (comma-separated): ").strip()
    resume_data['languages'] = [lang.strip() for lang in languages.split(',') if lang.strip()]
    
    # Certifications
    certs = input("Certifications (comma-separated, optional): ").strip()
    resume_data['certifications'] = [cert.strip() for cert in certs.split(',') if cert.strip()]
    print()
    
    # Save to application system
    application_system.resume_data = resume_data
    
    print("✅ Resume data saved to application system!")
    print()
    
    # Show summary
    print("📋 Resume Summary:")
    print(f"   👤 Name: {resume_data['name']}")
    print(f"   📧 Email: {resume_data['email']}")
    print(f"   📍 Location: {resume_data['location']}")
    print(f"   🔧 Skills: {', '.join(resume_data['skills'][:5])}...")
    print(f"   💼 Experience: {resume_data['experience_years']} years")
    print(f"   🎓 Education: {resume_data['education']['degree']} from {resume_data['education']['school']}")
    print()
    
    # Ask if user wants to save to file
    save_to_file = input("💾 Save resume data to file for future use? (y/n): ").strip().lower()
    if save_to_file in ['y', 'yes']:
        filename = 'my_resume_data.json'
        with open(filename, 'w') as f:
            json.dump(resume_data, f, indent=2)
        print(f"✅ Resume data saved to {filename}")
        print("   You can load this file later using: load_resume_from_file()")
    
    print()
    print("🎯 Your resume is now ready! The system will use this information to:")
    print("   - Tailor your skills for each job")
    print("   - Generate personalized cover letters")
    print("   - Fill application forms automatically")
    print()
    print("🚀 You can now start the Flask app and apply for jobs!")

def load_resume_from_file(filename='my_resume_data.json'):
    """Load resume data from a JSON file"""
    try:
        with open(filename, 'r') as f:
            resume_data = json.load(f)
        
        application_system.resume_data = resume_data
        print(f"✅ Resume data loaded from {filename}")
        print(f"   👤 Name: {resume_data.get('name', 'N/A')}")
        print(f"   🔧 Skills: {len(resume_data.get('skills', []))} skills loaded")
        
        return True
    except FileNotFoundError:
        print(f"❌ File {filename} not found. Run setup_resume_data() first.")
        return False
    except Exception as e:
        print(f"❌ Error loading resume data: {e}")
        return False

def show_current_resume():
    """Show current resume data in the system"""
    if not application_system.resume_data:
        print("❌ No resume data loaded. Run setup_resume_data() first.")
        return
    
    resume = application_system.resume_data
    print("📋 Current Resume Data:")
    print("=" * 40)
    print(f"👤 Name: {resume.get('name', 'N/A')}")
    print(f"📧 Email: {resume.get('email', 'N/A')}")
    print(f"📍 Location: {resume.get('location', 'N/A')}")
    print(f"🔧 Skills: {', '.join(resume.get('skills', []))}")
    print(f"💼 Experience: {resume.get('experience_years', 'N/A')} years")
    print(f"🎓 Education: {resume.get('education', {}).get('degree', 'N/A')} from {resume.get('education', {}).get('school', 'N/A')}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "load":
            load_resume_from_file()
        elif command == "show":
            show_current_resume()
        else:
            print("Usage: python setup_resume.py [load|show]")
    else:
        setup_resume_data() 