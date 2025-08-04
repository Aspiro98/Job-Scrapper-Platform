# Job Scraper Platform 🚀

A comprehensive job scraping and automation platform that scrapes job listings from multiple companies and provides intelligent job application automation.

## ✨ Features

### 🔍 **Multi-Company Job Scraping**
- **Greenhouse.io Integration**: Scrapes jobs from 30+ companies using Greenhouse boards
- **Lever Integration**: Supports Lever job boards
- **Real-time Updates**: Automatic job data refresh
- **Smart Filtering**: Filter by company, experience level, role, location, and more

### 🤖 **AI-Powered Job Analysis**
- **Job Description Analysis**: Uses Groq AI to analyze job requirements
- **Resume Tailoring**: Automatically tailors your resume for each job
- **Cover Letter Generation**: AI-generated personalized cover letters
- **Skill Matching**: Identifies matching and missing skills

### 🎯 **Intelligent Automation**
- **Form Auto-Fill**: Automatically fills job application forms
- **Multi-Browser Support**: Works with Chrome and Firefox
- **Smart Field Detection**: Automatically detects form fields
- **Batch Processing**: Apply to multiple jobs simultaneously

### 📊 **Advanced Web Interface**
- **Real-time Dashboard**: Live job statistics and updates
- **Advanced Filtering**: Filter by company, experience, role, location
- **Smart Sorting**: Sort by any column with visual indicators
- **Pagination**: Handle large datasets efficiently
- **Fast Mode**: Pattern-based date estimation (222x faster)
- **Accurate Mode**: External API-based date estimation

### 🚀 **Performance Optimizations**
- **Dual-Mode System**: Fast mode (0.009s/job) vs Accurate mode (2-10s/job)
- **Intelligent Caching**: Automatic caching of job data and analysis
- **Background Processing**: Non-blocking job processing
- **Memory Optimization**: Efficient data handling

## 🏗️ Architecture

```
job-scrapper-platform/
├── app.py                          # Main Flask web application
├── application_system.py           # Job application automation system
├── form_automation.py             # Web form automation engine
├── scrapers/                      # Scrapy spiders and utilities
│   ├── spiders/                   # Job scraping spiders
│   └── utils/                     # Scraping utilities
├── templates/                     # Web interface templates
├── requirements.txt               # Python dependencies
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Chrome or Firefox browser
- Groq API key (optional, for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/job-scrapper-platform.git
   cd job-scrapper-platform
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your resume data**
   ```bash
   python setup_resume.py
   ```

4. **Configure Groq API (optional)**
   ```bash
   python setup_groq.py
   ```

5. **Start the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   ```
   http://localhost:5000
   ```

## 📋 Usage Guide

### 1. **Scraping Jobs**
- Click "Scrape New Jobs" to fetch latest job listings
- Jobs are automatically categorized by company, experience, and role
- Real-time progress tracking

### 2. **Filtering and Browsing**
- Use the filter dropdowns to find specific jobs
- Search by job title, company, or location
- Sort by any column (title, company, experience, posted date)
- Use "Shuffle Jobs" to mix companies on the first page

### 3. **Job Application Automation**
- Select jobs using checkboxes
- Click "Apply for X Jobs" to start automation
- System will:
  - Analyze job descriptions with AI
  - Tailor your resume for each job
  - Generate personalized cover letters
  - Automatically fill application forms

### 4. **Performance Modes**
- **Fast Mode** (Default): Pattern-based date estimation (~0.009s/job)
- **Accurate Mode**: External API-based dates (~2-10s/job)
- Toggle between modes using the button in the interface

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Resume Setup
Run `python setup_resume.py` to configure your resume data:
- Personal information
- Skills and experience
- Education and certifications
- Work history

## 📊 Supported Companies

The platform currently scrapes jobs from:
- **Airbnb** - Engineering, Data Science, Product
- **Anduril Industries** - Aerospace, Defense, Robotics
- **Applied Intuition** - Autonomous Vehicles, AI
- **Asana** - Productivity, Collaboration
- **Axon** - Public Safety Technology
- **Braze** - Customer Engagement Platform
- **Calendly** - Scheduling Automation
- **Checkr** - Background Check Platform
- **Cloudflare** - Web Security, CDN
- **Coinbase** - Cryptocurrency Exchange
- **Databricks** - Data Engineering, AI
- **Dropbox** - File Storage, Collaboration
- **Duolingo** - Language Learning
- **Earnin** - Financial Services
- **Fastly** - Edge Computing Platform
- **Figma** - Design Collaboration
- **Flexport** - Supply Chain Management
- **Hazel** - Healthcare Technology
- **Headway** - Mental Health Platform
- **Honor** - Home Care Services
- And many more...

## 🛠️ Development

### Project Structure
```
├── app.py                          # Flask web application
├── application_system.py           # Job application automation
├── form_automation.py             # Web form automation
├── job_description_analyzer.py    # AI job analysis
├── resume_parser.py               # Resume parsing utilities
├── scrapers/                      # Scrapy spiders
│   ├── spiders/
│   │   ├── greenhouse_jobs_outline_spider.py
│   │   ├── greenhouse_job_departments_spider.py
│   │   └── lever_jobs_outline_spider.py
│   └── utils/
│       ├── ai_filter_processor.py
│       ├── job_analyzer.py
│       ├── job_date_estimator.py
│       └── scraper_util.py
├── templates/
│   └── index.html                 # Main web interface
└── requirements.txt               # Dependencies
```

### Running Tests
```bash
# Test job scraping
python test_single_spider.py

# Test automation
python test_automation.py

# Test AI analysis
python test_ai_analysis.py

# Test complete system
python test_complete_system.py
```

## 🔒 Security & Privacy

- **No Data Storage**: Job data is not permanently stored
- **Local Processing**: All AI analysis happens locally
- **Secure API Keys**: API keys are stored securely
- **Privacy First**: No personal data is shared

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:
1. Check the [Issues](https://github.com/yourusername/job-scrapper-platform/issues) page
2. Create a new issue with detailed information
3. Include error logs and system information

## 🚀 Roadmap

- [ ] Support for more job boards (LinkedIn, Indeed, Glassdoor)
- [ ] Advanced AI-powered job matching
- [ ] Resume optimization suggestions
- [ ] Interview preparation tools
- [ ] Job application tracking dashboard
- [ ] Email notification system
- [ ] Mobile app support

## 📊 Performance Metrics

- **Job Scraping**: 1000+ jobs per minute
- **AI Analysis**: 2-5 seconds per job
- **Form Automation**: 30-60 seconds per application
- **Web Interface**: Sub-second response times

---

**Made with ❤️ for job seekers everywhere**

*This project is for educational and personal use. Please respect the terms of service of job boards and companies.* 