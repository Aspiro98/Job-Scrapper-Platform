#!/usr/bin/env python3
"""
Setup script for AI-powered job filtering system
"""

import os
import sys

def setup_ai_filtering():
    """Guide user through setting up AI filtering"""
    
    print("🤖 AI-Powered Job Filtering Setup")
    print("=" * 50)
    
    # Check if API key is already set
    if os.getenv('GROQ_API_KEY'):
        print("✅ GROQ_API_KEY is already set!")
        print(f"Current key: {os.getenv('GROQ_API_KEY')[:10]}...")
        return True
    
    print("❌ GROQ_API_KEY is not set.")
    print("\n🔧 Setup Instructions:")
    print("1. Visit https://console.groq.com/")
    print("2. Sign up or log in to your account")
    print("3. Create a new API key")
    print("4. Copy the API key")
    
    # Ask user for API key
    api_key = input("\n📝 Enter your Groq API key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return False
    
    # Test the API key
    print("\n🧪 Testing API key...")
    try:
        os.environ['GROQ_API_KEY'] = api_key
        
        # Import and test
        sys.path.append('scrapers')
        from scrapers.utils.ai_filter_processor import AIFilterProcessor
        
        ai_processor = AIFilterProcessor()
        print("✅ API key is valid!")
        
        # Test with a simple job
        test_job = {
            'title': 'Software Engineer',
            'location': 'San Francisco, CA',
            'company': 'Test Company',
            'description': 'Test job description'
        }
        
        result = ai_processor.process_job(test_job)
        print("✅ AI processing test successful!")
        
        # Save to shell profile
        save_to_profile = input("\n💾 Save API key to shell profile? (y/n): ").strip().lower()
        
        if save_to_profile == 'y':
            shell_profile = get_shell_profile()
            if shell_profile:
                with open(shell_profile, 'a') as f:
                    f.write(f'\n# Groq API Key for AI Job Filtering\nexport GROQ_API_KEY="{api_key}"\n')
                print(f"✅ API key saved to {shell_profile}")
                print("🔄 Please restart your terminal or run: source ~/.bashrc (or ~/.zshrc)")
            else:
                print("⚠️  Could not determine shell profile. Please add manually:")
                print(f'export GROQ_API_KEY="{api_key}"')
        else:
            print("💡 To use the API key in this session, run:")
            print(f'export GROQ_API_KEY="{api_key}"')
        
        return True
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        print("🔧 Please check your API key and try again.")
        return False

def get_shell_profile():
    """Get the appropriate shell profile file"""
    shell = os.getenv('SHELL', '')
    
    if 'zsh' in shell:
        return os.path.expanduser('~/.zshrc')
    elif 'bash' in shell:
        return os.path.expanduser('~/.bashrc')
    else:
        return None

def main():
    """Main setup function"""
    print("🚀 Welcome to AI-Powered Job Filtering!")
    print("This will help you set up the Groq API key for intelligent job filtering.")
    
    if setup_ai_filtering():
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Test the system: python test_ai_processor.py")
        print("2. Run the scraper to get job data")
        print("3. Start the Flask app: python app.py")
        print("4. Enjoy AI-powered filtering! 🚀")
    else:
        print("\n❌ Setup failed. Please try again.")
        sys.exit(1)

if __name__ == "__main__":
    main() 