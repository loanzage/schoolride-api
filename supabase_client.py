import requests
import os

SUPABASE_URL = "https://db.laezukqmsutahwmjcsyo.supabase.co"

# For now we will use anon key (safe + enough for testing)
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def test_connection():
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/",
            headers=headers
        )
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)