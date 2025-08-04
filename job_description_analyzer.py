#!/usr/bin/env python3
"""
AI-Powered Job Description Analyzer
Fetches job descriptions and uses AI to extract skills and requirements
"""

import requests
import time
import re
from typing import Dict, Any, List, Optional
import logging
from bs4 import BeautifulSoup
import groq

logger = logging.getLogger(__name__)

class JobDescriptionAnalyzer:
    def __init__(self, groq_api_key: Optional[str] = None):
        self.groq_api_key = groq_api_key
        self.groq_client = None
        if groq_api_key:
            self.groq_client = groq.Groq(api_key=groq_api_key)
        
    def fetch_job_description(self, job_url: str) -> str:
        """Fetch job description from job URL"""
        try:
            logger.info(f"🌐 Fetching job description from: {job_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(job_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            logger.info(f"✅ Fetched {len(text)} characters of job description")
            return text
            
        except Exception as e:
            logger.error(f"❌ Error fetching job description: {e}")
            return ""
    
    def analyze_job_description_ai(self, job_title: str, job_description: str, resume_skills: List[str]) -> Dict[str, Any]:
        """Use Groq AI to analyze job description and extract requirements"""
        
        if not self.groq_client:
            logger.warning("⚠️ No Groq API key provided, using fallback analysis")
            return self.analyze_job_description_fallback(job_title, job_description, resume_skills)
        
        try:
            logger.info(f"🤖 Using Groq AI to analyze job description for: {job_title}")
            
            # Prepare the prompt
            prompt = f"""
Analyze this job description and extract key information:

Job Title: {job_title}

Job Description:
{job_description[:3000]}  # Limit to first 3000 chars to avoid token limits

Resume Skills Available: {', '.join(resume_skills)}

Please extract and return the following information in JSON format:
{{
    "technologies": ["list of technologies mentioned"],
    "required_skills": ["list of required skills"],
    "experience_level": "entry/mid/senior",
    "responsibilities": ["key responsibilities"],
    "requirements": ["key requirements"],
    "matching_skills": ["skills from resume that match job requirements"],
    "missing_skills": ["skills mentioned in job but not in resume"],
    "job_category": "engineering/data_science/product/design/sales/marketing/operations/other"
}}

Focus on technical skills, programming languages, frameworks, tools, and technologies.
"""
            
            response = self.groq_client.chat.completions.create(
                model="llama3-8b-8192",  # Using Llama 3 model via Groq
                messages=[
                    {"role": "system", "content": "You are a job analysis expert. Extract key information from job descriptions and match them with candidate skills."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            # Parse the response
            ai_response = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response
            try:
                import json
                # Find JSON in the response
                json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group())
                    logger.info(f"✅ Groq AI analysis completed: {len(result.get('technologies', []))} technologies found")
                    return result
                else:
                    logger.warning("⚠️ Could not parse Groq AI response as JSON, using fallback")
                    return self.analyze_job_description_fallback(job_title, job_description, resume_skills)
                    
            except json.JSONDecodeError:
                logger.warning("⚠️ Invalid JSON from Groq AI, using fallback")
                return self.analyze_job_description_fallback(job_title, job_description, resume_skills)
                
        except Exception as e:
            logger.error(f"❌ Groq AI analysis failed: {e}")
            return self.analyze_job_description_fallback(job_title, job_description, resume_skills)
    
    def analyze_job_description_fallback(self, job_title: str, job_description: str, resume_skills: List[str]) -> Dict[str, Any]:
        """Fallback analysis using keyword matching"""
        logger.info(f"🔍 Using fallback analysis for: {job_title}")
        
        # Common technology keywords
        tech_keywords = [
            'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala',
            'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'asp.net',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'gitlab',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch', 'kafka', 'spark', 'hadoop',
            'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'html', 'css', 'sass', 'less', 'webpack', 'babel', 'typescript', 'graphql', 'rest', 'api',
            'git', 'svn', 'agile', 'scrum', 'kanban', 'jira', 'confluence', 'slack', 'teams'
        ]
        
        # Extract technologies from description
        found_technologies = []
        description_lower = job_description.lower()
        
        for tech in tech_keywords:
            if tech.lower() in description_lower:
                found_technologies.append(tech)
        
        # Determine experience level from title
        title_lower = job_title.lower()
        if any(word in title_lower for word in ['senior', 'lead', 'principal', 'staff']):
            experience_level = 'senior'
        elif any(word in title_lower for word in ['junior', 'entry', 'associate', 'graduate']):
            experience_level = 'entry'
        else:
            experience_level = 'mid'
        
        # Find matching skills
        matching_skills = [skill for skill in resume_skills if skill.lower() in description_lower]
        missing_skills = [tech for tech in found_technologies if tech.lower() not in [skill.lower() for skill in resume_skills]]
        
        # Determine job category
        if any(word in title_lower for word in ['engineer', 'developer', 'programmer']):
            job_category = 'engineering'
        elif any(word in title_lower for word in ['data', 'ml', 'ai', 'analyst', 'scientist']):
            job_category = 'data_science'
        elif any(word in title_lower for word in ['product', 'program']):
            job_category = 'product'
        elif any(word in title_lower for word in ['design', 'ux', 'ui']):
            job_category = 'design'
        elif any(word in title_lower for word in ['sales', 'business development']):
            job_category = 'sales'
        elif any(word in title_lower for word in ['marketing', 'growth']):
            job_category = 'marketing'
        elif any(word in title_lower for word in ['operations', 'strategy']):
            job_category = 'operations'
        else:
            job_category = 'other'
        
        result = {
            'technologies': found_technologies,
            'required_skills': found_technologies,  # Simplified for fallback
            'experience_level': experience_level,
            'responsibilities': [],  # Would need more complex parsing
            'requirements': [],  # Would need more complex parsing
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'job_category': job_category
        }
        
        logger.info(f"✅ Fallback analysis completed: {len(found_technologies)} technologies found")
        return result

def analyze_job_with_ai(job_data: Dict[str, Any], resume_skills: List[str], groq_api_key: Optional[str] = None) -> Dict[str, Any]:
    """Analyze a job using Groq AI-powered description analysis"""
    
    analyzer = JobDescriptionAnalyzer(groq_api_key)
    
    job_url = job_data.get('opening_link', '')
    job_title = job_data.get('opening_title', '')
    
    if not job_url:
        logger.warning("⚠️ No job URL provided, using title-only analysis")
        return analyzer.analyze_job_description_fallback(job_title, "", resume_skills)
    
    # Fetch job description
    job_description = analyzer.fetch_job_description(job_url)
    
    if not job_description:
        logger.warning("⚠️ Could not fetch job description, using title-only analysis")
        return analyzer.analyze_job_description_fallback(job_title, "", resume_skills)
    
    # Analyze with AI
    analysis = analyzer.analyze_job_description_ai(job_title, job_description, resume_skills)
    
    return analysis

if __name__ == "__main__":
    # Test the analyzer
    test_job = {
        'opening_title': 'Senior Software Engineer',
        'opening_link': 'https://example.com/job'
    }
    
    test_skills = ['python', 'javascript', 'react', 'aws', 'docker']
    
    result = analyze_job_with_ai(test_job, test_skills)
    print("Test result:", result) 