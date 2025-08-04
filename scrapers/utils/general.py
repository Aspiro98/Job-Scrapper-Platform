from hashids import Hashids
import os
from dotenv import load_dotenv

load_dotenv()

# Get HASHIDS_SALT from environment, with fallback
salt = os.environ.get("HASHIDS_SALT")
if not salt or salt == "your_salt_here":
    salt = "default_salt_for_job_scraper_2024"  # Fallback salt
    print(f"⚠️  Using fallback HASHIDS_SALT. Set HASHIDS_SALT environment variable for production use.")

hash_ids = Hashids(
    salt=salt, alphabet="abcdefghijklmnopqrstuvwxyz1234567890"
)
