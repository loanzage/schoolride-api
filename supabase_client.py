import requests
import os

SUPABASE_URL = "https://laezukqmsutahwmjcsyo.supabase.co"

SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def test_connection():
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/test?select=*",
            headers=headers
        )
        return response.status_code, response.text
    except Exception as e:
        return 500, str(e)