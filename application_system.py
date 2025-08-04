#!/usr/bin/env python3
"""
Job Application System - Prototype
Handles job selection, resume tailoring, and application processing
"""

import json
import time
import threading
import logging
from datetime import datetime
from typing import List, Dict, Any
import openai

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class JobApplicationSystem:
    def __init__(self):
        self.selected_jobs = []
        self.application_queue = []
        self.processing_status = {}
        self.resume_data = {}
        
        # TODO: Add your resume data here or use setup_resume.py
        # Example resume data structure:
        # self.resume_data = {
        #     'name': 'Your Name',
        #     'email': 'your.email@example.com',
        #     'phone': '+1-555-123-4567',
        #     'location': 'San Francisco, CA',
        #     'linkedin': 'https://linkedin.com/in/yourprofile',
        #     'skills': ['python', 'javascript', 'react', 'node.js', 'aws', 'docker', 'sql', 'git'],
        #     'experience_years': '5',
        #     'experience_summary': 'Software engineer with 5 years building web applications',
        #     'education': {
        #         'degree': 'Bachelor of Science in Computer Science',
        #         'school': 'University of California',
        #         'graduation_year': '2020'
        #     },
        #     'summary': 'Passionate software engineer with expertise in full-stack development',
        #     'languages': ['English', 'Spanish'],
        #     'certifications': ['AWS Certified Developer', 'Google Cloud Professional']
        # }
        
    def load_jobs(self) -> List[Dict[str, Any]]:
        """Load available jobs from scraped data"""
        try:
            logger.info("📂 Loading jobs from scraped_data.json...")
            with open('scraped_data.json', 'r') as f:
                data = json.load(f)
            jobs = [job for job in data if 'opening_title' in job]
            logger.info(f"✅ Loaded {len(jobs)} jobs successfully")
            return jobs
        except Exception as e:
            logger.error(f"❌ Error loading jobs: {e}")
            return []
    
    def select_jobs(self, job_ids: List[str]) -> bool:
        """Select jobs for application"""
        logger.info(f"🎯 Selecting {len(job_ids)} jobs for application...")
        logger.info(f"📋 Job IDs: {job_ids}")
        
        # Clear previous selections first
        self.selected_jobs = []
        self.processing_status = {}
        
        jobs = self.load_jobs()
        
        # Create a mapping of unique job identifiers to jobs
        # Use combination of job ID and company name to make it unique
        job_mapping = {}
        for job in jobs:
            job_id = job.get('id')
            company = job.get('company_name', '')
            unique_id = f"{job_id}_{company}"  # Make ID unique per company
            job_mapping[unique_id] = job
            # Also keep the original ID mapping for backward compatibility
            if job_id not in job_mapping:
                job_mapping[job_id] = job
        
        # Try to find jobs by unique ID first, then fallback to original ID
        selected_jobs = []
        seen_ids = set()
        
        for job_id in job_ids:
            # First try to find by unique ID (job_id_company format)
            if '_' in job_id:
                if job_id in job_mapping:
                    selected_jobs.append(job_mapping[job_id])
                    seen_ids.add(job_id)
            else:
                # Try to find by original ID
                if job_id in job_mapping:
                    selected_jobs.append(job_mapping[job_id])
                    seen_ids.add(job_id)
        
        self.selected_jobs = selected_jobs
        
        logger.info(f"✅ Selected {len(self.selected_jobs)} jobs:")
        for job in self.selected_jobs:
            logger.info(f"   - {job.get('opening_title', 'Unknown')} at {job.get('company_name', 'Unknown')}")
            logger.info(f"     ID: {job.get('id', 'Unknown')}")
            logger.info(f"     Link: {job.get('opening_link', 'Unknown')}")
        
        return len(self.selected_jobs) > 0
    
    def analyze_job_description(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze job description to extract key requirements using AI"""
        title = job.get('opening_title', '')
        job_url = job.get('opening_link', '')
        
        logger.info(f"🔍 Analyzing job: {title}")
        
        # Use AI-powered job description analysis
        try:
            from job_description_analyzer import analyze_job_with_ai
            from setup_groq import load_groq_api_key
            
            # Get resume skills for comparison
            resume_skills = self.resume_data.get('skills', [])
            
            # Load Groq API key
            groq_api_key = load_groq_api_key()
            
            logger.info(f"🤖 Using AI to analyze job description...")
            logger.info(f"🌐 Fetching job description from: {job_url}")
            
            # Analyze with AI (will fallback to keyword matching if no API key)
            analysis = analyze_job_with_ai(job, resume_skills, groq_api_key)
            
            # Convert to our format
            keywords = {
                'technologies': analysis.get('technologies', []),
                'experience_level': analysis.get('experience_level', 'mid'),
                'skills': analysis.get('required_skills', []),
                'responsibilities': analysis.get('responsibilities', []),
                'matching_skills': analysis.get('matching_skills', []),
                'missing_skills': analysis.get('missing_skills', []),
                'job_category': analysis.get('job_category', 'other')
            }
            
            logger.info(f"✅ AI analysis complete: {len(keywords['technologies'])} technologies found")
            logger.info(f"   🎯 Experience level: {keywords['experience_level']}")
            logger.info(f"   🔧 Matching skills: {len(keywords['matching_skills'])}")
            logger.info(f"   ❌ Missing skills: {len(keywords['missing_skills'])}")
            
            return keywords
            
        except Exception as e:
            logger.error(f"❌ AI analysis failed: {e}")
            logger.info(f"🔄 Falling back to basic analysis...")
            
            # Fallback to basic analysis
            keywords = {
                'technologies': [],
                'experience_level': '',
                'skills': [],
                'responsibilities': [],
                'matching_skills': [],
                'missing_skills': [],
                'job_category': 'other'
            }
            
            # Extract experience level from title
            if any(word in title.lower() for word in ['senior', 'lead', 'principal']):
                keywords['experience_level'] = 'senior'
            elif any(word in title.lower() for word in ['junior', 'entry', 'associate']):
                keywords['experience_level'] = 'entry'
            else:
                keywords['experience_level'] = 'mid'
            
            logger.info(f"📊 Basic analysis complete: {len(keywords['technologies'])} technologies found")
            return keywords
    
    def tailor_resume_for_job(self, job: Dict[str, Any], resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Tailor resume based on job requirements using AI analysis"""
        title = job.get('opening_title', '')
        logger.info(f"📝 Tailoring resume for: {title}")
        
        job_analysis = self.analyze_job_description(job)
        
        tailored_resume = resume_data.copy()
        original_skills = resume_data.get('skills', [])
        
        logger.info(f"🔄 Reordering skills based on AI analysis...")
        logger.info(f"   Original skills: {len(original_skills)} skills")
        
        # Use AI analysis results for better skill matching
        matching_skills = job_analysis.get('matching_skills', [])
        missing_skills = job_analysis.get('missing_skills', [])
        required_technologies = job_analysis.get('technologies', [])
        
        if matching_skills:
            # Use AI-identified matching skills first
            relevant_skills = matching_skills
            other_skills = [skill for skill in original_skills if skill not in matching_skills]
            
            tailored_resume['skills'] = relevant_skills + other_skills
            
            logger.info(f"   ✅ AI-matched skills (moved to top): {relevant_skills}")
            logger.info(f"   📋 Other skills: {len(other_skills)} skills")
        elif required_technologies:
            # Fallback to technology matching
            relevant_skills = [skill for skill in original_skills 
                             if skill.lower() in [tech.lower() for tech in required_technologies]]
            other_skills = [skill for skill in original_skills 
                           if skill.lower() not in [tech.lower() for tech in required_technologies]]
            
            tailored_resume['skills'] = relevant_skills + other_skills
            
            logger.info(f"   ✅ Technology-matched skills (moved to top): {relevant_skills}")
            logger.info(f"   📋 Other skills: {len(other_skills)} skills")
        else:
            logger.info(f"   ℹ️  No specific matches found, keeping original order")
        
        # Add AI analysis insights
        tailored_resume['ai_analysis'] = {
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'job_category': job_analysis.get('job_category', 'other'),
            'skill_match_percentage': len(matching_skills) / len(original_skills) * 100 if original_skills else 0
        }
        
        # Adjust experience descriptions based on AI analysis
        logger.info(f"🎯 Adjusting experience emphasis...")
        if job_analysis['experience_level'] == 'senior':
            tailored_resume['experience_emphasis'] = 'leadership'
            logger.info(f"   🏆 Emphasizing: Leadership and senior achievements")
        elif job_analysis['experience_level'] == 'entry':
            tailored_resume['experience_emphasis'] = 'growth'
            logger.info(f"   🌱 Emphasizing: Learning and growth")
        else:
            tailored_resume['experience_emphasis'] = 'balanced'
            logger.info(f"   ⚖️  Emphasizing: Balanced experience")
        
        logger.info(f"✅ AI-powered resume tailoring complete")
        logger.info(f"   📊 Skill match: {tailored_resume['ai_analysis']['skill_match_percentage']:.1f}%")
        return tailored_resume
    
    def generate_cover_letter(self, job: Dict[str, Any], tailored_resume: Dict[str, Any]) -> str:
        """Generate a tailored cover letter"""
        company = job.get('company_name', 'the company')
        title = job.get('opening_title', 'this position')
        
        logger.info(f"📄 Generating cover letter for: {title} at {company}")
        
        skills = tailored_resume.get('skills', [])
        experience_emphasis = tailored_resume.get('experience_emphasis', 'mid-level')
        
        logger.info(f"   📋 Using skills: {skills[:3]}...")
        logger.info(f"   🎯 Experience emphasis: {experience_emphasis}")
        
        cover_letter = f"""
Dear Hiring Manager,

I am writing to express my strong interest in the {title} position at {company}. 

With my background in {', '.join(skills[:3])}, I believe I would be a valuable addition to your team.

Key highlights of my experience:
- {len(skills)} relevant technical skills
- Experience level: {experience_emphasis}
- Strong problem-solving and collaboration abilities

I am particularly excited about this opportunity because it aligns perfectly with my career goals and technical expertise.

Thank you for considering my application. I look forward to discussing how I can contribute to {company}.

Best regards,
[Your Name]
        """
        
        logger.info(f"✅ Cover letter generated successfully")
        return cover_letter.strip()
    
    def prepare_application(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare complete application for a job"""
        job_id = job.get('id', 'unknown')
        title = job.get('opening_title', 'Unknown')
        company = job.get('company_name', 'Unknown')
        
        logger.info(f"🚀 Preparing application for: {title} at {company}")
        logger.info(f"   📍 Job ID: {job_id}")
        
        # Analyze job requirements
        logger.info(f"📊 Step 1: Analyzing job requirements...")
        job_analysis = self.analyze_job_description(job)
        
        # Tailor resume
        logger.info(f"📝 Step 2: Tailoring resume...")
        tailored_resume = self.tailor_resume_for_job(job, self.resume_data)
        
        # Generate cover letter
        logger.info(f"📄 Step 3: Generating cover letter...")
        cover_letter = self.generate_cover_letter(job, tailored_resume)
        
        application = {
            'job_id': job_id,
            'company': company,
            'position': title,
            'job_analysis': job_analysis,
            'tailored_resume': tailored_resume,
            'cover_letter': cover_letter,
            'application_url': job.get('opening_link', ''),
            'status': 'prepared',
            'prepared_at': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Application prepared successfully for {title}")
        logger.info(f"   🔗 Application URL: {job.get('opening_link', 'N/A')}")
        
        return application
    
    def process_applications(self) -> Dict[str, Any]:
        """Process all selected jobs in background"""
        logger.info(f"🚀 Starting application processing for {len(self.selected_jobs)} jobs")
        logger.info(f"⏰ Start time: {datetime.now().strftime('%H:%M:%S')}")
        
        results = {
            'total_jobs': len(self.selected_jobs),
            'processed': 0,
            'applications': [],
            'errors': [],
            'automation_attempts': 0,
            'automation_success': 0,
            'start_time': datetime.now().isoformat()
        }
        
        for i, job in enumerate(self.selected_jobs, 1):
            job_title = job.get('opening_title', 'Unknown')
            company = job.get('company_name', 'Unknown')
            
            logger.info(f"")
            logger.info(f"📋 Processing job {i}/{len(self.selected_jobs)}: {job_title} at {company}")
            logger.info(f"🔄 Progress: {i}/{len(self.selected_jobs)} ({(i/len(self.selected_jobs)*100):.1f}%)")
            
            try:
                application = self.prepare_application(job)
                results['applications'].append(application)
                results['processed'] += 1
                
                # Update status
                self.processing_status[job.get('id')] = {
                    'status': 'completed',
                    'application': application
                }
                
                logger.info(f"✅ Successfully processed: {job_title}")
                
                # Attempt automation if job URL is available
                job_url = job.get('opening_link')
                if job_url and application.get('cover_letter'):
                    logger.info(f"🤖 Attempting form automation for: {job_title}")
                    results['automation_attempts'] += 1
                    automation_result = self.automate_form_filling(job.get('id'), application)
                    
                    if automation_result["success"]:
                        logger.info(f"✅ Automation successful: {automation_result.get('filled_fields', [])}")
                        results['automation_success'] += 1
                        # Update application with automation results
                        application['automation'] = automation_result
                    else:
                        logger.warning(f"⚠️ Automation failed: {automation_result.get('error', 'Unknown error')}")
                        application['automation'] = automation_result
                else:
                    logger.info(f"ℹ️  Skipping automation (no URL or cover letter)")
                
                # Small delay to prevent overwhelming
                if i < len(self.selected_jobs):  # Don't delay after last job
                    logger.info(f"⏳ Waiting 1 second before next job...")
                    time.sleep(1)
                
            except Exception as e:
                error_msg = f"Error processing {job_title}: {str(e)}"
                logger.error(f"❌ {error_msg}")
                results['errors'].append(error_msg)
                self.processing_status[job.get('id')] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        results['end_time'] = datetime.now().isoformat()
        results['status'] = 'completed'
        
        logger.info(f"")
        logger.info(f"🎉 Application processing completed!")
        logger.info(f"⏰ End time: {datetime.now().strftime('%H:%M:%S')}")
        logger.info(f"📊 Final results:")
        logger.info(f"   ✅ Successfully processed: {results['processed']}/{results['total_jobs']}")
        logger.info(f"   ❌ Errors: {len(results['errors'])}")
        logger.info(f"   🤖 Automation attempts: {results['automation_attempts']}")
        logger.info(f"   ✅ Automation successful: {results['automation_success']}")
        
        if results['errors']:
            logger.error(f"📋 Error summary:")
            for error in results['errors']:
                logger.error(f"   - {error}")
        
        return results
    
    def get_processing_status(self) -> Dict[str, Any]:
        """Get current processing status"""
        return {
            'selected_jobs_count': len(self.selected_jobs),
            'processing_status': self.processing_status,
            'is_processing': len(self.processing_status) > 0
        }
    
    def automate_form_filling(self, job_id: str, application_result: Dict[str, Any], keep_browser_open: bool = True, delay_seconds: int = 30) -> Dict[str, Any]:
        """Automate form filling for a job application"""
        try:
            from form_automation import JobFormAutomation
            
            # Find job in selected jobs
            job = None
            for selected_job in self.selected_jobs:
                if selected_job.get('id') == job_id:
                    job = selected_job
                    break
            
            if not job:
                return {"success": False, "error": "Job not found"}
            
            job_url = job.get('opening_link')
            if not job_url:
                return {"success": False, "error": "No job URL available"}
            
            cover_letter = application_result.get('cover_letter', '')
            tailored_resume = application_result.get('tailored_resume', {})
            
            logger.info(f"🤖 Starting form automation for: {job.get('opening_title', 'Unknown')}")
            logger.info(f"🌐 Job URL: {job_url}")
            logger.info(f"⏰ Browser will stay open for {delay_seconds} seconds after filling")
            
            # Create automation instance with custom settings
            automation = JobFormAutomation(
                headless=False,
                keep_open=keep_browser_open,
                delay_after_fill=delay_seconds
            )
            
            # Attempt automation
            automation_result = automation.automate_job_application(
                job_url=job_url,
                resume_data=tailored_resume,
                cover_letter=cover_letter
            )
            
            if automation_result["success"]:
                logger.info(f"✅ Form automation successful!")
                logger.info(f"   📝 Filled fields: {automation_result.get('filled_fields', [])}")
                if keep_browser_open:
                    logger.info(f"   ⏰ Browser will close in {delay_seconds} seconds")
            else:
                logger.warning(f"⚠️ Form automation failed: {automation_result.get('error', 'Unknown error')}")
            
            return automation_result
            
        except Exception as e:
            logger.error(f"❌ Error in form automation: {e}")
            return {"success": False, "error": str(e)}
    
    def preview_form_fields(self, job_id: str) -> Dict[str, Any]:
        """Preview form fields for a job application"""
        try:
            from form_automation import form_automation
            
            # Find job in selected jobs
            job = None
            for selected_job in self.selected_jobs:
                if selected_job.get('id') == job_id:
                    job = selected_job
                    break
            
            if not job:
                return {"success": False, "error": "Job not found"}
            
            job_url = job.get('opening_link')
            if not job_url:
                return {"success": False, "error": "No job URL available"}
            
            logger.info(f"🔍 Previewing form fields for: {job.get('opening_title', 'Unknown')}")
            logger.info(f"🌐 Job URL: {job_url}")
            
            # Preview form fields
            preview_result = form_automation.preview_form_fields(job_url)
            
            if preview_result["success"]:
                logger.info(f"✅ Form preview successful!")
                logger.info(f"   📋 Found {len(preview_result.get('form_elements', []))} form elements")
            else:
                logger.warning(f"⚠️ Form preview failed: {preview_result.get('error', 'Unknown error')}")
            
            return preview_result
            
        except Exception as e:
            logger.error(f"❌ Error in form preview: {e}")
            return {"success": False, "error": str(e)}

# Global instance
application_system = JobApplicationSystem() 