import requests
import time
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import json
import logging
from urllib.parse import quote_plus, urljoin
import random
import os
import pickle

logger = logging.getLogger(__name__)

class JobDateEstimator:
    """
    Estimates job posted dates by searching multiple job platforms
    Optimized for performance with caching and pattern analysis
    """
    
    def __init__(self, cache_file='date_cache.pkl', use_external_apis=False):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Performance settings
        self.request_delay = 2  # seconds between requests
        self.last_request_time = 0
        self.use_external_apis = use_external_apis  # Disable external APIs by default for speed
        self.cache_file = cache_file
        self.cache = self._load_cache()
        
    def _load_cache(self):
        """Load cached date estimates"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
        except Exception as e:
            logger.warning(f"Could not load cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save cached date estimates"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
        except Exception as e:
            logger.warning(f"Could not save cache: {e}")
    
    def _get_cache_key(self, job_title, company_name, location=None):
        """Generate cache key for a job"""
        key_parts = [job_title.lower().strip(), company_name.lower().strip()]
        if location:
            key_parts.append(location.lower().strip())
        return "|".join(key_parts)
    
    def _rate_limit(self):
        """Implement rate limiting between requests"""
        if not self.use_external_apis:
            return
            
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def estimate_job_date(self, job_title, company_name, location=None):
        """
        Estimate job posted date - optimized for performance
        
        Args:
            job_title (str): Job title to search for
            company_name (str): Company name
            location (str): Optional location
            
        Returns:
            dict: Contains estimated_date, confidence, and source
        """
        # Check cache first
        cache_key = self._get_cache_key(job_title, company_name, location)
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            # Add display formatting
            cached_result['posted_date_display'] = self.format_date_for_display(cached_result.get('estimated_date'))
            cached_result['posted_date_color'] = self.get_confidence_color(cached_result.get('confidence', 'low'))
            return cached_result
        
        # Use pattern analysis by default (fast)
        if not self.use_external_apis:
            result = self._estimate_based_on_patterns(job_title)
        else:
            # Try external platforms only if explicitly enabled
            result = self._try_external_platforms(job_title, company_name, location)
            if not result.get('estimated_date'):
                result = self._estimate_based_on_patterns(job_title)
        
        # Cache the result
        self.cache[cache_key] = result
        self._save_cache()
        
        # Add display formatting
        result['posted_date_display'] = self.format_date_for_display(result.get('estimated_date'))
        result['posted_date_color'] = self.get_confidence_color(result.get('confidence', 'low'))
        
        return result
    
    def _try_external_platforms(self, job_title, company_name, location=None):
        """Try external platforms for date estimation"""
        search_query = f"{job_title} {company_name}"
        if location:
            search_query += f" {location}"
            
        results = {
            'estimated_date': None,
            'confidence': 'low',
            'source': None,
            'date_range': None
        }
        
        # Try multiple platforms
        platforms = [
            self._search_linkedin,
            self._search_indeed,
            self._search_glassdoor,
            self._search_ziprecruiter
        ]
        
        for platform_func in platforms:
            try:
                self._rate_limit()
                platform_result = platform_func(search_query, company_name)
                if platform_result and platform_result.get('date'):
                    results.update(platform_result)
                    break
            except Exception as e:
                logger.warning(f"Error searching {platform_func.__name__}: {e}")
                continue
        
        return results
    
    def _search_linkedin(self, search_query, company_name):
        """Search LinkedIn for job posting date"""
        try:
            # LinkedIn job search URL (public jobs)
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(search_query)}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for job cards with posting dates
                job_cards = soup.find_all('div', {'class': 'job-search-card'})
                
                for card in job_cards[:5]:  # Check first 5 results
                    # Look for time posted indicators
                    time_element = card.find('time') or card.find('span', string=re.compile(r'\d+ (day|week|month|hour)s? ago'))
                    if time_element:
                        date_text = time_element.get_text().strip()
                        estimated_date = self._parse_relative_date(date_text)
                        if estimated_date:
                            return {
                                'estimated_date': estimated_date,
                                'confidence': 'medium',
                                'source': 'LinkedIn'
                            }
                            
        except Exception as e:
            logger.warning(f"LinkedIn search error: {e}")
        
        return None
    
    def _search_indeed(self, search_query, company_name):
        """Search Indeed for job posting date"""
        try:
            # Indeed job search URL
            search_url = f"https://www.indeed.com/jobs?q={quote_plus(search_query)}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for job cards with posting dates
                job_cards = soup.find_all('div', {'class': 'job_seen_beacon'})
                
                for card in job_cards[:5]:
                    # Look for date posted
                    date_element = card.find('span', string=re.compile(r'\d+ (day|week|month|hour)s? ago'))
                    if date_element:
                        date_text = date_element.get_text().strip()
                        estimated_date = self._parse_relative_date(date_text)
                        if estimated_date:
                            return {
                                'estimated_date': estimated_date,
                                'confidence': 'medium',
                                'source': 'Indeed'
                            }
                            
        except Exception as e:
            logger.warning(f"Indeed search error: {e}")
        
        return None
    
    def _search_glassdoor(self, search_query, company_name):
        """Search Glassdoor for job posting date"""
        try:
            # Glassdoor job search URL
            search_url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={quote_plus(search_query)}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for job listings with dates
                job_listings = soup.find_all('li', {'class': 'react-job-listing'})
                
                for listing in job_listings[:5]:
                    date_element = listing.find('span', string=re.compile(r'\d+ (day|week|month|hour)s? ago'))
                    if date_element:
                        date_text = date_element.get_text().strip()
                        estimated_date = self._parse_relative_date(date_text)
                        if estimated_date:
                            return {
                                'estimated_date': estimated_date,
                                'confidence': 'medium',
                                'source': 'Glassdoor'
                            }
                            
        except Exception as e:
            logger.warning(f"Glassdoor search error: {e}")
        
        return None
    
    def _search_ziprecruiter(self, search_query, company_name):
        """Search ZipRecruiter for job posting date"""
        try:
            # ZipRecruiter job search URL
            search_url = f"https://www.ziprecruiter.com/candidate/search?search={quote_plus(search_query)}"
            
            response = self.session.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for job cards with dates
                job_cards = soup.find_all('article', {'class': 'job_result'})
                
                for card in job_cards[:5]:
                    date_element = card.find('time') or card.find('span', string=re.compile(r'\d+ (day|week|month|hour)s? ago'))
                    if date_element:
                        date_text = date_element.get_text().strip()
                        estimated_date = self._parse_relative_date(date_text)
                        if estimated_date:
                            return {
                                'estimated_date': estimated_date,
                                'confidence': 'medium',
                                'source': 'ZipRecruiter'
                            }
                            
        except Exception as e:
            logger.warning(f"ZipRecruiter search error: {e}")
        
        return None
    
    def _parse_relative_date(self, date_text):
        """Parse relative date strings like '2 days ago', '1 week ago'"""
        try:
            date_text = date_text.lower().strip()
            
            # Extract number and unit
            match = re.search(r'(\d+)\s+(day|week|month|hour)s?\s+ago', date_text)
            if not match:
                return None
                
            number = int(match.group(1))
            unit = match.group(2)
            
            now = datetime.now()
            
            if unit == 'hour':
                return now - timedelta(hours=number)
            elif unit == 'day':
                return now - timedelta(days=number)
            elif unit == 'week':
                return now - timedelta(weeks=number)
            elif unit == 'month':
                return now - timedelta(days=number * 30)  # Approximate
                
        except Exception as e:
            logger.warning(f"Error parsing relative date '{date_text}': {e}")
        
        return None
    
    def _estimate_based_on_patterns(self, job_title):
        """Estimate date based on job title patterns and common posting behaviors"""
        title_lower = job_title.lower()
        
        # Common patterns that indicate recent postings
        recent_indicators = [
            'urgent', 'immediate', 'asap', 'quick', 'fast',
            'new', 'recent', 'fresh', 'latest'
        ]
        
        # Patterns that might indicate older postings
        older_indicators = [
            'senior', 'lead', 'principal', 'staff', 'director',
            'vp', 'head', 'chief', 'manager'
        ]
        
        # Check for recent indicators
        has_recent = any(indicator in title_lower for indicator in recent_indicators)
        has_older = any(indicator in title_lower for indicator in older_indicators)
        
        now = datetime.now()
        
        if has_recent:
            # Recent posting: 1-7 days ago
            days_ago = random.randint(1, 7)
            estimated_date = now - timedelta(days=days_ago)
            confidence = 'low'
        elif has_older:
            # Older posting: 2-4 weeks ago
            days_ago = random.randint(14, 28)
            estimated_date = now - timedelta(days=days_ago)
            confidence = 'low'
        else:
            # Default: 1-2 weeks ago
            days_ago = random.randint(7, 14)
            estimated_date = now - timedelta(days=days_ago)
            confidence = 'very_low'
        
        return {
            'estimated_date': estimated_date,
            'confidence': confidence,
            'source': 'pattern_analysis',
            'date_range': f"{days_ago} days ago (estimated)"
        }
    
    def format_date_for_display(self, date_obj):
        """Format date for display in the UI"""
        if not date_obj:
            return "Unknown"
        
        if isinstance(date_obj, str):
            try:
                date_obj = datetime.fromisoformat(date_obj.replace('Z', '+00:00'))
            except:
                return date_obj
        
        now = datetime.now()
        diff = now - date_obj
        
        if diff.days == 0:
            return "Today"
        elif diff.days == 1:
            return "Yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''} ago"
        else:
            months = diff.days // 30
            return f"{months} month{'s' if months > 1 else ''} ago"
    
    def get_confidence_color(self, confidence):
        """Get color class for confidence level"""
        confidence_colors = {
            'high': 'success',
            'medium': 'warning', 
            'low': 'info',
            'very_low': 'secondary'
        }
        return confidence_colors.get(confidence, 'secondary')
    
    def enable_external_apis(self):
        """Enable external API calls for more accurate dates"""
        self.use_external_apis = True
        logger.info("External APIs enabled - slower but more accurate")
    
    def disable_external_apis(self):
        """Disable external API calls for faster performance"""
        self.use_external_apis = False
        logger.info("External APIs disabled - faster performance using pattern analysis")
    
    def clear_cache(self):
        """Clear the date estimation cache"""
        self.cache = {}
        if os.path.exists(self.cache_file):
            os.remove(self.cache_file)
        logger.info("Date estimation cache cleared") 