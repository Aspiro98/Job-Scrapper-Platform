#!/usr/bin/env python3
"""
Fix Duplicate Job IDs
Clean existing data and re-scrape with fixed job ID generation logic
"""

import os
import sys
import subprocess
from pathlib import Path

def clean_and_rescrape():
    """Clean existing data and re-scrape with fixed ID generation"""
    
    print("🔧 Fixing Duplicate Job IDs")
    print("=" * 50)
    
    # Check if scraped_data.json exists
    if os.path.exists('scraped_data.json'):
        print("🗑️  Removing existing scraped_data.json...")
        os.remove('scraped_data.json')
        print("✅ Removed existing data")
    else:
        print("ℹ️  No existing scraped_data.json found")
    
    # Check if there are any backup files
    backup_files = ['scraped_data_backup.json', 'scraped_data_clean.json']
    for backup_file in backup_files:
        if os.path.exists(backup_file):
            print(f"🗑️  Removing backup file: {backup_file}")
            os.remove(backup_file)
    
    print("\n🚀 Starting fresh scrape with fixed job ID generation...")
    print("📋 This will ensure all job IDs are globally unique")
    print("⏰ This may take several minutes...")
    
    try:
        # Run the multi-company spider
        print("\n🔄 Running multi-company spider...")
        result = subprocess.run([
            sys.executable, 'run_multi_company_spider.py'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Scraping completed successfully!")
            print("📊 New data generated with unique job IDs")
            
            # Verify the fix
            print("\n🔍 Verifying job ID uniqueness...")
            verify_result = subprocess.run([
                sys.executable, 'check_duplicate_job_ids.py'
            ], capture_output=True, text=True)
            
            if verify_result.returncode == 0:
                print("✅ Verification completed!")
                print("🎉 Job IDs should now be globally unique")
            else:
                print("⚠️  Verification failed, but scraping completed")
                
        else:
            print(f"❌ Scraping failed with error code: {result.returncode}")
            print(f"Error output: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error during scraping: {e}")
        return False
    
    print("\n🎯 Next Steps:")
    print("1. Test automation with a few jobs to verify the fix")
    print("2. Check that the correct company pages open")
    print("3. If issues persist, run check_duplicate_job_ids.py again")
    
    return True

def backup_existing_data():
    """Create a backup of existing data before cleaning"""
    
    if os.path.exists('scraped_data.json'):
        print("💾 Creating backup of existing data...")
        
        import json
        from datetime import datetime
        
        # Load existing data
        with open('scraped_data.json', 'r') as f:
            data = json.load(f)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"scraped_data_backup_{timestamp}.json"
        
        # Save backup
        with open(backup_filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Backup created: {backup_filename}")
        return backup_filename
    
    return None

if __name__ == "__main__":
    print("🔧 Fix Duplicate Job IDs Tool")
    print("=" * 50)
    
    # Ask user if they want to backup existing data
    if os.path.exists('scraped_data.json'):
        response = input("\n❓ Do you want to backup existing data before cleaning? (y/n): ")
        if response.lower() in ['y', 'yes']:
            backup_file = backup_existing_data()
            if backup_file:
                print(f"💾 Backup saved as: {backup_file}")
    
    # Confirm the action
    print("\n⚠️  This will:")
    print("   - Delete existing scraped_data.json")
    print("   - Re-scrape all companies with fixed job ID generation")
    print("   - Ensure all job IDs are globally unique")
    
    response = input("\n❓ Continue with fixing duplicate job IDs? (y/n): ")
    
    if response.lower() in ['y', 'yes']:
        success = clean_and_rescrape()
        if success:
            print("\n🎉 Duplicate job ID fix completed successfully!")
        else:
            print("\n❌ Fix failed. Please check the error messages above.")
    else:
        print("\n❌ Operation cancelled.") 