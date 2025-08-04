#!/usr/bin/env python3
"""
Job Application Form Automation
Automatically fills out job application forms using analyzed data
"""

import time
import logging
from typing import Dict, Any, List, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re

logger = logging.getLogger(__name__)

class JobFormAutomation:
    def __init__(self, headless: bool = False, keep_open: bool = True, delay_after_fill: int = 30):
        """Initialize the form automation system"""
        self.headless = headless
        self.keep_open = keep_open
        self.delay_after_fill = delay_after_fill
        self.driver = None
        self.wait = None
        
        # Common form field mappings - prioritize exact matches
        self.field_mappings = {
            # Personal Information - HIGH PRIORITY
            'first_name': [
                'first_name', 'firstname', 'fname', 'given_name', 'first-name',
                'firstName', 'first_name', 'firstname', 'fname'
            ],
            'last_name': [
                'last_name', 'lastname', 'lname', 'family_name', 'last-name',
                'lastName', 'last_name', 'lastname', 'lname'
            ],
            'full_name': [
                'full_name', 'name', 'fullname', 'full-name',
                'fullName', 'full_name', 'fullname'
            ],
            'email': [
                'email', 'e-mail', 'email_address', 'email-address',
                'Email', 'email', 'e-mail', 'email_address'
            ],
            'phone': [
                'phone', 'telephone', 'phone_number', 'mobile', 'cell',
                'Phone', 'phone', 'telephone', 'phone_number'
            ],
            'linkedin': [
                'linkedin', 'linkedin_url', 'linkedin-url', 'linkedin_profile',
                'LinkedIn', 'linkedin', 'linkedin_url'
            ],
            
            # Address - MEDIUM PRIORITY
            'city': ['city', 'town', 'City', 'location'],
            'state': ['state', 'province', 'region', 'State'],
            'country': ['country', 'nation', 'Country'],
            'zip_code': ['zip', 'zip_code', 'postal_code', 'postcode', 'Zip'],
            'address': ['address', 'street_address', 'Address'],
            
            # Education - HIGH PRIORITY
            'school': [
                'school', 'university', 'college', 'institution', 'School',
                'university_name', 'college_name', 'institution_name'
            ],
            'degree': [
                'degree', 'degree_type', 'degree_type', 'Degree',
                'degree_name', 'degree_type'
            ],
            'discipline': [
                'discipline', 'major', 'field_of_study', 'Discipline',
                'major_field', 'study_field', 'academic_field'
            ],
            'graduation_year': [
                'graduation_year', 'grad_year', 'year_graduated', 'Graduation Year',
                'graduation_date', 'completion_year'
            ],
            'gpa_undergraduate': [
                'gpa_undergraduate', 'undergraduate_gpa', 'gpa', 'GPA (Undergraduate)',
                'undergrad_gpa', 'bachelor_gpa'
            ],
            'gpa_graduate': [
                'gpa_graduate', 'graduate_gpa', 'GPA (Graduate)',
                'masters_gpa', 'graduate_school_gpa'
            ],
            'gpa_doctorate': [
                'gpa_doctorate', 'doctorate_gpa', 'GPA (Doctorate)',
                'phd_gpa', 'doctoral_gpa'
            ],
            'sat_score': [
                'sat_score', 'sat', 'SAT Score', 'sat_test_score',
                'sat_exam_score', 'sat_results'
            ],
            'act_score': [
                'act_score', 'act', 'ACT Score', 'act_test_score',
                'act_exam_score', 'act_results'
            ],
            'gre_score': [
                'gre_score', 'gre', 'GRE Score', 'gre_test_score',
                'gre_exam_score', 'gre_results'
            ],
            
            # Work Authorization & Citizenship - HIGH PRIORITY
            'work_authorization': [
                'work_authorization', 'authorized_to_work', 'work_eligibility',
                'Are you legally authorized to work in the United States?',
                'work_permit', 'employment_authorization'
            ],
            'citizenship_status': [
                'citizenship_status', 'citizenship', 'Citizenship Status',
                'nationality', 'citizen_status'
            ],
            'security_clearance': [
                'security_clearance', 'clearance', 'Active Security Clearance(s)',
                'security_clearances', 'government_clearance'
            ],
            'can_perform_essential_functions': [
                'can_perform_essential_functions', 'essential_functions',
                'Can you perform all of the essential functions of this role with or without reasonable accommodations?',
                'accommodations', 'disability_accommodations'
            ],
            
            # How did you hear about this job - MEDIUM PRIORITY
            'how_heard': [
                'how_heard', 'how_did_you_hear', 'source', 'How did you hear about this job?',
                'referral_source', 'application_source'
            ],
            'how_heard_other': [
                'how_heard_other', 'other_source', 'Please specify',
                'If event or other, please specify below.', 'specify_source'
            ],
            
            # Professional - MEDIUM PRIORITY
            'current_company': ['current_company', 'employer', 'company', 'current_employer'],
            'current_title': ['current_title', 'job_title', 'position', 'current_position'],
            'years_experience': ['experience', 'years_experience', 'experience_years'],
            
            # Skills - LOW PRIORITY
            'skills': ['skills', 'technical_skills', 'competencies', 'expertise'],
            
            # Cover Letter - HIGH PRIORITY
            'cover_letter': [
                'cover_letter', 'coverletter', 'why_join', 'motivation', 'message',
                'Cover Letter', 'cover_letter', 'coverletter'
            ],
            
            # Resume Upload - HIGH PRIORITY
            'resume_upload': [
                'resume', 'cv', 'resume_file', 'cv_file', 'attachment',
                'Resume', 'resume', 'cv', 'resume_file'
            ]
        }
        
        # Default personal information (should be manually set)
        self.default_personal_info = {
            'first_name': 'Vijaya Sankara Naga Sai Akarsh',  # Set your actual first name
            'last_name': 'Jana',     # Set your actual last name
            'full_name': 'Vijaya Sankara Naga Sai Akarsh Jana',  # Set your actual full name
            'email': 'akarshjana03091999@gmail.com',
            'phone': '4695929129',
            'linkedin': '',  # Set your LinkedIn URL if available
            'city': 'Arlington',
            'state': 'TX',
            'country': 'United States',
            'zip_code': '76013',
            
            # Education Information
            'school': 'University of Texas at Arlington',  # Your university/college
            'degree': 'Master of Science',  # Your degree type
            'discipline': 'Computer Science',  # Your major/field of study
            'graduation_year': '2025',  # Your graduation year
            'gpa_undergraduate': '3.7',  # Your undergraduate GPA (4.0 scale)
            'gpa_graduate': '3.75',  # Your graduate GPA if applicable
            'gpa_doctorate': 'Not applicable/Do not recall',  # Your doctorate GPA if applicable
            'sat_score': 'Not applicable/Do not recall',  # Your SAT score if applicable
            'act_score': 'Not applicable/Do not recall',  # Your ACT score if applicable
            'gre_score': 'Not applicable/Do not recall',  # Your GRE score if applicable
            
            # Work Authorization & Citizenship
            'work_authorization': 'Yes',  # Are you legally authorized to work in the US?
            'citizenship_status': 'Indian',  # Your citizenship status
            'security_clearance': 'No',  # Do you have active security clearance?
            'can_perform_essential_functions': 'Yes',  # Can you perform essential functions with/without accommodations?
            
            # How did you hear about this job
            'how_heard': 'LinkedIn',  # How did you hear about this job?
            'how_heard_other': '',  # If "Other" was selected, specify here
            
            # Additional Information
            'current_company': 'NA',  # Will be filled from resume experience
            'current_title': 'Software Engineer',  # Will be filled from resume experience
            'years_experience': '2+',  # Your years of experience
            'skills': '',  # Will be filled from resume skills
            'cover_letter': '',  # Will be filled with AI-generated content
        }
    
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User agent to avoid detection
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 10)
            
            logger.info("✅ Chrome WebDriver setup complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting up WebDriver: {e}")
            return False
    
    def find_form_field(self, field_names: List[str]) -> Optional[Any]:
        """Find form field by multiple possible names with improved detection"""
        for field_name in field_names:
            try:
                # Try different selectors with better detection
                selectors = [
                    # Exact matches first
                    f'input[name="{field_name}"]',
                    f'input[id="{field_name}"]',
                    f'textarea[name="{field_name}"]',
                    f'textarea[id="{field_name}"]',
                    f'select[name="{field_name}"]',
                    f'select[id="{field_name}"]',
                    
                    # Case-insensitive matches
                    f'input[name*="{field_name}" i]',
                    f'input[id*="{field_name}" i]',
                    f'input[placeholder*="{field_name}" i]',
                    f'textarea[name*="{field_name}" i]',
                    f'textarea[id*="{field_name}" i]',
                    f'textarea[placeholder*="{field_name}" i]',
                    f'select[name*="{field_name}" i]',
                    f'select[id*="{field_name}" i]',
                    
                    # Label-based detection
                    f'input[aria-label*="{field_name}" i]',
                    f'textarea[aria-label*="{field_name}" i]',
                    f'select[aria-label*="{field_name}" i]',
                    
                    # Data attributes
                    f'input[data-field*="{field_name}" i]',
                    f'textarea[data-field*="{field_name}" i]',
                    f'select[data-field*="{field_name}" i]',
                ]
                
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            if element.is_displayed() and element.is_enabled():
                                # Check if field is not read-only
                                readonly = element.get_attribute("readonly")
                                disabled = element.get_attribute("disabled")
                                
                                if not readonly and not disabled:
                                    logger.info(f"✅ Found field: {field_name} using selector: {selector}")
                                    return element
                                else:
                                    logger.debug(f"⚠️ Field {field_name} is read-only or disabled")
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                logger.debug(f"Field {field_name} not found: {e}")
                continue
        
        logger.warning(f"⚠️ Could not find field for: {field_names}")
        return None
    
    def fill_text_field(self, element, value: str):
        """Fill a text input field with improved interaction"""
        try:
            # Clear the field first
            element.clear()
            
            # Wait a moment for the clear to take effect
            time.sleep(0.5)
            
            # Try different methods to fill the field
            try:
                # Method 1: Direct send_keys
                element.send_keys(value)
            except Exception as e1:
                logger.debug(f"Method 1 failed: {e1}")
                try:
                    # Method 2: Click and then send_keys
                    element.click()
                    time.sleep(0.2)
                    element.send_keys(value)
                except Exception as e2:
                    logger.debug(f"Method 2 failed: {e2}")
                    try:
                        # Method 3: JavaScript injection
                        self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
                        # Trigger change event
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
                    except Exception as e3:
                        logger.debug(f"Method 3 failed: {e3}")
                        return False
            
            logger.info(f"✅ Filled field with: {value[:20]}...")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error filling field: {e}")
            return False
    
    def fill_textarea_field(self, element, value: str):
        """Fill a textarea field with improved interaction"""
        try:
            # Clear the field first
            element.clear()
            
            # Wait a moment for the clear to take effect
            time.sleep(0.5)
            
            # Try different methods to fill the field
            try:
                # Method 1: Direct send_keys
                element.send_keys(value)
            except Exception as e1:
                logger.debug(f"Method 1 failed: {e1}")
                try:
                    # Method 2: Click and then send_keys
                    element.click()
                    time.sleep(0.2)
                    element.send_keys(value)
                except Exception as e2:
                    logger.debug(f"Method 2 failed: {e2}")
                    try:
                        # Method 3: JavaScript injection
                        self.driver.execute_script("arguments[0].value = arguments[1];", element, value)
                        # Trigger change event
                        self.driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", element)
                    except Exception as e3:
                        logger.debug(f"Method 3 failed: {e3}")
                        return False
            
            logger.info(f"✅ Filled textarea with: {len(value)} characters")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error filling textarea: {e}")
            return False
    
    def upload_resume(self, resume_path: str):
        """Upload resume file"""
        try:
            # Look for file upload fields
            file_selectors = [
                'input[type="file"]',
                'input[accept*="pdf"]',
                'input[accept*="doc"]',
                'input[name*="resume" i]',
                'input[name*="cv" i]'
            ]
            
            for selector in file_selectors:
                try:
                    file_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if file_input.is_displayed():
                        file_input.send_keys(resume_path)
                        logger.info(f"✅ Uploaded resume: {resume_path}")
                        return True
                except NoSuchElementException:
                    continue
            
            logger.warning("⚠️ No file upload field found")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error uploading resume: {e}")
            return False
    
    def get_field_value(self, field_type: str, resume_data: Dict[str, Any]) -> str:
        """Get appropriate value for a field type, prioritizing default personal info"""
        
        if field_type == 'first_name':
            # Use default first name instead of parsing from resume
            return self.default_personal_info['first_name']
        
        elif field_type == 'last_name':
            # Use default last name instead of parsing from resume
            return self.default_personal_info['last_name']
        
        elif field_type == 'full_name':
            # Use default full name
            return self.default_personal_info['full_name']
        
        elif field_type == 'email':
            # Use default email or resume email
            return resume_data.get('email') or self.default_personal_info['email']
        
        elif field_type == 'phone':
            # Use default phone or resume phone
            phone = resume_data.get('phone', '')
            if phone:
                # Clean up phone number
                phone = re.sub(r'[\n\s]', '', phone)
            return phone or self.default_personal_info['phone']
        
        elif field_type == 'linkedin':
            # Use default LinkedIn or resume LinkedIn
            return resume_data.get('linkedin') or self.default_personal_info['linkedin']
        
        elif field_type == 'city':
            # Parse from resume location or use default
            location = resume_data.get('location', '')
            if isinstance(location, str) and ',' in location:
                return location.split(',')[0].strip()
            return self.default_personal_info['city']
        
        elif field_type == 'state':
            # Parse from resume location or use default
            location = resume_data.get('location', '')
            if isinstance(location, str) and ',' in location:
                parts = location.split(',')
                if len(parts) > 1:
                    return parts[1].strip()
            return self.default_personal_info['state']
        
        elif field_type == 'country':
            # Parse from resume location or use default
            location = resume_data.get('location', '')
            if isinstance(location, str) and ',' in location:
                parts = location.split(',')
                if len(parts) > 2:
                    return parts[2].strip()
            return self.default_personal_info['country']
        
        # Education fields - use default values
        elif field_type == 'school':
            return self.default_personal_info['school']
        
        elif field_type == 'degree':
            return self.default_personal_info['degree']
        
        elif field_type == 'discipline':
            return self.default_personal_info['discipline']
        
        elif field_type == 'graduation_year':
            return self.default_personal_info['graduation_year']
        
        elif field_type == 'gpa_undergraduate':
            return self.default_personal_info['gpa_undergraduate']
        
        elif field_type == 'gpa_graduate':
            return self.default_personal_info['gpa_graduate']
        
        elif field_type == 'gpa_doctorate':
            return self.default_personal_info['gpa_doctorate']
        
        elif field_type == 'sat_score':
            return self.default_personal_info['sat_score']
        
        elif field_type == 'act_score':
            return self.default_personal_info['act_score']
        
        elif field_type == 'gre_score':
            return self.default_personal_info['gre_score']
        
        # Work authorization fields - use default values
        elif field_type == 'work_authorization':
            return self.default_personal_info['work_authorization']
        
        elif field_type == 'citizenship_status':
            return self.default_personal_info['citizenship_status']
        
        elif field_type == 'security_clearance':
            return self.default_personal_info['security_clearance']
        
        elif field_type == 'can_perform_essential_functions':
            return self.default_personal_info['can_perform_essential_functions']
        
        # How did you hear about this job
        elif field_type == 'how_heard':
            return self.default_personal_info['how_heard']
        
        elif field_type == 'how_heard_other':
            return self.default_personal_info['how_heard_other']
        
        elif field_type == 'current_company':
            # Get from resume experience
            experience = resume_data.get('experience', [])
            if experience and len(experience) > 0:
                return experience[0].get('company', '')
            return ''
        
        elif field_type == 'current_title':
            # Get from resume experience
            experience = resume_data.get('experience', [])
            if experience and len(experience) > 0:
                return experience[0].get('title', '')
            return ''
        
        elif field_type == 'skills':
            # Get from resume skills
            skills = resume_data.get('skills', [])
            if skills:
                return ", ".join(skills[:10])  # Limit to first 10 skills
            return ''
        
        else:
            # For other fields, try to get from resume data
            return resume_data.get(field_type, '')
    
    def automate_job_application(self, job_url: str, resume_data: Dict[str, Any], 
                               cover_letter: str, resume_path: Optional[str] = None) -> Dict[str, Any]:
        """Automate filling out a job application form"""
        
        logger.info(f"🚀 Starting automation for: {job_url}")
        
        # Debug resume data structure
        logger.info(f"📋 Resume data structure:")
        logger.info(f"   - Name: {resume_data.get('name', 'N/A')}")
        logger.info(f"   - Email: {resume_data.get('email', 'N/A')}")
        logger.info(f"   - Phone: {resume_data.get('phone', 'N/A')}")
        logger.info(f"   - Location: {resume_data.get('location', 'N/A')}")
        logger.info(f"   - Skills: {len(resume_data.get('skills', []))} skills")
        logger.info(f"   - Experience: {len(resume_data.get('experience', []))} entries")
        
        try:
            # Setup driver
            if not self.setup_driver():
                return {"success": False, "error": "Failed to setup WebDriver"}
            
            # Navigate to job application page
            logger.info(f"🌐 Navigating to: {job_url}")
            self.driver.get(job_url)
            
            # Wait for page to load
            time.sleep(5)  # Increased wait time
            
            # Debug form fields on the page
            logger.info("🔍 Analyzing form fields on the page...")
            visible_fields = self.debug_form_fields()
            
            # Track filled fields
            filled_fields = []
            errors = []
            
            # Fill personal information (HIGH PRIORITY)
            logger.info("📝 Filling personal information...")
            
            # First Name
            first_name_field = self.find_form_field(self.field_mappings['first_name'])
            if first_name_field:
                first_name = self.get_field_value('first_name', resume_data)
                if first_name and self.fill_text_field(first_name_field, first_name):
                    filled_fields.append('first_name')
            
            # Last Name
            last_name_field = self.find_form_field(self.field_mappings['last_name'])
            if last_name_field:
                last_name = self.get_field_value('last_name', resume_data)
                if last_name and self.fill_text_field(last_name_field, last_name):
                    filled_fields.append('last_name')
            
            # Full Name (if separate first/last name fields not found)
            if 'first_name' not in filled_fields and 'last_name' not in filled_fields:
                full_name_field = self.find_form_field(self.field_mappings['full_name'])
                if full_name_field:
                    full_name = self.get_field_value('full_name', resume_data)
                    if full_name and self.fill_text_field(full_name_field, full_name):
                        filled_fields.append('full_name')
            
            # Email
            email_field = self.find_form_field(self.field_mappings['email'])
            if email_field:
                email = self.get_field_value('email', resume_data)
                if email and self.fill_text_field(email_field, email):
                    filled_fields.append('email')
            
            # Phone
            phone_field = self.find_form_field(self.field_mappings['phone'])
            if phone_field:
                phone = self.get_field_value('phone', resume_data)
                if phone and self.fill_text_field(phone_field, phone):
                    filled_fields.append('phone')
            
            # LinkedIn
            linkedin_field = self.find_form_field(self.field_mappings['linkedin'])
            if linkedin_field:
                linkedin = self.get_field_value('linkedin', resume_data)
                if linkedin and self.fill_text_field(linkedin_field, linkedin):
                    filled_fields.append('linkedin')
            
            # Fill location information (MEDIUM PRIORITY)
            logger.info("📍 Filling location information...")
            
            # City
            city_field = self.find_form_field(self.field_mappings['city'])
            if city_field:
                city = self.get_field_value('city', resume_data)
                if city and self.fill_text_field(city_field, city):
                    filled_fields.append('city')
            
            # State
            state_field = self.find_form_field(self.field_mappings['state'])
            if state_field:
                state = self.get_field_value('state', resume_data)
                if state and self.fill_text_field(state_field, state):
                    filled_fields.append('state')
            
            # Country
            country_field = self.find_form_field(self.field_mappings['country'])
            if country_field:
                country = self.get_field_value('country', resume_data)
                if country and self.fill_text_field(country_field, country):
                    filled_fields.append('country')
            
            # Fill education information (HIGH PRIORITY)
            logger.info("🎓 Filling education information...")
            
            # School
            school_field = self.find_form_field(self.field_mappings['school'])
            if school_field:
                school = self.get_field_value('school', resume_data)
                if school and self.fill_text_field(school_field, school):
                    filled_fields.append('school')
            
            # Degree
            degree_field = self.find_form_field(self.field_mappings['degree'])
            if degree_field:
                degree = self.get_field_value('degree', resume_data)
                if degree and self.fill_text_field(degree_field, degree):
                    filled_fields.append('degree')
            
            # Discipline
            discipline_field = self.find_form_field(self.field_mappings['discipline'])
            if discipline_field:
                discipline = self.get_field_value('discipline', resume_data)
                if discipline and self.fill_text_field(discipline_field, discipline):
                    filled_fields.append('discipline')
            
            # Graduation Year
            graduation_year_field = self.find_form_field(self.field_mappings['graduation_year'])
            if graduation_year_field:
                graduation_year = self.get_field_value('graduation_year', resume_data)
                if graduation_year and self.fill_text_field(graduation_year_field, graduation_year):
                    filled_fields.append('graduation_year')
            
            # GPA Fields
            gpa_fields = ['gpa_undergraduate', 'gpa_graduate', 'gpa_doctorate']
            for gpa_field_type in gpa_fields:
                gpa_field = self.find_form_field(self.field_mappings[gpa_field_type])
                if gpa_field:
                    gpa_value = self.get_field_value(gpa_field_type, resume_data)
                    if gpa_value and self.fill_text_field(gpa_field, gpa_value):
                        filled_fields.append(gpa_field_type)
            
            # Test Score Fields
            test_score_fields = ['sat_score', 'act_score', 'gre_score']
            for test_field_type in test_score_fields:
                test_field = self.find_form_field(self.field_mappings[test_field_type])
                if test_field:
                    test_value = self.get_field_value(test_field_type, resume_data)
                    if test_value and self.fill_text_field(test_field, test_value):
                        filled_fields.append(test_field_type)
            
            # Fill work authorization information (HIGH PRIORITY)
            logger.info("🔐 Filling work authorization information...")
            
            # Work Authorization
            work_auth_field = self.find_form_field(self.field_mappings['work_authorization'])
            if work_auth_field:
                work_auth = self.get_field_value('work_authorization', resume_data)
                if work_auth and self.fill_text_field(work_auth_field, work_auth):
                    filled_fields.append('work_authorization')
            
            # Citizenship Status
            citizenship_field = self.find_form_field(self.field_mappings['citizenship_status'])
            if citizenship_field:
                citizenship = self.get_field_value('citizenship_status', resume_data)
                if citizenship and self.fill_text_field(citizenship_field, citizenship):
                    filled_fields.append('citizenship_status')
            
            # Security Clearance
            clearance_field = self.find_form_field(self.field_mappings['security_clearance'])
            if clearance_field:
                clearance = self.get_field_value('security_clearance', resume_data)
                if clearance and self.fill_text_field(clearance_field, clearance):
                    filled_fields.append('security_clearance')
            
            # Can Perform Essential Functions
            essential_functions_field = self.find_form_field(self.field_mappings['can_perform_essential_functions'])
            if essential_functions_field:
                essential_functions = self.get_field_value('can_perform_essential_functions', resume_data)
                if essential_functions and self.fill_text_field(essential_functions_field, essential_functions):
                    filled_fields.append('can_perform_essential_functions')
            
            # Fill how did you hear about this job (MEDIUM PRIORITY)
            logger.info("📢 Filling how did you hear about this job...")
            
            how_heard_field = self.find_form_field(self.field_mappings['how_heard'])
            if how_heard_field:
                how_heard = self.get_field_value('how_heard', resume_data)
                if how_heard and self.fill_text_field(how_heard_field, how_heard):
                    filled_fields.append('how_heard')
            
            # How heard other (if applicable)
            how_heard_other_field = self.find_form_field(self.field_mappings['how_heard_other'])
            if how_heard_other_field:
                how_heard_other = self.get_field_value('how_heard_other', resume_data)
                if how_heard_other and self.fill_text_field(how_heard_other_field, how_heard_other):
                    filled_fields.append('how_heard_other')
            
            # Fill professional information (MEDIUM PRIORITY)
            logger.info("💼 Filling professional information...")
            
            # Current Company
            company_field = self.find_form_field(self.field_mappings['current_company'])
            if company_field:
                company = self.get_field_value('current_company', resume_data)
                if company and self.fill_text_field(company_field, company):
                    filled_fields.append('current_company')
            
            # Current Title
            title_field = self.find_form_field(self.field_mappings['current_title'])
            if title_field:
                title = self.get_field_value('current_title', resume_data)
                if title and self.fill_text_field(title_field, title):
                    filled_fields.append('current_title')
            
            # Fill skills (LOW PRIORITY)
            logger.info("🔧 Filling skills...")
            skills_field = self.find_form_field(self.field_mappings['skills'])
            if skills_field:
                skills = self.get_field_value('skills', resume_data)
                if skills and self.fill_textarea_field(skills_field, skills):
                    filled_fields.append('skills')
            
            # Fill cover letter (HIGH PRIORITY)
            logger.info("📄 Filling cover letter...")
            cover_letter_field = self.find_form_field(self.field_mappings['cover_letter'])
            if cover_letter_field and cover_letter:
                if self.fill_textarea_field(cover_letter_field, cover_letter):
                    filled_fields.append('cover_letter')
            
            # Upload resume (HIGH PRIORITY)
            if resume_path:
                logger.info("📎 Uploading resume...")
                if self.upload_resume(resume_path):
                    filled_fields.append('resume_upload')
            
            # Make fields editable for manual interaction
            logger.info("🔧 Making fields editable for manual interaction...")
            self.make_fields_editable()
            
            # Summary
            logger.info(f"✅ Automation completed!")
            logger.info(f"   📝 Filled {len(filled_fields)} fields: {filled_fields}")
            logger.info(f"   📊 Total visible fields on page: {len(visible_fields)}")
            
            if len(filled_fields) == 0:
                logger.warning("⚠️ No fields were filled! This might indicate:")
                logger.warning("   - Form fields are not detected properly")
                logger.warning("   - Page structure is different than expected")
                logger.warning("   - Form is loaded dynamically")
                logger.info("💡 You can manually fill the form and submit")
            
            # Keep browser open for manual review and submission
            if self.keep_open:
                logger.info(f"⏳ Keeping browser open for {self.delay_after_fill} seconds for manual review...")
                logger.info(f"   📝 You can now review and edit the filled form")
                logger.info(f"   ✅ All fields should be editable for manual modification")
                logger.info(f"   📤 You can submit the form manually")
                logger.info(f"   🔄 Browser will close automatically after {self.delay_after_fill} seconds")
                
                try:
                    time.sleep(self.delay_after_fill)
                    logger.info(f"✅ Delay completed, closing browser...")
                except KeyboardInterrupt:
                    logger.info(f"⚠️ User interrupted, closing browser...")
                finally:
                    if self.driver:
                        self.driver.quit()
                        logger.info(f"✅ Browser closed")
            else:
                if self.driver:
                    self.driver.quit()
                    logger.info(f"✅ Browser closed immediately")
            
            return {
                "success": True,
                "filled_fields": filled_fields,
                "errors": errors,
                "url": job_url,
                "browser_kept_open": self.keep_open,
                "delay_seconds": self.delay_after_fill,
                "total_visible_fields": len(visible_fields),
                "field_detection_debug": visible_fields[:5]  # Include first 5 fields for debugging
            }
            
        except Exception as e:
            logger.error(f"❌ Automation failed: {e}")
            if self.driver:
                self.driver.quit()
                logger.info(f"✅ Browser closed due to error")
            return {
                "success": False,
                "error": str(e),
                "url": job_url
            }
    
    def preview_form_fields(self, job_url: str) -> Dict[str, Any]:
        """Preview available form fields on a job application page"""
        
        logger.info(f"🔍 Previewing form fields for: {job_url}")
        
        try:
            if not self.setup_driver():
                return {"success": False, "error": "Failed to setup WebDriver"}
            
            self.driver.get(job_url)
            time.sleep(3)
            
            # Find all form elements
            form_elements = []
            
            # Input fields
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for input_elem in inputs:
                try:
                    if input_elem.is_displayed():
                        element_info = {
                            "type": "input",
                            "tag": input_elem.tag_name,
                            "name": input_elem.get_attribute("name"),
                            "id": input_elem.get_attribute("id"),
                            "placeholder": input_elem.get_attribute("placeholder"),
                            "type_attr": input_elem.get_attribute("type")
                        }
                        form_elements.append(element_info)
                except:
                    continue
            
            # Textarea fields
            textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            for textarea in textareas:
                try:
                    if textarea.is_displayed():
                        element_info = {
                            "type": "textarea",
                            "tag": textarea.tag_name,
                            "name": textarea.get_attribute("name"),
                            "id": textarea.get_attribute("id"),
                            "placeholder": textarea.get_attribute("placeholder")
                        }
                        form_elements.append(element_info)
                except:
                    continue
            
            # Select fields
            selects = self.driver.find_elements(By.TAG_NAME, "select")
            for select in selects:
                try:
                    if select.is_displayed():
                        element_info = {
                            "type": "select",
                            "tag": select.tag_name,
                            "name": select.get_attribute("name"),
                            "id": select.get_attribute("id")
                        }
                        form_elements.append(element_info)
                except:
                    continue
            
            logger.info(f"✅ Found {len(form_elements)} form elements")
            
            return {
                "success": True,
                "form_elements": form_elements,
                "url": job_url
            }
            
        except Exception as e:
            logger.error(f"❌ Preview failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "url": job_url
            }
        
        finally:
            if self.driver:
                self.driver.quit()

    def make_fields_editable(self):
        """Make form fields editable after automation fills them"""
        try:
            # Remove readonly attributes from all input fields
            readonly_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[readonly]')
            for input_elem in readonly_inputs:
                self.driver.execute_script("arguments[0].removeAttribute('readonly');", input_elem)
            
            # Remove disabled attributes from all input fields
            disabled_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[disabled]')
            for input_elem in disabled_inputs:
                self.driver.execute_script("arguments[0].removeAttribute('disabled');", input_elem)
            
            # Remove readonly attributes from all textarea fields
            readonly_textareas = self.driver.find_elements(By.CSS_SELECTOR, 'textarea[readonly]')
            for textarea in readonly_textareas:
                self.driver.execute_script("arguments[0].removeAttribute('readonly');", textarea)
            
            # Remove disabled attributes from all textarea fields
            disabled_textareas = self.driver.find_elements(By.CSS_SELECTOR, 'textarea[disabled]')
            for textarea in disabled_textareas:
                self.driver.execute_script("arguments[0].removeAttribute('disabled');", textarea)
            
            logger.info("✅ Made form fields editable for manual interaction")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️ Could not make all fields editable: {e}")
            return False
    
    def debug_form_fields(self):
        """Debug and log all available form fields on the page"""
        try:
            logger.info("🔍 Debugging form fields on the page...")
            
            # Find all form elements
            all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
            all_textareas = self.driver.find_elements(By.TAG_NAME, "textarea")
            all_selects = self.driver.find_elements(By.TAG_NAME, "select")
            
            logger.info(f"📊 Found {len(all_inputs)} input fields, {len(all_textareas)} textareas, {len(all_selects)} selects")
            
            # Log details of visible form fields
            visible_fields = []
            
            for elem in all_inputs + all_textareas + all_selects:
                try:
                    if elem.is_displayed():
                        field_info = {
                            "tag": elem.tag_name,
                            "name": elem.get_attribute("name"),
                            "id": elem.get_attribute("id"),
                            "placeholder": elem.get_attribute("placeholder"),
                            "type": elem.get_attribute("type"),
                            "readonly": elem.get_attribute("readonly"),
                            "disabled": elem.get_attribute("disabled"),
                            "aria-label": elem.get_attribute("aria-label")
                        }
                        visible_fields.append(field_info)
                except:
                    continue
            
            logger.info(f"📋 Visible form fields ({len(visible_fields)}):")
            for i, field in enumerate(visible_fields[:10]):  # Show first 10
                logger.info(f"   {i+1}. {field['tag']} - name: '{field['name']}', id: '{field['id']}', placeholder: '{field['placeholder']}'")
            
            if len(visible_fields) > 10:
                logger.info(f"   ... and {len(visible_fields) - 10} more fields")
            
            return visible_fields
            
        except Exception as e:
            logger.error(f"❌ Error debugging form fields: {e}")
            return []

# Global automation instance with browser kept open for 30 seconds
form_automation = JobFormAutomation(keep_open=True, delay_after_fill=30)

def close_browser():
    """Manually close the browser if it's open"""
    if form_automation.driver:
        form_automation.driver.quit()
        form_automation.driver = None
        logger.info("✅ Browser manually closed")
        return True
    return False 