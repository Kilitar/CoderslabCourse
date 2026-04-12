import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import os
import json
import re
from datetime import datetime

# Configuration
INPUT_FILE = 'DATA/ufc_fighters.csv'
OUTPUT_FILE = 'DATA/ufc_fighters_enriched.csv'
CACHE_FILE = 'DATA/ufcstats_index.json'
BASE_URL = 'http://ufcstats.com/statistics/fighters'

def get_fighter_index():
    """Scrapes the alphabetical index of all fighters from UFCStats."""
    if os.path.exists(CACHE_FILE):
        print(f"Loading index from cache: {CACHE_FILE}", flush=True)
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    print("Scraping UFCStats index (A-Z)...", flush=True)
    index = {}
    import string
    for char in string.ascii_lowercase:
        url = f"{BASE_URL}?char={char}&page=all"
        print(f"  Fetching: {url}", flush=True)
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all fighter links in the table
            # Links are in rows, usually the first and second <a> tags in a row are First and Last name
            rows = soup.find_all('tr', class_='b-statistics__table-row')
            for row in rows[2:]: # Skip header
                cells = row.find_all('td')
                if len(cells) < 2: continue
                
                links = cells[0].find_all('a')
                if not links: continue
                
                # Link is the same for first/last name, just take the first one
                profile_url = links[0]['href']
                first_name = cells[0].text.strip()
                last_name = cells[1].text.strip()
                full_name = f"{first_name} {last_name}".strip()
                
                if full_name not in index:
                    index[full_name] = []
                index[full_name].append(profile_url)
            
            time.sleep(1) # Be respectful
        except Exception as e:
            print(f"Error fetching {url}: {e}", flush=True)
            
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=4)
    
    return index

def parse_dob(dob_str):
    """Converts 'Month DD, YYYY' to 'YYYY-MM-DD'."""
    dob_str = dob_str.strip()
    if not dob_str or dob_str == '--':
        return None
    try:
        # Expected format: "Jan 12, 1980"
        dt = datetime.strptime(dob_str, "%b %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return None

def scrape_fighter_dob(url):
    """Scrapes the Date of Birth from a fighter's profile page."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # DOB is usually in a list item: <li class="b-list__box-list-item b-list__box-list-item_type_block"> ... DOB: ... </li>
        list_items = soup.find_all('li', class_='b-list__box-list-item_type_block')
        for item in list_items:
            text = item.text.strip()
            if 'DOB:' in text:
                dob_raw = text.replace('DOB:', '').strip()
                return parse_dob(dob_raw)
    except Exception as e:
        print(f"Error scraping {url}: {e}")
    return None

def main():
    # Load original data
    print(f"Reading {INPUT_FILE}...", flush=True)
    df = pd.read_csv(INPUT_FILE)
    
    # Get total missing
    missing_mask = df['date_of_birth'].isna()
    missing_count = missing_mask.sum()
    print(f"Found {len(df)} fighters, {missing_count} missing DOB.", flush=True)
    
    if missing_count == 0:
        print("No missing birth dates to fill.", flush=True)
        df.to_csv(OUTPUT_FILE, index=False)
        return

    # Get index from UFCStats
    fighter_index = get_fighter_index()
    
    # Process missing fighters
    count_found = 0
    count_filled = 0
    
    for idx, row in df[missing_mask].iterrows():
        name = row['fighter_name']
        
        # Try to find link in index
        urls = fighter_index.get(name, [])
        
        if not urls:
            # Try fuzzy matching or case-insensitive if needed
            # For now, stick to exact match
            continue
            
        count_found += 1
        
        # If multiple URLs, we might need to disambiguate. 
        # For now, let's take the first one or skip if too many.
        if len(urls) > 1:
            print(f"Ambiguous result for {name}: {urls}. Skipping for safety.", flush=True)
            continue
            
        url = urls[0]
        print(f"Scraping DOB for {name} ({url})...", flush=True)
        
        dob = scrape_fighter_dob(url)
        if dob:
            df.at[idx, 'date_of_birth'] = dob
            count_filled += 1
            print(f"  Success: {dob}", flush=True)
        else:
            print(f"  Failed: DOB not found on page.", flush=True)
            
        # Stop after every request
        time.sleep(1)
        
        # Periodic save (every 50)
        if count_filled % 50 == 0 and count_filled > 0:
            df.to_csv(OUTPUT_FILE, index=False)
            print(f"--- Saved progress to {OUTPUT_FILE} ({count_filled} filled) ---", flush=True)

    # Final save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nFinal Summary:", flush=True)
    print(f"Total missing: {missing_count}", flush=True)
    print(f"Matched on UFCStats: {count_found}", flush=True)
    print(f"Successfully filled: {count_filled}", flush=True)
    print(f"Result saved to: {OUTPUT_FILE}", flush=True)

if __name__ == "__main__":
    main()
