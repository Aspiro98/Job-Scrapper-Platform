#!/usr/bin/env python3
"""
Check if resume data is loaded
"""

from application_system import application_system

def check_resume_data():
    """Check if resume data is loaded"""
    
    print("📋 Resume Data Check")
    print("=" * 40)
    
    if not application_system.resume_data:
        print("❌ No resume data loaded!")
        print("💡 Run: python use_my_resume.py")
        return False
    
    resume = application_system.resume_data
    print("✅ Resume data is loaded!")
    print()
    
    print("📋 Resume Information:")
    print(f"👤 Name: {resume.get('name', 'Not found')}")
    print(f"📧 Email: {resume.get('email', 'Not found')}")
    print(f"📞 Phone: {resume.get('phone', 'Not found')}")
    print(f"📍 Location: {resume.get('location', 'Not found')}")
    print(f"🔗 LinkedIn: {resume.get('linkedin', 'Not found')}")
    print(f"💼 Experience: {resume.get('experience_years', 'Not found')} years")
    
    skills = resume.get('skills', [])
    print(f"🔧 Skills: {len(skills)} skills loaded")
    if skills:
        print(f"   {', '.join(skills[:10])}{'...' if len(skills) > 10 else ''}")
    
    education = resume.get('education', {})
    if education:
        print(f"🎓 Education: {education.get('degree', 'Not found')} from {education.get('school', 'Not found')}")
    
    return True

if __name__ == "__main__":
    check_resume_data() 