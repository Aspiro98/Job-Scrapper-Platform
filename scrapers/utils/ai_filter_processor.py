import json
import os
from typing import Dict, List, Optional, Any
from groq import Groq

class AIFilterProcessor:
    """AI-powered job filtering processor using Groq's Llama3-8b-8192 model"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI filter processor"""
        # Use provided API key, then environment variable, then default key
        self.api_key = api_key or os.getenv('GROQ_API_KEY') or "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"
        
        try:
            self.client = Groq(api_key=self.api_key)
            self.model = "llama3-8b-8192"
            # Test the API key
            test_response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=10
            )
            print(f"✅ AI Processor initialized with API key: {self.api_key[:10]}...")
        except Exception as e:
            print(f"❌ Failed to initialize AI Processor: {e}")
            print("🔧 Please check your API key or try generating a new one from https://console.groq.com/")
            raise ValueError(f"Invalid API key: {e}")
    
    def process_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single job through all AI filters
        
        Args:
            job_data: Raw job data with title, location, company, etc.
            
        Returns:
            Processed job data with AI-extracted information
        """
        try:
            # Extract basic info
            title = job_data.get('title', '')
            location = job_data.get('location', '')
            company = job_data.get('company', '')
            description = job_data.get('description', '')
            
            # Add delay to prevent rate limiting
            import time
            time.sleep(0.1)  # 100ms delay between API calls
            
            # Process through AI filters
            location_info = self.parse_location(location)
            experience_level = self.extract_experience(title, description)
            role_category = self.categorize_role(title, description)
            company_normalized = self.normalize_company(company)
            
            # Add AI-processed data to job
            processed_job = job_data.copy()
            processed_job.update({
                'location_info': location_info,
                'experience_level': experience_level,
                'role_category': role_category,
                'company_normalized': company_normalized,
                'ai_processed': True
            })
            
            return processed_job
            
        except Exception as e:
            print(f"Error processing job with AI: {e}")
            # Return original job data if AI processing fails
            return job_data
    
    def parse_location(self, location_str: str) -> Dict[str, Any]:
        """
        Parse location string using AI
        
        Args:
            location_str: Raw location string
            
        Returns:
            Structured location information
        """
        if not location_str or location_str.lower() in ['n/a', 'remote', 'anywhere']:
            return {
                'country': 'remote',
                'states': [],
                'cities': [],
                'is_remote': True,
                'raw_location': location_str
            }
        
        prompt = f"""
Parse this job location into structured data. Return only valid JSON without any markdown formatting.

Location: "{location_str}"

Return a JSON object with these exact fields:
- country: The country (e.g., "united states", "canada", "remote")
- states: Array of states/provinces (e.g., ["california", "washington"])
- cities: Array of cities (e.g., ["san francisco", "seattle"])
- is_remote: Boolean (true/false)
- raw_location: Original location string

Examples:
- "San Francisco, CA" → {{"country": "united states", "states": ["california"], "cities": ["san francisco"], "is_remote": false, "raw_location": "San Francisco, CA"}}
- "Remote" → {{"country": "remote", "states": [], "cities": [], "is_remote": true, "raw_location": "Remote"}}
- "New York, NY | Seattle, WA" → {{"country": "united states", "states": ["new york", "washington"], "cities": ["new york", "seattle"], "is_remote": false, "raw_location": "New York, NY | Seattle, WA"}}

Return only the JSON object:
"""
        
        try:
            # Add retry logic for API calls
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.1,
                        max_tokens=500
                    )
                    
                    result = response.choices[0].message.content.strip()
                    break  # Success, exit retry loop
                    
                except Exception as api_error:
                    if "401" in str(api_error) and "invalid_api_key" in str(api_error).lower():
                        print(f"❌ Invalid API key on attempt {attempt + 1}")
                        if attempt == max_retries - 1:
                            raise api_error
                        continue
                    elif "429" in str(api_error) or "rate_limit" in str(api_error).lower():
                        print(f"⏳ Rate limit hit, waiting {2 ** attempt} seconds... (attempt {attempt + 1})")
                        import time
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        raise api_error
            
            # Clean up the response - remove any markdown formatting
            if result.startswith('```json'):
                result = result[7:]
            if result.startswith('```'):
                result = result[3:]
            if result.endswith('```'):
                result = result[:-3]
            
            # Remove any quotes around the entire response
            result = result.strip('"')
            
            # Try to extract JSON from the response (in case there's text before/after)
            import re
            json_match = re.search(r'\{.*\}', result, re.DOTALL)
            if json_match:
                result = json_match.group()
            
            try:
                location_info = json.loads(result)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                print(f"Raw response: {result}")
                raise e
            return location_info
            
        except Exception as e:
            print(f"Error parsing location '{location_str}': {e}")
            return {
                'country': 'other',
                'states': [],
                'cities': [],
                'is_remote': False,
                'raw_location': location_str
            }
    
    def extract_experience(self, title: str, description: str) -> str:
        """
        Extract experience level from job title and description
        
        Args:
            title: Job title
            description: Job description
            
        Returns:
            Experience level category
        """
        prompt = f"""
Analyze this job and determine the experience level. Return only the experience level category.

Job Title: "{title}"
Job Description: "{description[:500]}..." (truncated)

Experience levels:
- entry: Entry level, junior, 0-2 years, recent graduate
- mid: Mid-level, 3-5 years, intermediate
- senior: Senior, 5+ years, lead, principal
- staff: Staff, senior staff, 7+ years
- director: Director, VP, executive level
- unknown: Cannot determine

Return only the experience level category (entry, mid, senior, staff, director, or unknown):
"""
        
        try:
            # Add retry logic for API calls
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.1,
                        max_tokens=50
                    )
                    
                    experience = response.choices[0].message.content.strip().lower()
                    break  # Success, exit retry loop
                    
                except Exception as api_error:
                    if "401" in str(api_error) and "invalid_api_key" in str(api_error).lower():
                        print(f"❌ Invalid API key on attempt {attempt + 1}")
                        if attempt == max_retries - 1:
                            raise api_error
                        continue
                    elif "rate_limit" in str(api_error).lower():
                        print(f"⏳ Rate limit hit, waiting... (attempt {attempt + 1})")
                        import time
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        raise api_error
            
            # Validate response
            valid_levels = ['entry', 'mid', 'senior', 'staff', 'director', 'unknown']
            if experience in valid_levels:
                return experience
            else:
                return 'unknown'
                
        except Exception as e:
            print(f"Error extracting experience: {e}")
            return 'unknown'
    
    def categorize_role(self, title: str, description: str) -> str:
        """
        Categorize job role from title and description
        
        Args:
            title: Job title
            description: Job description
            
        Returns:
            Role category
        """
        prompt = f"""
Categorize this job into a role category. Return only the role category.

Job Title: "{title}"
Job Description: "{description[:500]}..." (truncated)

Role categories:
- engineering: Software engineer, developer, programmer, DevOps, SRE
- data_science: Data scientist, ML engineer, AI engineer, analyst
- product: Product manager, product owner, program manager
- design: UX designer, UI designer, graphic designer
- sales: Sales, business development, account executive
- marketing: Marketing, growth, content, SEO
- operations: Operations, strategy, business operations
- hr: HR, recruiting, talent acquisition
- finance: Finance, accounting, controller
- legal: Legal, compliance, counsel
- other: Other roles not listed above

Return only the role category:
"""
        
        try:
            # Add retry logic for API calls
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.1,
                        max_tokens=50
                    )
                    
                    role = response.choices[0].message.content.strip().lower()
                    break  # Success, exit retry loop
                    
                except Exception as api_error:
                    if "401" in str(api_error) and "invalid_api_key" in str(api_error).lower():
                        print(f"❌ Invalid API key on attempt {attempt + 1}")
                        if attempt == max_retries - 1:
                            raise api_error
                        continue
                    elif "rate_limit" in str(api_error).lower():
                        print(f"⏳ Rate limit hit, waiting... (attempt {attempt + 1})")
                        import time
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        raise api_error
            
            # Validate response
            valid_roles = ['engineering', 'data_science', 'product', 'design', 'sales', 
                          'marketing', 'operations', 'hr', 'finance', 'legal', 'other']
            if role in valid_roles:
                return role
            else:
                return 'other'
                
        except Exception as e:
            print(f"Error categorizing role: {e}")
            return 'other'
    
    def normalize_company(self, company: str) -> str:
        """
        Normalize company name
        
        Args:
            company: Raw company name
            
        Returns:
            Normalized company name
        """
        if not company:
            return 'Unknown'
        
        prompt = f"""
Normalize this company name to a standard format. Return only the normalized name.

Company: "{company}"

Examples:
- "Anthropic PBC" → "Anthropic"
- "Google LLC" → "Google"
- "Microsoft Corporation" → "Microsoft"
- "Meta Platforms Inc." → "Meta"

Return only the normalized company name:
"""
        
        try:
            # Add retry logic for API calls
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.1,
                        max_tokens=100
                    )
                    
                    normalized = response.choices[0].message.content.strip()
                    break  # Success, exit retry loop
                    
                except Exception as api_error:
                    if "401" in str(api_error) and "invalid_api_key" in str(api_error).lower():
                        print(f"❌ Invalid API key on attempt {attempt + 1}")
                        if attempt == max_retries - 1:
                            raise api_error
                        continue
                    elif "rate_limit" in str(api_error).lower():
                        print(f"⏳ Rate limit hit, waiting... (attempt {attempt + 1})")
                        import time
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    else:
                        raise api_error
            # Remove quotes if present
            normalized = normalized.strip('"').strip("'")
            return normalized if normalized else company
            
        except Exception as e:
            print(f"Error normalizing company: {e}")
            return company
    
    def get_hierarchical_filters(self, jobs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate hierarchical filters from AI-processed job data
        
        Args:
            jobs: List of processed job dictionaries
            
        Returns:
            Hierarchical filter structure
        """
        countries = {}
        experience_levels = set()
        role_categories = set()
        companies = set()
        
        for job in jobs:
            # Location filters
            location_info = job.get('location_info', {})
            country = location_info.get('country', 'other')
            states = location_info.get('states', [])
            cities = location_info.get('cities', [])
            
            if country not in countries:
                countries[country] = {'states': set(), 'cities': set()}
            
            for state in states:
                countries[country]['states'].add(state)
            for city in cities:
                countries[country]['cities'].add(city)
            
            # Experience levels
            exp_level = job.get('experience_level', 'unknown')
            experience_levels.add(exp_level)
            
            # Role categories
            role = job.get('role_category', 'other')
            role_categories.add(role)
            
            # Companies
            company = job.get('company_normalized', job.get('company', 'Unknown'))
            companies.add(company)
        
        # Convert sets to sorted lists
        result = {
            'location_filters': {},
            'experience_levels': sorted(list(experience_levels)),
            'role_categories': sorted(list(role_categories)),
            'companies': sorted(list(companies))
        }
        
        for country, data in countries.items():
            result['location_filters'][country] = {
                'states': sorted(list(data['states'])),
                'cities': sorted(list(data['cities']))
            }
        
        return result
    
    def matches_location_filter(self, job_location_info: Dict[str, Any], 
                               selected_country: str, selected_state: str = '') -> bool:
        """
        Check if a job matches the selected location filters
        
        Args:
            job_location_info: Job's location information from AI
            selected_country: Selected country filter
            selected_state: Selected state/city filter
            
        Returns:
            True if job matches the location filters
        """
        if not selected_country:
            return True
        
        job_country = job_location_info.get('country', 'other')
        job_states = job_location_info.get('states', [])
        job_cities = job_location_info.get('cities', [])
        
        # Check country match
        if job_country != selected_country:
            return False
        
        # If no state selected, match any location in that country
        if not selected_state:
            return True
        
        # Check state/city match
        if selected_state in job_states or selected_state in job_cities:
            return True
        
        return False 