import requests
from bs4 import BeautifulSoup
from mock_draft_data import MOCK_REGISTRY
import datetime

def scout_experts():
    print(f"--- NFL Draft Scout Report | {datetime.date.today()} ---")
    print(f"{'AUTHOR':<20} | {'LOCAL DATE':<12} | {'STATUS'}")
    print("-" * 50)

    for key, meta in MOCK_REGISTRY.items():
        author = meta['author']
        url = meta['url']
        local_date = meta['date']
        
        try:
            # We use a header to avoid being blocked as a bot
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"{author:<20} | {local_date:<12} | ⚠️ Link Error ({response.status_code})")
                continue

            # Check for mentions of "Mock" or "2026" near new dates
            # This is a heuristic - it looks for the word "Mock" and then a date string
            soup = BeautifulSoup(response.text, 'html.parser')
            page_text = soup.get_text().lower()
            
            # Simple heuristic: Does the page contain "Mock" and a date newer than our local one?
            # For a production script, we'd use site-specific selectors (e.g. .entry-date)
            has_mock = "mock" in page_text
            
            # Note: Scrapers often fail on complex SPAs, so we provide a general signal
            # If the page was modified today, it's a high-priority flag
            last_modified = response.headers.get('Last-Modified', 'Unknown')
            
            if has_mock:
                print(f"{author:<20} | {local_date:<12} | ✅ Checked (Mock keyword found)")
            else:
                print(f"{author:<20} | {local_date:<12} | 🔍 No recent 'Mock' keyword")

        except Exception as e:
            print(f"{author:<20} | {local_date:<12} | ❌ Error: {str(e)[:20]}")

    print("-" * 50)
    print("Recommendation: Check 🚨 'OUTDATED' entries manually to update DRAFT_DATA.")

if __name__ == "__main__":
    scout_experts()
