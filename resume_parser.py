#!/usr/bin/env python3
"""
Resume Parser
Extracts information from PDF and Word resume files
"""

import os
import re
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ResumeParser:
    def __init__(self):
        self.supported_formats = ['.pdf', '.docx', '.doc']
        
    def parse_resume_file(self, file_path: str) -> Dict[str, Any]:
        """Parse resume from PDF or Word file"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Resume file not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {file_ext}. Supported: {self.supported_formats}")
        
        logger.info(f"📄 Parsing resume file: {file_path}")
        
        if file_ext == '.pdf':
            return self._parse_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            return self._parse_word(file_path)
    
    def _parse_pdf(self, file_path: str) -> Dict[str, Any]:
        """Parse PDF resume"""
        try:
            import PyPDF2
            import pdfplumber
            
            # Try pdfplumber first (better text extraction)
            try:
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            except ImportError:
                # Fallback to PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            
            return self._extract_resume_data(text)
            
        except ImportError:
            logger.error("❌ PDF parsing libraries not installed. Install with: pip install PyPDF2 pdfplumber")
            raise
    
    def _parse_word(self, file_path: str) -> Dict[str, Any]:
        """Parse Word document resume"""
        try:
            from docx import Document
            
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return self._extract_resume_data(text)
            
        except ImportError:
            logger.error("❌ Word parsing library not installed. Install with: pip install python-docx")
            raise
    
    def _extract_resume_data(self, text: str) -> Dict[str, Any]:
        """Extract resume information from text"""
        logger.info("🔍 Extracting resume information from text...")
        
        resume_data = {
            'name': '',
            'email': '',
            'phone': '',
            'location': '',
            'linkedin': '',
            'skills': [],
            'experience_years': '',
            'experience_summary': '',
            'education': {},
            'summary': '',
            'languages': [],
            'certifications': []
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            resume_data['email'] = emails[0]
            logger.info(f"📧 Found email: {emails[0]}")
        
        # Extract phone
        phone_patterns = [
            r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',
            r'\([0-9]{3}\)\s*[0-9]{3}-[0-9]{4}',
            r'[0-9]{3}-[0-9]{3}-[0-9]{4}'
        ]
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                resume_data['phone'] = phones[0]
                logger.info(f"📞 Found phone: {phones[0]}")
                break
        
        # Extract LinkedIn URL
        linkedin_pattern = r'https?://(?:www\.)?linkedin\.com/in/[a-zA-Z0-9-]+'
        linkedin_urls = re.findall(linkedin_pattern, text)
        if linkedin_urls:
            resume_data['linkedin'] = linkedin_urls[0]
            logger.info(f"🔗 Found LinkedIn: {linkedin_urls[0]}")
        
        # Extract skills (common technical skills)
        skills_patterns = [
            r'\b(python|javascript|java|c\+\+|c#|php|ruby|go|rust|swift|kotlin|scala|r|matlab|sql|html|css|react|angular|vue|node\.js|express|django|flask|spring|laravel|aws|azure|gcp|docker|kubernetes|git|jenkins|jira|agile|scrum|rest|api|mongodb|postgresql|mysql|redis|elasticsearch|kafka|spark|hadoop|machine learning|ai|data science|devops|ci/cd|terraform|ansible|linux|unix|windows|macos)\b',
            r'\b(frontend|backend|full-stack|mobile|web|desktop|cloud|database|testing|qa|ui/ux|design|product|project management|business analysis|data analysis|cybersecurity|networking|system administration)\b'
        ]
        
        all_skills = set()
        for pattern in skills_patterns:
            skills = re.findall(pattern, text.lower())
            all_skills.update(skills)
        
        resume_data['skills'] = list(all_skills)
        logger.info(f"🔧 Found {len(resume_data['skills'])} skills: {', '.join(resume_data['skills'][:5])}...")
        
        # Extract education
        education_patterns = [
            r'(bachelor|master|phd|b\.s\.|m\.s\.|b\.a\.|m\.a\.).*?(university|college|institute)',
            r'(university|college|institute).*?(bachelor|master|phd|b\.s\.|m\.s\.|b\.a\.|m\.a\.)'
        ]
        
        for pattern in education_patterns:
            education_matches = re.findall(pattern, text, re.IGNORECASE)
            if education_matches:
                degree, school = education_matches[0]
                resume_data['education'] = {
                    'degree': degree.strip(),
                    'school': school.strip(),
                    'graduation_year': ''  # Will need manual input
                }
                logger.info(f"🎓 Found education: {degree} from {school}")
                break
        
        # Extract experience years
        experience_patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)',
            r'(?:experience|exp)\s*:\s*(\d+)\s*(?:years?|yrs?)'
        ]
        
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                resume_data['experience_years'] = matches[0]
                logger.info(f"💼 Found experience: {matches[0]} years")
                break
        
        # Extract name (first line or near email)
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and not any(char in line for char in ['@', 'http', 'www', '•', '-', '_']):
                if len(line.split()) <= 4:  # Likely a name
                    resume_data['name'] = line
                    logger.info(f"👤 Found name: {line}")
                    break
        
        logger.info("✅ Resume parsing completed")
        return resume_data

def load_resume_from_file(file_path: str) -> Dict[str, Any]:
    """Load resume data from PDF/Word file"""
    parser = ResumeParser()
    return parser.parse_resume_file(file_path)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python resume_parser.py <resume_file_path>")
        print("Example: python resume_parser.py my_resume.pdf")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    try:
        resume_data = load_resume_from_file(file_path)
        
        print("📋 Extracted Resume Data:")
        print("=" * 40)
        print(f"👤 Name: {resume_data.get('name', 'Not found')}")
        print(f"📧 Email: {resume_data.get('email', 'Not found')}")
        print(f"📞 Phone: {resume_data.get('phone', 'Not found')}")
        print(f"🔗 LinkedIn: {resume_data.get('linkedin', 'Not found')}")
        print(f"🔧 Skills: {', '.join(resume_data.get('skills', []))}")
        print(f"💼 Experience: {resume_data.get('experience_years', 'Not found')} years")
        print(f"🎓 Education: {resume_data.get('education', {}).get('degree', 'Not found')} from {resume_data.get('education', {}).get('school', 'Not found')}")
        
        # Save to application system
        from application_system import application_system
        application_system.resume_data = resume_data
        print(f"\n✅ Resume data loaded into application system!")
        
    except Exception as e:
        print(f"❌ Error parsing resume: {e}")
        sys.exit(1) 