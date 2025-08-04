# 🤖 AI-Powered Job Filtering System

This project now uses **Groq's Llama3-8b-8192 model** for intelligent job filtering and categorization, replacing the previous regex-based approach.

## 🚀 Features

### **AI-Powered Filters:**

1. **📍 Location Filter**
   - Parses complex location strings: "San Francisco, CA | Seattle, WA"
   - Handles multiple locations per job
   - Normalizes country/state/city names
   - Supports remote work detection

2. **👨‍💼 Experience Level Filter**
   - Extracts experience from job titles and descriptions
   - Categories: Entry, Mid, Senior, Staff, Director
   - Handles variations: "Senior", "Lead", "Principal", "Junior"

3. **🎯 Role Category Filter**
   - Categorizes jobs into roles: Engineering, Data Science, Product, etc.
   - Handles ambiguous titles
   - Extracts from job descriptions, not just titles

4. **🏢 Company Filter**
   - Normalizes company names: "Anthropic PBC" → "Anthropic"
   - Handles subsidiaries and variations
   - Groups related companies

## 🛠️ Setup

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Set Up Groq API Key**

**Option A: Store in Code (Recommended)**
Edit `scrapers/utils/ai_filter_processor.py` and replace the API key on line 11:
```python
self.api_key = api_key or os.getenv('GROQ_API_KEY') or "YOUR_NEW_API_KEY_HERE"
```

**Option B: Environment Variable**
```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

**Get your API key from:** https://console.groq.com/

### **3. Test the AI Processor**
```bash
python test_ai_processor.py
```

### **4. Run the Application**
```bash
python app.py
```

## 📊 How It Works

### **Job Processing Flow:**
1. **Load Raw Job Data** from `scraped_data.json`
2. **AI Processing** for each job:
   - Parse location → structured location info
   - Extract experience level from title/description
   - Categorize role from title/description
   - Normalize company name
3. **Generate Filters** from processed data
4. **Apply Filters** using AI-processed information

### **Example AI Processing:**

**Input Job:**
```json
{
  "title": "Senior Software Engineer",
  "location": "San Francisco, CA | Seattle, WA",
  "company": "Anthropic PBC",
  "description": "5+ years experience required..."
}
```

**AI Output:**
```json
{
  "experience_level": "senior",
  "role_category": "engineering",
  "company_normalized": "Anthropic",
  "location_info": {
    "country": "united states",
    "states": ["california", "washington"],
    "cities": ["san francisco", "seattle"],
    "is_remote": false
  }
}
```

## 🎯 Benefits

### **✅ Accuracy**
- **Location**: Handles complex multi-location strings
- **Experience**: "Senior Software Engineer" → "senior"
- **Roles**: "Product Manager" → "product"
- **Companies**: "Anthropic PBC" → "Anthropic"

### **🔄 Flexibility**
- Handles new job titles and formats
- Adapts to different company naming conventions
- Processes unstructured job descriptions

### **📈 Better UX**
- More accurate filtering
- Smarter categorization
- Hierarchical location filtering

## 💰 Cost Analysis

### **Groq Pricing:**
- **Llama3-8b-8192**: ~$0.05 per 1M input tokens
- **Typical job processing**: ~100-200 tokens per job
- **Cost per job**: ~$0.000005-0.00001

### **Example Costs:**
- **1,000 jobs**: ~$0.005-0.01
- **10,000 jobs**: ~$0.05-0.10
- **100,000 jobs**: ~$0.50-1.00

## 🔧 Configuration

### **Model Settings:**
```python
# In ai_filter_processor.py
self.model = "llama3-8b-8192"  # Fast and cost-effective
temperature = 0.1  # Low temperature for consistent results
```

### **Fallback Mode:**
If AI processing fails, the system falls back to basic filtering:
- Location: Simple string matching
- Experience: "unknown"
- Role: "other"
- Company: Original name

## 🧪 Testing

### **Test Individual Components:**
```bash
python test_ai_processor.py
```

### **Test with Real Data:**
1. Run the scraper to get job data
2. Start the Flask app
3. Check the UI for AI-processed filters

## 🚨 Troubleshooting

### **Common Issues:**

1. **"Invalid API Key"**
   - Check the API key in `scrapers/utils/ai_filter_processor.py`
   - Get a new API key from https://console.groq.com/
   - Update the key in the code file

2. **AI Processing Fails**
   - Check API key validity
   - Verify internet connection
   - Check Groq service status

3. **Slow Processing**
   - AI processing adds ~1-2 seconds per job
   - Consider caching processed results
   - Use batch processing for large datasets

### **Performance Tips:**
- Process jobs in batches
- Cache AI results
- Use fallback mode for testing

## 🔄 Migration from Regex

### **Removed Files:**
- `scrapers/utils/location_parser.py` (replaced by AI)
- `test_location_parser.py` (replaced by `test_ai_processor.py`)

### **Updated Files:**
- `app.py` (uses AI processor)
- `requirements.txt` (added groq dependency)

## 🎉 Success!

The AI-powered filtering system provides:
- **Better accuracy** than regex patterns
- **More flexible** handling of edge cases
- **Future-proof** architecture
- **Cost-effective** processing

Your job filtering is now powered by AI! 🚀 