import requests     # For making GET requests to fetch html content
from bs4 import BeautifulSoup       # For navigating html using css selectors
import pandas as pd     # Data manipulation and saving to excel
import os       # For file path handling / directory creation
import re       # used to extract numbers from text
import time     # For adding delays

# Output file path
OUTPUT_FILE = os.path.join("data", "whiskey_scores_data.xlsx")
os.makedirs("data", exist_ok=True)

# List of whisky base URLs (/____)
COUNTRIES = [
    "scotland", "ireland", "japan", "usa", "canada", "australia",
    "india", "england", "france", "germany", "sweden", "world"
]

BASE_URL = "https://whiskyscores.com/whisky"    # base url
HEADERS = {"User-Agent": "Mozilla/5.0"}         # user agent to avoid bot blocks

def extract_score_data(score_text: str):
    """
    Extract average score and review count from text like:
    'Average Score (88) x Highest Score (92) x Lowest Score (83) x # of Times Scored (4)'
    """
    avg_match = re.search(r"Average Score \((\d+)\)", score_text)
    count_match = re.search(r"Times Scored \((\d+)\)", score_text)
    try:
        avg = float(avg_match.group(1)) if avg_match else None
        count = int(count_match.group(1)) if count_match else 0
        return avg, count
    except:
        return None, 0

def fetch_all_whiskey_scores(max_pages_per_country=10000, delay=0.5):
    """
Loops through each country url and page, extracting scores.
    """
    results = []
    for country in COUNTRIES:
        print(f"\n=== Fetching: {country.upper()} ===")

        for page in range(0, max_pages_per_country * 10, 10):   # *10 for url (url pages specified /10, /20, /30 etc.)
            url = f"{BASE_URL}/{country}" if page == 0 else f"{BASE_URL}/{country}/{page}"
            resp = requests.get(url, headers=HEADERS)       # load html
            if resp.status_code != 200:
                print(f"  Failed to fetch page {page}: HTTP {resp.status_code}")
                break

            soup = BeautifulSoup(resp.text, "html.parser")  # Parse html page
            rows = soup.select("div.row-score-list")                # Find each whiskey listing on page
            if not rows:
                print(f"  No row-score-list blocks on page {page}. Stopping.")
                break

            valid_count = 0
            for row in rows:
                name_tag = row.select_one("p.pt11b.remove-bottom a")    # Whiskey name
                score_tag = row.select_one("span.article-date")         # Score

                if not name_tag or not score_tag:
                    continue

                name = name_tag.get_text(strip=True)
                avg_score, count = extract_score_data(score_tag.get_text())     # Parses values

                if avg_score is not None and count > 0:
                    results.append({        # Add to result
                        "Whiskey": name,
                        "Score": avg_score,
                        "ReviewCount": count
                    })
                    valid_count += 1

            print(f"  Page {page if page > 0 else 1}: {valid_count} valid whiskeys scraped")

            if valid_count == 0:    # Early stopping. If no whiskeys on page, stop fetching for that country
                print(f"  No valid whiskeys found on page {page}. Ending.")
                break

            time.sleep(delay)

    return results

def main():
    data = fetch_all_whiskey_scores()   # Call scraping function

    if not data:
        print("No data found.")
        return

    df = pd.DataFrame(data)
    df = df.sort_values("ReviewCount", ascending=False)     # Sort
    df = df.drop_duplicates(subset="Whiskey", keep="first")     # Remove duplicates
    df["Score"] = df["Score"].round(1)  # Format

    df.to_excel(OUTPUT_FILE, index=False)       # Save
    print(f"\nSaved {len(df)} unique whiskeys to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()