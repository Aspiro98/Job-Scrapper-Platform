#!/usr/bin/env python3
"""
Use My Resume
Load your existing PDF/Word resume into the application system
"""

import os
from resume_parser import load_resume_from_file
from application_system import application_system

def find_resume_files():
    """Find resume files in current directory"""
    resume_files = []
    for file in os.listdir('.'):
        if file.lower().endswith(('.pdf', '.docx', '.doc')):
            if 'resume' in file.lower() or 'cv' in file.lower():
                resume_files.append(file)
    
    return resume_files

def use_my_resume():
    """Interactive resume loading"""
    print("📄 Load Your Resume File")
    print("=" * 40)
    
    # Find resume files
    resume_files = find_resume_files()
    
    if resume_files:
        print("📁 Found resume files:")
        for i, file in enumerate(resume_files, 1):
            print(f"   {i}. {file}")
        print()
        
        # Let user choose
        try:
            choice = int(input("Select your resume file (number): ")) - 1
            if 0 <= choice < len(resume_files):
                selected_file = resume_files[choice]
            else:
                print("❌ Invalid choice")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
    else:
        print("📁 No resume files found in current directory.")
        print("Supported formats: .pdf, .docx, .doc")
        print()
        
        # Manual file path
        file_path = input("Enter the path to your resume file: ").strip()
        if not file_path:
            print("❌ No file path provided")
            return
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        selected_file = file_path
    
    print(f"\n🔄 Loading resume from: {selected_file}")
    
    try:
        # Parse resume
        resume_data = load_resume_from_file(selected_file)
        
        # Show extracted data
        print("\n📋 Extracted Resume Information:")
        print("-" * 40)
        print(f"👤 Name: {resume_data.get('name', 'Not found')}")
        print(f"📧 Email: {resume_data.get('email', 'Not found')}")
        print(f"📞 Phone: {resume_data.get('phone', 'Not found')}")
        print(f"🔗 LinkedIn: {resume_data.get('linkedin', 'Not found')}")
        print(f"🔧 Skills: {len(resume_data.get('skills', []))} skills found")
        print(f"💼 Experience: {resume_data.get('experience_years', 'Not found')} years")
        
        education = resume_data.get('education', {})
        if education:
            print(f"🎓 Education: {education.get('degree', 'Not found')} from {education.get('school', 'Not found')}")
        
        # Show skills
        skills = resume_data.get('skills', [])
        if skills:
            print(f"\n🔧 Technical Skills Found:")
            print(f"   {', '.join(skills[:10])}{'...' if len(skills) > 10 else ''}")
        
        # Ask for missing information
        print(f"\n❓ Missing Information:")
        if not resume_data.get('name'):
            resume_data['name'] = input("Full Name: ").strip()
        
        if not resume_data.get('location'):
            resume_data['location'] = input("Location (City, State): ").strip()
        
        if not resume_data.get('experience_years'):
            resume_data['experience_years'] = input("Years of experience: ").strip()
        
        # Save to application system
        application_system.resume_data = resume_data
        
        print(f"\n✅ Resume loaded successfully!")
        print(f"🎯 Your resume is now ready for job applications!")
        print(f"🚀 Start the Flask app with: python app.py")
        
        # Save to file for future use
        save_choice = input("\n💾 Save resume data to file for future use? (y/n): ").strip().lower()
        if save_choice in ['y', 'yes']:
            import json
            filename = 'my_resume_data.json'
            with open(filename, 'w') as f:
                json.dump(resume_data, f, indent=2)
            print(f"✅ Resume data saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error loading resume: {e}")
        print("\n💡 Make sure you have the required libraries installed:")
        print("   pip install PyPDF2 pdfplumber python-docx")

if __name__ == "__main__":
    use_my_resume() 