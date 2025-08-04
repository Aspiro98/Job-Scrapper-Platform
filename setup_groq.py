#!/usr/bin/env python3
"""
Setup Groq API Key for Job Analysis
Configure Groq API key for AI-powered job description analysis
"""

import os
import json
from pathlib import Path

def setup_groq_api_key():
    """Set up Groq API key for the job analysis system"""
    
    print("🤖 Setting up Groq API Key for Job Analysis")
    print("=" * 50)
    
    # Check if API key already exists
    config_file = Path("groq_config.json")
    
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            if config.get('api_key'):
                print(f"✅ Groq API key already configured")
                print(f"   Key: {config['api_key'][:10]}...{config['api_key'][-4:]}")
                
                choice = input("\n🔄 Do you want to update the API key? (y/n): ").lower()
                if choice != 'y':
                    return config['api_key']
        except Exception as e:
            print(f"⚠️ Error reading existing config: {e}")
    
    print("\n📝 Please enter your Groq API key:")
    print("   You can get one from: https://console.groq.com/")
    print("   The key should start with 'gsk_'")
    
    api_key = input("\n🔑 Groq API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return None
    
    if not api_key.startswith('gsk_'):
        print("⚠️ Warning: Groq API keys typically start with 'gsk_'")
        choice = input("   Continue anyway? (y/n): ").lower()
        if choice != 'y':
            return None
    
    # Save the API key
    config = {
        'api_key': api_key,
        'provider': 'groq',
        'model': 'llama3-8b-8192'
    }
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Groq API key saved successfully!")
        print(f"   📁 Config file: {config_file}")
        
        # Also set as environment variable
        os.environ['GROQ_API_KEY'] = api_key
        print(f"   🌍 Environment variable set: GROQ_API_KEY")
        
        return api_key
        
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return None

def load_groq_api_key():
    """Load Groq API key from config file or environment"""
    
    # Try environment variable first
    api_key = os.environ.get('GROQ_API_KEY')
    if api_key:
        return api_key
    
    # Try config file
    config_file = Path("groq_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            return config.get('api_key')
        except Exception:
            pass
    
    return None

def test_groq_connection(api_key):
    """Test Groq API connection"""
    
    if not api_key:
        print("❌ No API key provided for testing")
        return False
    
    try:
        import groq
        
        print("\n🧪 Testing Groq API connection...")
        
        client = groq.Groq(api_key=api_key)
        
        # Simple test request
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": "Hello! Please respond with 'Groq API is working!'"}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content.strip()
        print(f"✅ Groq API test successful!")
        print(f"   🤖 Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")
        return False

if __name__ == "__main__":
    # Set up API key
    api_key = setup_groq_api_key()
    
    if api_key:
        # Test the connection
        test_groq_connection(api_key)
        
        print(f"\n🎉 Groq API setup complete!")
        print(f"💡 You can now use AI-powered job analysis with Groq")
        print(f"   The system will automatically use this API key for job analysis")
    else:
        print(f"\n⚠️ Groq API setup incomplete")
        print(f"   The system will use fallback keyword matching instead") 