import re
from typing import Dict, Tuple

# Experience level patterns
EXPERIENCE_PATTERNS = {
    'intern': ['intern', 'internship', 'student', 'co-op', 'coop'],
    'entry': ['entry', 'junior', 'jr', 'associate', 'assistant', 'trainee', 'graduate', 'new grad'],
    'mid': ['mid', 'intermediate', 'experienced', 'professional'],
    'senior': ['senior', 'sr', 'lead', 'principal', 'staff'],
    'expert': ['expert', 'architect', 'director', 'head', 'chief', 'vp', 'vice president', 'cto', 'ceo']
}

# Role category patterns
ROLE_CATEGORIES = {
    'engineering': [
        'software engineer', 'developer', 'programmer', 'engineer', 'swe', 'full stack', 'frontend', 'backend',
        'devops', 'site reliability', 'sre', 'data engineer', 'ml engineer', 'ai engineer', 'systems engineer',
        'infrastructure', 'platform', 'mobile', 'ios', 'android', 'web', 'cloud', 'security engineer'
    ],
    'data_science': [
        'data scientist', 'machine learning', 'ml', 'ai', 'artificial intelligence', 'analytics', 'statistician',
        'research scientist', 'quantitative', 'algorithm', 'deep learning', 'nlp', 'computer vision'
    ],
    'product': [
        'product manager', 'product owner', 'program manager', 'project manager', 'technical product',
        'product marketing', 'growth', 'strategy'
    ],
    'design': [
        'designer', 'ux', 'ui', 'user experience', 'user interface', 'visual designer', 'interaction designer',
        'product designer', 'graphic designer', 'creative'
    ],
    'marketing': [
        'marketing', 'brand', 'communications', 'pr', 'public relations', 'content', 'social media',
        'digital marketing', 'growth marketing', 'performance marketing'
    ],
    'sales': [
        'sales', 'account executive', 'business development', 'partnership', 'revenue', 'customer success',
        'account manager', 'sales development', 'sdr', 'bdr'
    ],
    'operations': [
        'operations', 'business operations', 'strategy', 'analyst', 'business analyst', 'data analyst',
        'operations manager', 'process', 'optimization'
    ],
    'finance': [
        'finance', 'financial', 'accounting', 'controller', 'treasurer', 'investment', 'banking',
        'financial analyst', 'accountant', 'auditor'
    ],
    'hr': [
        'hr', 'human resources', 'recruiter', 'talent', 'people', 'benefits', 'compensation',
        'recruitment', 'hiring', 'talent acquisition'
    ],
    'legal': [
        'legal', 'lawyer', 'attorney', 'counsel', 'compliance', 'regulatory', 'paralegal',
        'legal counsel', 'general counsel'
    ],
    'support': [
        'support', 'customer service', 'help desk', 'technical support', 'customer care',
        'support engineer', 'customer success'
    ],
    'research': [
        'research', 'scientist', 'phd', 'postdoc', 'research engineer', 'research scientist',
        'academic', 'university'
    ],
    'management': [
        'manager', 'director', 'head', 'chief', 'vp', 'vice president', 'cto', 'ceo', 'cfo',
        'lead', 'principal', 'staff'
    ]
}

def extract_experience_level(job_title: str) -> str:
    """
    Extract experience level from job title
    Returns: 'intern', 'entry', 'mid', 'senior', 'expert', or 'unknown'
    """
    if not job_title:
        return 'unknown'
    
    title_lower = job_title.lower()
    
    for level, patterns in EXPERIENCE_PATTERNS.items():
        for pattern in patterns:
            if pattern in title_lower:
                return level
    
    return 'unknown'

def extract_role_category(job_title: str) -> str:
    """
    Extract role category from job title
    Returns: category name or 'other'
    """
    if not job_title:
        return 'other'
    
    title_lower = job_title.lower()
    
    for category, patterns in ROLE_CATEGORIES.items():
        for pattern in patterns:
            if pattern in title_lower:
                return category
    
    return 'other'

def analyze_job_title(job_title: str) -> Dict[str, str]:
    """
    Analyze job title and return experience level and role category
    """
    return {
        'experience_level': extract_experience_level(job_title),
        'role_category': extract_role_category(job_title)
    }

def get_experience_level_display(level: str) -> str:
    """
    Get display name for experience level
    """
    display_names = {
        'intern': 'Intern',
        'entry': 'Entry Level',
        'mid': 'Mid Level',
        'senior': 'Senior',
        'expert': 'Expert/Leadership',
        'unknown': 'Unknown'
    }
    return display_names.get(level, 'Unknown')

def get_role_category_display(category: str) -> str:
    """
    Get display name for role category
    """
    display_names = {
        'engineering': 'Engineering',
        'data_science': 'Data Science & AI',
        'product': 'Product & Program Management',
        'design': 'Design & UX',
        'marketing': 'Marketing & Communications',
        'sales': 'Sales & Business Development',
        'operations': 'Operations & Strategy',
        'finance': 'Finance & Accounting',
        'hr': 'Human Resources',
        'legal': 'Legal & Compliance',
        'support': 'Customer Support',
        'research': 'Research & Academia',
        'management': 'Management & Leadership',
        'other': 'Other'
    }
    return display_names.get(category, 'Other')

def get_experience_level_color(level: str) -> str:
    """
    Get color class for experience level
    """
    colors = {
        'intern': 'info',
        'entry': 'success',
        'mid': 'primary',
        'senior': 'warning',
        'expert': 'danger',
        'unknown': 'secondary'
    }
    return colors.get(level, 'secondary')

def get_role_category_color(category: str) -> str:
    """
    Get color class for role category
    """
    colors = {
        'engineering': 'primary',
        'data_science': 'info',
        'product': 'success',
        'design': 'warning',
        'marketing': 'danger',
        'sales': 'dark',
        'operations': 'secondary',
        'finance': 'success',
        'hr': 'info',
        'legal': 'dark',
        'support': 'secondary',
        'research': 'info',
        'management': 'danger',
        'other': 'light'
    }
    return colors.get(category, 'light') 