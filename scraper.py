import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import re   # Necessary imports

# Output file path
output_file = os.path.join("data", "rumhowler_data.xlsx")   # save location
os.makedirs("data", exist_ok=True)      # creates folder if it doesnt exist

# Rum review URL
url = "https://therumhowlerblog.com/rum-reviews/"   # Target url for scraping
headers = {"User-Agent": "Mozilla/5.0"}

# Fetch the page
'''
Sends GET request to webpage.
If the request is not 200, send error and exit
'''
response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Failed to load page: {response.status_code}")
    exit()

soup = BeautifulSoup(response.text, "html.parser")  # Parse Html Page
rum_list = []   # For storing parsed data


lis = soup.select("div.entrytext li")   # Find all <li> elements inside div
i = 0
while i < len(lis):     # Iterate trough list items
    current_text = lis[i].get_text(strip=True)      # Gets text from the list
    next_text = lis[i + 1].get_text(strip=True) if i + 1 < len(lis) else ""     # Gets current and next text if score is on next line

    # Match patterns like: "Rum Name (86.5)"
    direct_match = re.match(r"^(.*?)\s*\((\d{1,3}(?:\.\d)?)\)$", current_text)      # Matches patterns
    if direct_match:    # Handle lines where name and review score are together
        name = direct_match.group(1).strip()
        score = float(direct_match.group(2))
        rum_list.append({"Rum": name, "Score": score})
        i += 1
        continue

    next_is_score = re.match(r"^\((\d{1,3}(?:\.\d)?)\)$", next_text)    # Checks if next line contains only score

    '''
    Handle two-line cases like:
    <li>Rum Name</li>
    <li>(88.5)</li> 
    or:
    <li><a>Rum A</a> <a>Rum B</a></li>
    <li>(90.0)</li>
    '''
    if next_is_score:
        anchors = lis[i].select("a")
        if anchors:     # If current line has mustiple <a> elements, treat as a rum with the same score
            for a in anchors:
                name = a.get_text(strip=True)
                rum_list.append({
                    "Rum": name,
                    "Score": float(next_is_score.group(1))
                })
        else:       # Else assume the whole text is the name
            rum_list.append({
                "Rum": current_text,
                "Score": float(next_is_score.group(1))
            })
        i += 2
        continue

    print(f"Skipped: '{current_text}'")     # If no pattern matches, logs skipped item and continues. (Prints out skipped data)
    i += 1

# Save to Excel
df = pd.DataFrame(rum_list)
df.to_excel(output_file, index=False)
print(f"Saved {len(df)} rums to {output_file}")
