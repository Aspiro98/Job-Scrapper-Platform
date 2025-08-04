#!/usr/bin/env python3
"""
Complete Test System for Job Application Automation
Tests resume data, form filling, and application automation
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Any
from application_system import JobApplicationSystem

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class CompleteTestSystem:
    """Test system for complete job application automation"""
    
    def __init__(self):
        self.application_system = JobApplicationSystem()
        self.test_results = {}
        
    def setup_dummy_resume_data(self):
        """Set up comprehensive dummy resume data"""
        logger.info("📝 Setting up dummy resume data...")
        
        self.application_system.resume_data = {
            'personal_info': {
                'name': 'John Doe',
                'email': 'john.doe@email.com',
                'phone': '+1-555-123-4567',
                'location': 'San Francisco, CA',
                'linkedin': 'linkedin.com/in/johndoe',
                'github': 'github.com/johndoe',
                'website': 'johndoe.dev'
            },
            'skills': [
                'Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker', 
                'Kubernetes', 'PostgreSQL', 'MongoDB', 'Git', 'REST APIs',
                'GraphQL', 'TypeScript', 'Vue.js', 'Django', 'Flask'
            ],
            'experience': [
                {
                    'title': 'Senior Software Engineer',
                    'company': 'TechCorp Inc.',
                    'duration': '2021 - Present',
                    'description': 'Led development of microservices architecture, mentored junior developers, implemented CI/CD pipelines'
                },
                {
                    'title': 'Software Engineer',
                    'company': 'StartupXYZ',
                    'duration': '2019 - 2021',
                    'description': 'Built full-stack web applications using React and Node.js, deployed on AWS'
                }
            ],
            'education': [
                {
                    'degree': 'Bachelor of Science in Computer Science',
                    'school': 'University of California, Berkeley',
                    'year': '2019',
                    'gpa': '3.8/4.0'
                }
            ],
            'projects': [
                {
                    'name': 'E-commerce Platform',
                    'description': 'Full-stack e-commerce solution with React frontend and Node.js backend',
                    'technologies': ['React', 'Node.js', 'MongoDB', 'AWS']
                },
                {
                    'name': 'Task Management App',
                    'description': 'Real-time task management application with WebSocket support',
                    'technologies': ['Vue.js', 'Python', 'PostgreSQL', 'Socket.io']
                }
            ],
            'certifications': [
                'AWS Certified Solutions Architect',
                'Google Cloud Professional Developer',
                'Certified Kubernetes Administrator'
            ]
        }
        
        logger.info("✅ Dummy resume data set up successfully")
        logger.info(f"   📧 Email: {self.application_system.resume_data['personal_info']['email']}")
        logger.info(f"   🎯 Skills: {len(self.application_system.resume_data['skills'])} skills")
        logger.info(f"   💼 Experience: {len(self.application_system.resume_data['experience'])} positions")
        
    def create_dummy_jobs(self):
        """Create dummy jobs for testing"""
        logger.info("🏢 Creating dummy jobs for testing...")
        
        dummy_jobs = [
            {
                'id': 'test_senior_python',
                'opening_title': 'Senior Python Developer',
                'company_name': 'TechStartup Inc.',
                'description': 'We are looking for a Senior Python Developer with experience in Django, Flask, AWS, and PostgreSQL. Must have 5+ years of experience leading development teams.',
                'opening_link': 'https://techstartup.com/careers/senior-python-dev',
                'location': 'San Francisco, CA',
                'department': 'Engineering'
            },
            {
                'id': 'test_frontend_react',
                'opening_title': 'Frontend React Developer',
                'company_name': 'WebSolutions Corp.',
                'description': 'Join our team as a Frontend Developer specializing in React, JavaScript, TypeScript, and modern web technologies. Experience with REST APIs and GraphQL preferred.',
                'opening_link': 'https://websolutions.com/careers/frontend-react',
                'location': 'Remote',
                'department': 'Frontend'
            },
            {
                'id': 'test_fullstack_dev',
                'opening_title': 'Full Stack Developer',
                'company_name': 'Innovation Labs',
                'description': 'Full Stack Developer needed with expertise in Python, JavaScript, React, Node.js, AWS, and Docker. Experience with microservices architecture required.',
                'opening_link': 'https://innovationlabs.com/careers/fullstack',
                'location': 'New York, NY',
                'department': 'Engineering'
            }
        ]
        
        logger.info(f"✅ Created {len(dummy_jobs)} dummy jobs")
        for job in dummy_jobs:
            logger.info(f"   - {job['opening_title']} at {job['company_name']}")
            
        return dummy_jobs
    
    def test_job_analysis(self, jobs):
        """Test job analysis functionality"""
        logger.info("🔍 Testing job analysis...")
        
        for job in jobs:
            logger.info(f"")
            logger.info(f"📊 Analyzing: {job['opening_title']}")
            
            analysis = self.application_system.analyze_job_description(job)
            
            logger.info(f"   🎯 Experience Level: {analysis['experience_level']}")
            logger.info(f"   🔧 Technologies: {analysis['technologies']}")
            logger.info(f"   📋 Skills: {analysis['skills']}")
            
            # Validate analysis
            if 'python' in job['description'].lower() and 'python' not in analysis['technologies']:
                logger.error(f"   ❌ Failed to detect Python in job description")
            else:
                logger.info(f"   ✅ Technology detection working")
                
        logger.info("✅ Job analysis test completed")
    
    def test_resume_tailoring(self, jobs):
        """Test resume tailoring functionality"""
        logger.info("📝 Testing resume tailoring...")
        
        for job in jobs:
            logger.info(f"")
            logger.info(f"🔄 Tailoring resume for: {job['opening_title']}")
            
            tailored = self.application_system.tailor_resume_for_job(job, self.application_system.resume_data)
            
            logger.info(f"   📋 Original skills: {self.application_system.resume_data['skills'][:5]}...")
            logger.info(f"   🎯 Tailored skills: {tailored['skills'][:5]}...")
            logger.info(f"   💼 Experience emphasis: {tailored.get('experience_emphasis', 'N/A')}")
            
            # Validate tailoring
            if len(tailored['skills']) != len(self.application_system.resume_data['skills']):
                logger.error(f"   ❌ Skills count mismatch")
            else:
                logger.info(f"   ✅ Resume tailoring working")
                
        logger.info("✅ Resume tailoring test completed")
    
    def test_cover_letter_generation(self, jobs):
        """Test cover letter generation"""
        logger.info("📄 Testing cover letter generation...")
        
        for job in jobs:
            logger.info(f"")
            logger.info(f"📝 Generating cover letter for: {job['opening_title']}")
            
            tailored_resume = self.application_system.tailor_resume_for_job(job, self.application_system.resume_data)
            cover_letter = self.application_system.generate_cover_letter(job, tailored_resume)
            
            logger.info(f"   📏 Cover letter length: {len(cover_letter)} characters")
            logger.info(f"   🏢 Company mentioned: {'Yes' if job['company_name'].lower() in cover_letter.lower() else 'No'}")
            logger.info(f"   📋 Position mentioned: {'Yes' if job['opening_title'].lower() in cover_letter.lower() else 'No'}")
            
            # Show preview
            preview = cover_letter[:200] + "..." if len(cover_letter) > 200 else cover_letter
            logger.info(f"   📄 Preview: {preview}")
            
        logger.info("✅ Cover letter generation test completed")
    
    def test_form_automation_simulation(self, jobs):
        """Simulate form automation (without actually filling forms)"""
        logger.info("🤖 Testing form automation simulation...")
        
        for job in jobs:
            logger.info(f"")
            logger.info(f"🔄 Simulating form fill for: {job['opening_title']}")
            
            # Simulate form fields that would be filled
            form_fields = {
                'personal_info': {
                    'name': self.application_system.resume_data['personal_info']['name'],
                    'email': self.application_system.resume_data['personal_info']['email'],
                    'phone': self.application_system.resume_data['personal_info']['phone'],
                    'location': self.application_system.resume_data['personal_info']['location']
                },
                'experience': {
                    'current_title': self.application_system.resume_data['experience'][0]['title'],
                    'current_company': self.application_system.resume_data['experience'][0]['company'],
                    'years_experience': '5+ years'
                },
                'skills': self.application_system.resume_data['skills'][:10],  # Top 10 skills
                'education': {
                    'degree': self.application_system.resume_data['education'][0]['degree'],
                    'school': self.application_system.resume_data['education'][0]['school'],
                    'graduation_year': self.application_system.resume_data['education'][0]['year']
                }
            }
            
            logger.info(f"   📝 Would fill form fields:")
            logger.info(f"      - Name: {form_fields['personal_info']['name']}")
            logger.info(f"      - Email: {form_fields['personal_info']['email']}")
            logger.info(f"      - Current Role: {form_fields['experience']['current_title']}")
            logger.info(f"      - Skills: {', '.join(form_fields['skills'][:3])}...")
            
            # Simulate potential issues
            if 'python' in job['description'].lower() and 'python' not in form_fields['skills']:
                logger.warning(f"   ⚠️  Missing required skill: Python")
            else:
                logger.info(f"   ✅ Required skills covered")
                
        logger.info("✅ Form automation simulation completed")
    
    def test_complete_application_workflow(self, jobs):
        """Test complete application workflow"""
        logger.info("🚀 Testing complete application workflow...")
        
        # Select jobs
        job_ids = [job['id'] for job in jobs]
        self.application_system.selected_jobs = jobs
        
        logger.info(f"📋 Selected {len(jobs)} jobs for testing")
        
        # Process applications
        results = self.application_system.process_applications()
        
        logger.info(f"")
        logger.info(f"📊 Workflow Results:")
        logger.info(f"   ✅ Processed: {results['processed']}/{results['total_jobs']}")
        logger.info(f"   ❌ Errors: {len(results['errors'])}")
        logger.info(f"   📄 Applications prepared: {len(results['applications'])}")
        
        # Show sample application
        if results['applications']:
            app = results['applications'][0]
            logger.info(f"")
            logger.info(f"📝 Sample Application:")
            logger.info(f"   🏢 Company: {app['company']}")
            logger.info(f"   📋 Position: {app['position']}")
            logger.info(f"   🔧 Technologies: {app['job_analysis']['technologies']}")
            logger.info(f"   🎯 Experience Level: {app['job_analysis']['experience_level']}")
            logger.info(f"   🔗 Application URL: {app['application_url']}")
            
        logger.info("✅ Complete workflow test finished")
    
    def run_all_tests(self):
        """Run all tests"""
        logger.info("🧪 Starting Complete Test System")
        logger.info("=" * 60)
        
        try:
            # Setup
            self.setup_dummy_resume_data()
            dummy_jobs = self.create_dummy_jobs()
            
            # Run individual tests
            self.test_job_analysis(dummy_jobs)
            self.test_resume_tailoring(dummy_jobs)
            self.test_cover_letter_generation(dummy_jobs)
            self.test_form_automation_simulation(dummy_jobs)
            self.test_complete_application_workflow(dummy_jobs)
            
            logger.info("")
            logger.info("🎉 All tests completed successfully!")
            logger.info("=" * 60)
            
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            raise

if __name__ == "__main__":
    test_system = CompleteTestSystem()
    test_system.run_all_tests() 