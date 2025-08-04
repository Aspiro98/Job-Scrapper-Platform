from flask import Flask, render_template, jsonify, request
import json
import os
import random
from datetime import datetime, timedelta
from scrapers.utils.ai_filter_processor import AIFilterProcessor
from scrapers.utils.job_date_estimator import JobDateEstimator
from application_system import application_system

app = Flask(__name__)

# Initialize AI processor
try:
    ai_processor = AIFilterProcessor()
    print("✅ AI Filter Processor initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize AI Filter Processor: {e}")
    ai_processor = None

# Initialize Job Date Estimator (optimized for performance)
try:
    date_estimator = JobDateEstimator(use_external_apis=False)  # Fast mode by default
    print("✅ Job Date Estimator initialized successfully (Fast Mode)")
    print("💡 Use date_estimator.enable_external_apis() for more accurate dates (slower)")
except Exception as e:
    print(f"❌ Failed to initialize Job Date Estimator: {e}")
    date_estimator = None

# Load resume data for application system
try:
    import json
    with open('my_resume_data.json', 'r') as f:
        resume_data = json.load(f)
    application_system.resume_data = resume_data
    print(f"✅ Resume data loaded: {len(resume_data.get('skills', []))} skills")
except Exception as e:
    print(f"⚠️ Could not load resume data: {e}")
    print("💡 Run: python use_my_resume.py to set up your resume")

def load_job_data():
    """Load and clean job data from scraped_data.json with simple processing"""
    try:
        with open('scraped_data.json', 'r') as f:
            data = json.load(f)
        
        jobs = []
        
        # Process all jobs with opening_title
        jobs_to_process = [job for job in data if 'opening_title' in job]
        
        print(f"🔄 Processing {len(jobs_to_process)} jobs with simple filtering...")
        
        for job in jobs_to_process:
            # Basic job data
            clean_job = {
                'title': job.get('opening_title', 'N/A'),
                'location': job.get('location', 'N/A'),
                'link': job.get('opening_link', 'N/A'),
                'source': job.get('source', 'N/A'),
                'id': job.get('id', 'N/A'),
                'company': job.get('company_name', extract_company_name(job.get('source', ''))),
                'description': job.get('description', '')
            }
            
            # Process posted date
            posted_date_info = process_posted_date(job, clean_job)
            clean_job.update(posted_date_info)
            
            # Debug: Print first few jobs to see posted dates
            if len(jobs) < 5:
                print(f"Job: {clean_job['title']} - Posted: {clean_job.get('posted_date_display', 'Unknown')}")
            
            # Smart processing for experience and roles
            clean_job.update({
                'experience_level': extract_experience_smart(clean_job['title']),
                'role_category': extract_role_smart(clean_job['title']),
                'company_normalized': clean_job['company'],
                'ai_processed': False
            })
            
            # Add display properties
            clean_job.update({
                'experience_display': get_experience_display_name(clean_job['experience_level']),
                'role_display': get_role_display_name(clean_job['role_category']),
                'experience_color': get_experience_color(clean_job['experience_level']),
                'role_color': get_role_color(clean_job['role_category'])
            })
            
            jobs.append(clean_job)
        
        print(f"🎉 Loaded {len(jobs)} jobs with simple processing")
        return jobs
    except FileNotFoundError:
        print("❌ scraped_data.json not found")
        return []
    except Exception as e:
        print(f"Error loading data: {e}")
        return []

def extract_experience_smart(title):
    """Extract experience level from job title using smart rules"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['senior', 'lead', 'principal', 'staff', 'sr']):
        return 'senior'
    elif any(word in title_lower for word in ['junior', 'entry', 'associate', 'graduate', 'jr']):
        return 'entry'
    elif any(word in title_lower for word in ['mid', 'intermediate', 'mid-level']):
        return 'mid'
    elif any(word in title_lower for word in ['director', 'vp', 'head', 'chief', 'manager']):
        return 'director'
    else:
        return 'unknown'

def extract_role_smart(title):
    """Extract role category from job title using smart rules"""
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['engineer', 'developer', 'programmer', 'devops', 'sre']):
        return 'engineering'
    elif any(word in title_lower for word in ['data', 'ml', 'ai', 'analyst', 'scientist']):
        return 'data_science'
    elif any(word in title_lower for word in ['product', 'program']):
        return 'product'
    elif any(word in title_lower for word in ['design', 'ux', 'ui']):
        return 'design'
    elif any(word in title_lower for word in ['sales', 'business development']):
        return 'sales'
    elif any(word in title_lower for word in ['marketing', 'growth', 'content']):
        return 'marketing'
    elif any(word in title_lower for word in ['operations', 'strategy']):
        return 'operations'
    elif any(word in title_lower for word in ['hr', 'recruiting', 'talent']):
        return 'hr'
    elif any(word in title_lower for word in ['finance', 'accounting', 'controller']):
        return 'finance'
    elif any(word in title_lower for word in ['legal', 'compliance', 'counsel']):
        return 'legal'
    else:
        return 'other'

def format_timestamp(timestamp):
    """Convert Unix timestamp to readable date"""
    if timestamp:
        try:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return 'N/A'
    return 'N/A'

def get_experience_display_name(level):
    """Get display name for experience level"""
    display_names = {
        'entry': 'Entry Level',
        'mid': 'Mid Level',
        'senior': 'Senior',
        'staff': 'Staff',
        'director': 'Director',
        'unknown': 'Unknown'
    }
    return display_names.get(level, 'Unknown')

def get_role_display_name(role):
    """Get display name for role category"""
    display_names = {
        'engineering': 'Engineering',
        'data_science': 'Data Science',
        'product': 'Product',
        'design': 'Design',
        'sales': 'Sales',
        'marketing': 'Marketing',
        'operations': 'Operations',
        'hr': 'HR',
        'finance': 'Finance',
        'legal': 'Legal',
        'other': 'Other'
    }
    return display_names.get(role, 'Other')

def get_experience_color(level):
    """Get color for experience level"""
    colors = {
        'entry': 'secondary',
        'mid': 'info',
        'senior': 'primary',
        'staff': 'warning',
        'director': 'danger',
        'unknown': 'dark'
    }
    return colors.get(level, 'light')

def get_role_color(role):
    """Get color for role category"""
    colors = {
        'engineering': 'primary',
        'data_science': 'info',
        'product': 'success',
        'design': 'warning',
        'sales': 'danger',
        'marketing': 'secondary',
        'operations': 'dark',
        'hr': 'secondary',
        'finance': 'success',
        'legal': 'warning',
        'other': 'dark'
    }
    return colors.get(role, 'light')

def process_posted_date(job, clean_job):
    """Process and estimate posted date for a job"""
    # Check if we already have posted date data
    if job.get('posted_date'):
        return {
            'posted_date': job.get('posted_date'),
            'posted_date_confidence': job.get('posted_date_confidence', 'unknown'),
            'posted_date_source': job.get('posted_date_source', 'scraped'),
            'posted_date_display': format_posted_date_display(job.get('posted_date')),
            'posted_date_color': get_posted_date_color(job.get('posted_date_confidence', 'unknown'))
        }
    
    # If no posted date, estimate it
    if date_estimator:
        try:
            result = date_estimator.estimate_job_date(
                clean_job['title'], 
                clean_job['company'], 
                clean_job['location']
            )
            
            # Ensure we have a valid result
            if result and result.get('estimated_date'):
                return {
                    'posted_date': result.get('estimated_date'),
                    'posted_date_confidence': result.get('confidence', 'low'),
                    'posted_date_source': result.get('source', 'estimated'),
                    'posted_date_display': date_estimator.format_date_for_display(result.get('estimated_date')),
                    'posted_date_color': date_estimator.get_confidence_color(result.get('confidence', 'low'))
                }
        except Exception as e:
            print(f"Error estimating date for job {clean_job['title']}: {e}")
    
    # Fallback - always provide a date estimate
    try:
        # Simple fallback based on job title patterns
        title_lower = clean_job['title'].lower()
        now = datetime.now()
        
        if any(word in title_lower for word in ['senior', 'lead', 'principal', 'staff', 'director', 'vp', 'head']):
            days_ago = random.randint(14, 28)
            estimated_date = now - timedelta(days=days_ago)
            confidence = 'low'
            source = 'pattern_fallback'
        elif any(word in title_lower for word in ['urgent', 'immediate', 'asap', 'new', 'recent']):
            days_ago = random.randint(1, 7)
            estimated_date = now - timedelta(days=days_ago)
            confidence = 'low'
            source = 'pattern_fallback'
        else:
            days_ago = random.randint(7, 14)
            estimated_date = now - timedelta(days=days_ago)
            confidence = 'very_low'
            source = 'pattern_fallback'
        
        return {
            'posted_date': estimated_date,
            'posted_date_confidence': confidence,
            'posted_date_source': source,
            'posted_date_display': format_posted_date_display(estimated_date),
            'posted_date_color': get_posted_date_color(confidence)
        }
    except Exception as e:
        print(f"Fallback error for job {clean_job['title']}: {e}")
        # Final fallback
        return {
            'posted_date': None,
            'posted_date_confidence': 'unknown',
            'posted_date_source': 'unknown',
            'posted_date_display': 'Unknown',
            'posted_date_color': 'secondary'
        }

def format_posted_date_display(date_obj):
    """Format posted date for display"""
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

def get_posted_date_color(confidence):
    """Get color class for posted date confidence"""
    confidence_colors = {
        'high': 'success',
        'medium': 'warning', 
        'low': 'info',
        'very_low': 'secondary',
        'unknown': 'secondary'
    }
    return confidence_colors.get(confidence, 'secondary')

def extract_company_name(source_url):
    """Extract company name from source URL"""
    if 'for=' in source_url:
        company = source_url.split('for=')[-1].split('&')[0]
        return company.replace('_', ' ').title()
    return 'Unknown'

@app.route('/')
def index():
    """Main page showing job listings"""
    jobs = load_job_data()
    
    # Debug: Check first few jobs for posted date data
    if jobs:
        print(f"🔍 Debug: First job posted date: {jobs[0].get('posted_date_display', 'MISSING')}")
        print(f"🔍 Debug: First job posted date color: {jobs[0].get('posted_date_color', 'MISSING')}")
    
    return render_template('index.html', jobs=jobs, total_jobs=len(jobs))

@app.route('/api/jobs')
def api_jobs():
    """API endpoint to get job data as JSON with optional filtering and pagination"""
    jobs = load_job_data()
    
    # Get filter parameters
    company = request.args.get('company')
    experience = request.args.get('experience')
    role = request.args.get('role')
    country = request.args.get('country')
    state = request.args.get('state')
    search = request.args.get('search')
    
    # Get pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    
    # Apply filters
    if company:
        jobs = [job for job in jobs if company.lower() in job.get('company_normalized', job['company']).lower()]
    if experience:
        jobs = [job for job in jobs if job['experience_level'] == experience]
    if role:
        jobs = [job for job in jobs if job['role_category'] == role]
    if country:
        # Simple location filtering using string matching
        if country.lower() == 'united states':
            # For US, match common US patterns but exclude non-US locations
            us_patterns = ['ca', 'ny', 'tx', 'wa', 'fl', 'il', 'ma', 'pa', 'co', 'ga', 'nc', 'va', 
                          'california', 'new york', 'texas', 'washington', 'florida', 'illinois', 
                          'massachusetts', 'pennsylvania', 'colorado', 'georgia', 'north carolina', 'virginia',
                          'sf', 'la', 'seattle', 'austin', 'chicago', 'boston', 'atlanta', 'denver',
                          'san francisco', 'los angeles']
            non_us_patterns = ['mexico', 'paris', 'london', 'dublin', 'toronto', 'singapore', 'tokyo', 'bangalore', 'bengaluru']
            
            def is_us_location(location):
                location_lower = location.lower()
                # Check if it contains US patterns
                has_us_pattern = any(pattern in location_lower for pattern in us_patterns)
                # Check if it contains non-US patterns (exclude these)
                has_non_us_pattern = any(pattern in location_lower for pattern in non_us_patterns)
                return has_us_pattern and not has_non_us_pattern
            
            jobs = [job for job in jobs if is_us_location(job['location'])]
        elif country.lower() == 'remote':
            jobs = [job for job in jobs if 'remote' in job['location'].lower()]
        elif country.lower() == 'mexico':
            jobs = [job for job in jobs if 'mexico' in job['location'].lower()]
        elif country.lower() == 'france':
            jobs = [job for job in jobs if 'paris' in job['location'].lower()]
        elif country.lower() == 'united kingdom':
            jobs = [job for job in jobs if any(pattern in job['location'].lower() for pattern in ['london', 'uk', 'england'])]
        elif country.lower() == 'canada':
            jobs = [job for job in jobs if 'toronto' in job['location'].lower()]
        elif country.lower() == 'ireland':
            jobs = [job for job in jobs if 'dublin' in job['location'].lower()]
        elif country.lower() == 'japan':
            jobs = [job for job in jobs if 'tokyo' in job['location'].lower()]
        elif country.lower() == 'india':
            jobs = [job for job in jobs if any(pattern in job['location'].lower() for pattern in ['bangalore', 'bengaluru'])]
        else:
            # For other countries, do simple string matching
            jobs = [job for job in jobs if country.lower() in job['location'].lower()]
    if search:
        search_lower = search.lower()
        jobs = [job for job in jobs if 
                search_lower in job['title'].lower() or 
                search_lower in job.get('company_normalized', job['company']).lower() or 
                search_lower in job['location'].lower()]
    
    # Calculate pagination
    total_jobs = len(jobs)
    total_pages = (total_jobs + per_page - 1) // per_page
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Get jobs for current page
    paginated_jobs = jobs[start_idx:end_idx]
    
    # Add random sorting to mix companies (only if no other sorting is applied)
    if not any([company, experience, role, country, state, search]):
        import random
        random.shuffle(paginated_jobs)
    
    return jsonify({
        'jobs': paginated_jobs,
        'total': total_jobs,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'has_next': page < total_pages,
        'has_prev': page > 1,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/refresh')
def refresh_data():
    """Refresh the job data"""
    jobs = load_job_data()
    return jsonify({
        'success': True,
        'total_jobs': len(jobs),
        'message': f'Refreshed data - found {len(jobs)} jobs'
    })

@app.route('/scrape')
def scrape_new_jobs():
    """Trigger a new scraping job"""
    import subprocess
    import threading
    import os
    
    def run_scraper():
        try:
            print("🔄 Starting background scraping...")
            # Run scraper with timeout (30 minutes max)
            result = subprocess.run(
                ['python', 'run_multi_company_spider.py'], 
                capture_output=True, 
                text=True, 
                timeout=1800  # 30 minutes timeout
            )
            if result.returncode == 0:
                print("✅ Scraping completed successfully!")
            else:
                print(f"❌ Scraping failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⏰ Scraping timed out after 30 minutes")
        except Exception as e:
            print(f"❌ Scraping error: {e}")
    
    # Check if scraping is already running
    if hasattr(scrape_new_jobs, 'is_running') and scrape_new_jobs.is_running:
        return jsonify({
            'success': False,
            'message': 'Scraping is already running. Please wait for it to complete.',
            'status': 'already_running'
        })
    
    # Mark scraping as running
    scrape_new_jobs.is_running = True
    
    # Run scraper in background thread
    thread = threading.Thread(target=run_scraper)
    thread.daemon = True  # Thread will stop when main app stops
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Scraping started! This will take 15-30 minutes. You can check back later.',
        'status': 'started',
        'estimated_time': '15-30 minutes'
    })

@app.route('/scrape-status')
def scrape_status():
    """Check if scraping is running"""
    is_running = hasattr(scrape_new_jobs, 'is_running') and scrape_new_jobs.is_running
    return jsonify({
        'is_running': is_running,
        'message': 'Scraping in progress' if is_running else 'No scraping running'
    })

@app.route('/api/filters')
def api_filters():
    """Get available filter options"""
    jobs = load_job_data()
    
    # Simple filter generation
    companies = sorted(list(set(job.get('company_normalized', job['company']) for job in jobs)))
    experience_levels = sorted(list(set(job['experience_level'] for job in jobs)))
    role_categories = sorted(list(set(job['role_category'] for job in jobs)))
    
    # Simple location filters based on location strings
    countries = set()
    for job in jobs:
        location = job['location'].lower()
        if 'remote' in location:
            countries.add('remote')
        elif any(pattern in location for pattern in ['nyc', 'sf', 'la', 'seattle', 'austin', 'chicago', 'boston', 'atlanta', 'denver',
                                                    'ca', 'ny', 'tx', 'wa', 'fl', 'il', 'ma', 'pa', 'co', 'ga', 'nc', 'va',
                                                    'california', 'new york', 'texas', 'washington', 'florida', 'illinois', 
                                                    'massachusetts', 'pennsylvania', 'colorado', 'georgia', 'north carolina', 'virginia',
                                                    'san francisco', 'los angeles', 'us-', 'united states']):
            countries.add('united states')
        elif any(pattern in location for pattern in ['london', 'uk', 'england']):
            countries.add('united kingdom')
        elif any(pattern in location for pattern in ['toronto', 'canada']):
            countries.add('canada')
        elif any(pattern in location for pattern in ['paris', 'france']):
            countries.add('france')
        elif any(pattern in location for pattern in ['mexico', 'mexico city']):
            countries.add('mexico')
        elif any(pattern in location for pattern in ['singapore']):
            countries.add('singapore')
        elif any(pattern in location for pattern in ['dublin', 'ireland']):
            countries.add('ireland')
        elif any(pattern in location for pattern in ['tokyo', 'japan']):
            countries.add('japan')
        elif any(pattern in location for pattern in ['bangalore', 'bengaluru', 'india']):
            countries.add('india')
        else:
            countries.add('other')
    
    location_filters = {country: {'states': [], 'cities': []} for country in sorted(countries)}
    
    return jsonify({
        'companies': companies,
        'experience_levels': experience_levels,
        'role_categories': role_categories,
        'location_filters': location_filters
    })

@app.route('/api/location/<country>')
def api_location_details(country):
    """Get states and cities for a specific country"""
    jobs = load_job_data()
    
    # Simple location details based on location strings
    states = set()
    cities = set()
    
    for job in jobs:
        location = job['location'].lower()
        
        if country.lower() == 'united states':
            # Extract US states and cities
            us_states = {
                'ca': 'california', 'ny': 'new york', 'tx': 'texas', 'wa': 'washington',
                'fl': 'florida', 'il': 'illinois', 'ma': 'massachusetts', 'pa': 'pennsylvania',
                'co': 'colorado', 'ga': 'georgia', 'nc': 'north carolina', 'va': 'virginia'
            }
            us_cities = {
                'sf': 'san francisco', 'nyc': 'new york', 'la': 'los angeles',
                'seattle': 'seattle', 'austin': 'austin', 'chicago': 'chicago',
                'boston': 'boston', 'atlanta': 'atlanta', 'denver': 'denver'
            }
            
            for state_code, state_name in us_states.items():
                if state_code in location or state_name in location:
                    states.add(state_name)
            
            for city_code, city_name in us_cities.items():
                if city_code in location or city_name in location:
                    cities.add(city_name)
    
    return jsonify({
        'country': country,
        'states': sorted(list(states)),
        'cities': sorted(list(cities))
    })

@app.route('/api/grouped')
def api_grouped():
    """Get jobs grouped by company"""
    jobs = load_job_data()
    
    # Group by company
    grouped = {}
    for job in jobs:
        company = job['company']
        if company not in grouped:
            grouped[company] = []
        grouped[company].append(job)
    
    # Sort companies by number of jobs
    sorted_companies = sorted(grouped.items(), key=lambda x: len(x[1]), reverse=True)
    
    return jsonify({
        'grouped': dict(sorted_companies),
        'total_companies': len(grouped),
        'total_jobs': len(jobs)
    })

# Application System Endpoints
@app.route('/api/select-jobs', methods=['POST'])
def select_jobs():
    """Select jobs for application"""
    try:
        data = request.get_json()
        job_ids = data.get('job_ids', [])
        
        print(f"🎯 [API] Selecting {len(job_ids)} jobs for application")
        print(f"📋 [API] Job IDs: {job_ids}")
        
        success = application_system.select_jobs(job_ids)
        
        print(f"✅ [API] Selection result: {success}")
        
        return jsonify({
            'success': success,
            'selected_count': len(application_system.selected_jobs),
            'message': f'Selected {len(application_system.selected_jobs)} jobs for application'
        })
    except Exception as e:
        print(f"❌ [API] Error selecting jobs: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/apply-all', methods=['POST'])
def apply_all_jobs():
    """Process applications for all selected jobs"""
    import threading
    
    print(f"🚀 [API] Starting application processing for {len(application_system.selected_jobs)} jobs")
    
    def process_in_background():
        try:
            print(f"🔄 [Background] Starting application processing...")
            results = application_system.process_applications()
            print(f"✅ [Background] Application processing completed: {results['processed']}/{results['total_jobs']} jobs")
        except Exception as e:
            print(f"❌ [Background] Application processing error: {e}")
    
    # Check if already processing
    if application_system.get_processing_status()['is_processing']:
        print(f"⚠️ [API] Application processing already running")
        return jsonify({
            'success': False,
            'message': 'Application processing is already running'
        })
    
    # Start processing in background
    thread = threading.Thread(target=process_in_background)
    thread.daemon = True
    thread.start()
    
    print(f"✅ [API] Background processing started")
    
    return jsonify({
        'success': True,
        'message': f'Started processing {len(application_system.selected_jobs)} applications',
        'status': 'processing'
    })

@app.route('/api/application-status')
def application_status():
    """Get application processing status"""
    status = application_system.get_processing_status()
    return jsonify(status)

@app.route('/api/applications')
def get_applications():
    """Get prepared applications"""
    applications = []
    for job_id, status in application_system.processing_status.items():
        if status.get('status') == 'completed':
            applications.append(status.get('application'))
    
    return jsonify({
        'applications': applications,
        'total': len(applications)
    })

@app.route('/api/date-estimation/mode', methods=['GET', 'POST'])
def date_estimation_mode():
    """Get or set date estimation mode"""
    if request.method == 'POST':
        mode = request.json.get('mode', 'fast')
        if date_estimator:
            if mode == 'accurate':
                date_estimator.enable_external_apis()
                return jsonify({'status': 'success', 'mode': 'accurate', 'message': 'External APIs enabled for more accurate dates'})
            else:
                date_estimator.disable_external_apis()
                return jsonify({'status': 'success', 'mode': 'fast', 'message': 'Fast mode enabled using pattern analysis'})
        else:
            return jsonify({'status': 'error', 'message': 'Date estimator not available'})
    else:
        if date_estimator:
            mode = 'accurate' if date_estimator.use_external_apis else 'fast'
            return jsonify({'mode': mode})
        else:
            return jsonify({'mode': 'unavailable'})

@app.route('/api/date-estimation/clear-cache', methods=['POST'])
def clear_date_cache():
    """Clear the date estimation cache"""
    if date_estimator:
        date_estimator.clear_cache()
        return jsonify({'status': 'success', 'message': 'Date estimation cache cleared'})
    else:
        return jsonify({'status': 'error', 'message': 'Date estimator not available'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 