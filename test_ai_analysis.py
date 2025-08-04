#!/usr/bin/env python3
"""
Test AI-Powered Job Analysis
Demonstrates the new AI-powered job description analysis
"""

from application_system import application_system
import json

def test_ai_job_analysis():
    """Test AI-powered job analysis with a real job"""
    
    print("🤖 Testing AI-Powered Job Analysis")
    print("=" * 50)
    
    # Load resume data
    try:
        with open('my_resume_data.json', 'r') as f:
            resume_data = json.load(f)
        application_system.resume_data = resume_data
        print(f"✅ Resume loaded: {len(resume_data.get('skills', []))} skills")
    except Exception as e:
        print(f"❌ Error loading resume: {e}")
        return
    
    # Load jobs
    jobs = application_system.load_jobs()
    if not jobs:
        print("❌ No jobs found")
        return
    
    print(f"📋 Found {len(jobs)} jobs")
    
    # Find a job with a good URL for testing
    test_job = None
    for job in jobs:
        if job.get('opening_link') and 'greenhouse' in job.get('opening_link', ''):
            test_job = job
            break
    
    if not test_job:
        print("❌ No suitable test job found with URL")
        return
    
    print(f"🎯 Testing with job: {test_job.get('opening_title', 'Unknown')} at {test_job.get('company_name', 'Unknown')}")
    print(f"🔗 URL: {test_job.get('opening_link', 'N/A')}")
    
    # Test AI analysis
    print(f"\n🤖 Running AI-powered job analysis...")
    print("-" * 40)
    
    try:
        # Analyze job description
        analysis = application_system.analyze_job_description(test_job)
        
        print(f"\n📊 AI Analysis Results:")
        print(f"   🎯 Experience Level: {analysis.get('experience_level', 'N/A')}")
        print(f"   🔧 Technologies Found: {len(analysis.get('technologies', []))}")
        print(f"   📋 Required Skills: {len(analysis.get('skills', []))}")
        print(f"   🎯 Matching Skills: {len(analysis.get('matching_skills', []))}")
        print(f"   ❌ Missing Skills: {len(analysis.get('missing_skills', []))}")
        print(f"   📂 Job Category: {analysis.get('job_category', 'N/A')}")
        
        # Show technologies found
        technologies = analysis.get('technologies', [])
        if technologies:
            print(f"\n🔧 Technologies Found:")
            for tech in technologies[:10]:  # Show first 10
                print(f"   - {tech}")
            if len(technologies) > 10:
                print(f"   ... and {len(technologies) - 10} more")
        
        # Show matching skills
        matching_skills = analysis.get('matching_skills', [])
        if matching_skills:
            print(f"\n✅ Skills That Match:")
            for skill in matching_skills[:5]:  # Show first 5
                print(f"   - {skill}")
            if len(matching_skills) > 5:
                print(f"   ... and {len(matching_skills) - 5} more")
        
        # Show missing skills
        missing_skills = analysis.get('missing_skills', [])
        if missing_skills:
            print(f"\n❌ Skills You're Missing:")
            for skill in missing_skills[:5]:  # Show first 5
                print(f"   - {skill}")
            if len(missing_skills) > 5:
                print(f"   ... and {len(missing_skills) - 5} more")
        
        # Test resume tailoring
        print(f"\n📝 Testing AI-powered resume tailoring...")
        print("-" * 40)
        
        tailored_resume = application_system.tailor_resume_for_job(test_job, resume_data)
        
        ai_analysis = tailored_resume.get('ai_analysis', {})
        print(f"📊 Resume Tailoring Results:")
        print(f"   🎯 Skill Match Percentage: {ai_analysis.get('skill_match_percentage', 0):.1f}%")
        print(f"   🔧 Top Skills (AI-optimized): {tailored_resume.get('skills', [])[:5]}")
        print(f"   💼 Experience Emphasis: {tailored_resume.get('experience_emphasis', 'N/A')}")
        
        # Test cover letter generation
        print(f"\n📄 Testing enhanced cover letter generation...")
        print("-" * 40)
        
        cover_letter = application_system.generate_cover_letter(test_job, tailored_resume)
        
        print(f"📄 Cover Letter Preview:")
        print(cover_letter[:300] + "..." if len(cover_letter) > 300 else cover_letter)
        
        print(f"\n🎉 AI-powered analysis completed successfully!")
        print(f"💡 The system now:")
        print(f"   - Fetches real job descriptions from URLs")
        print(f"   - Uses AI to extract skills and requirements")
        print(f"   - Compares against your resume skills")
        print(f"   - Provides detailed matching analysis")
        print(f"   - Generates better tailored applications")
        
    except Exception as e:
        print(f"❌ Error during AI analysis: {e}")
        print(f"💡 This might be due to:")
        print(f"   - Network issues fetching job description")
        print(f"   - Job URL not accessible")
        print(f"   - No OpenAI API key (will use fallback)")

if __name__ == "__main__":
    test_ai_job_analysis() 