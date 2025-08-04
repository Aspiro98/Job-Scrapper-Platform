# Posted Date Feature

## Overview

The Job Scraper Platform now includes an intelligent **Posted Date** column that estimates when jobs were posted by searching multiple job platforms. Since Greenhouse doesn't provide posting dates, this feature cross-references jobs on platforms like LinkedIn, Indeed, Glassdoor, and ZipRecruiter to provide estimated posting dates.

## Features

### 🎯 Smart Date Estimation
- **Multi-Platform Search**: Searches LinkedIn, Indeed, Glassdoor, and ZipRecruiter
- **Pattern Analysis**: Uses job title patterns to estimate dates when platform data isn't available
- **Confidence Levels**: Provides confidence indicators (High, Medium, Low, Very Low)
- **Source Attribution**: Shows which platform provided the date information

### 🎨 Visual Indicators
- **Color-Coded Confidence**: 
  - 🟢 Green: High confidence
  - 🟡 Yellow: Medium confidence  
  - 🔵 Blue: Low confidence
  - ⚪ Gray: Very low confidence/Unknown
- **Hover Tooltips**: Show the data source on hover
- **Relative Dates**: Displays dates as "2 days ago", "1 week ago", etc.

## Legal Compliance

### ✅ Legal Implementation
- **Public Data Only**: Only scrapes publicly available job listings
- **Rate Limiting**: Implements 2-second delays between requests
- **Respectful Headers**: Uses proper User-Agent headers
- **Terms Compliance**: Focuses on platforms that allow scraping
- **Data Attribution**: Clearly indicates data sources

### 🛡️ Safety Measures
- **Error Handling**: Graceful fallbacks when platforms are unavailable
- **Timeout Protection**: 10-second timeouts for all requests
- **Pattern Fallback**: Uses job title analysis when external data isn't available

## Technical Implementation

### Core Components

1. **JobDateEstimator Class** (`scrapers/utils/job_date_estimator.py`)
   - Handles all date estimation logic
   - Manages rate limiting and error handling
   - Provides confidence scoring

2. **Updated Data Model** (`scrapers/items.py`)
   - Added `posted_date`, `posted_date_confidence`, `posted_date_source` fields

3. **Enhanced UI** (`templates/index.html`)
   - New "Posted Date" column with visual indicators
   - Color-coded confidence levels
   - Hover tooltips for data sources

### Data Flow

1. **Job Scraping**: Jobs are scraped from Greenhouse/Lever
2. **Date Estimation**: For each job, search multiple platforms for posting dates
3. **Pattern Analysis**: If no external data found, analyze job title patterns
4. **Display**: Show estimated dates with confidence indicators

## Usage

### Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export HASHIDS_SALT="your_salt_here"

# Start the application
python app.py

# Open browser to http://localhost:5000
```

### Testing the Feature

```bash
# Test date estimation functionality
python test_date_estimation.py
```

## Configuration

### Rate Limiting
Adjust the request delay in `JobDateEstimator`:
```python
self.request_delay = 2  # seconds between requests
```

### Platform Selection
Modify the platforms list in `estimate_job_date()`:
```python
platforms = [
    self._search_linkedin,
    self._search_indeed,
    self._search_glassdoor,
    self._search_ziprecruiter
]
```

## API Endpoints

The posted date information is included in all existing API endpoints:

- `GET /api/jobs` - Returns jobs with posted date data
- `GET /api/grouped` - Returns grouped jobs with posted dates
- `GET /` - Main dashboard with posted date column

### Sample API Response
```json
{
  "title": "Senior Software Engineer",
  "company": "Google",
  "posted_date": "2024-01-15T10:30:00",
  "posted_date_confidence": "medium",
  "posted_date_source": "LinkedIn",
  "posted_date_display": "3 days ago",
  "posted_date_color": "warning"
}
```

## Troubleshooting

### Common Issues

1. **"Unknown" Posted Dates**
   - Check internet connectivity
   - Verify rate limiting isn't too aggressive
   - Check if target platforms are accessible

2. **Slow Date Estimation**
   - Increase `request_delay` for better rate limiting
   - Consider caching results for repeated searches

3. **Platform Errors**
   - Check platform availability
   - Verify User-Agent headers are acceptable
   - Review platform terms of service

### Debug Mode

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Future Enhancements

### Planned Features
- **Caching System**: Cache date estimates to reduce API calls
- **Machine Learning**: Improve pattern-based estimation accuracy
- **More Platforms**: Add support for additional job boards
- **Historical Data**: Track posting date trends over time

### Performance Optimizations
- **Batch Processing**: Process multiple jobs simultaneously
- **Async Requests**: Use async/await for better performance
- **Database Storage**: Store estimated dates in database

## Contributing

When contributing to the posted date feature:

1. **Respect Rate Limits**: Always implement proper delays
2. **Handle Errors**: Provide graceful fallbacks
3. **Update Documentation**: Keep this README current
4. **Test Thoroughly**: Use the test script before submitting

## Legal Notice

This feature is designed for educational and personal use. Users are responsible for:
- Complying with platform terms of service
- Respecting rate limits and robots.txt files
- Using data responsibly and ethically
- Not overwhelming target platforms with requests 