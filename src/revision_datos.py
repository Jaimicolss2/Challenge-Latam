import json
import re
from datetime import datetime, date
from collections import defaultdict
from typing import List, Dict

def find_invalid_entries(file_path: str) -> List[Dict]:
    invalid_entries = []
    emoji_counts = defaultdict(int)
    emoji_pattern = re.compile(r'[\U0001F300-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]', flags=re.UNICODE)

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                tweet = json.loads(line)

                # Check for required fields
                if 'user' not in tweet or 'date' not in tweet or 'content' not in tweet:
                    raise KeyError("Missing required fields")

                # Check date format
                try:
                    datetime.strptime(tweet['date'], "%Y-%m-%dT%H:%M:%S%z")
                except ValueError:
                    raise ValueError("Incorrect date format")

                # Check emojis in content
                emojis = emoji_pattern.findall(tweet['content'])
                for emoji in emojis:
                    emoji_counts[emoji] += 1

            except (json.JSONDecodeError, KeyError, ValueError) as e:
                invalid_entries.append({"line": line.strip(), "error": str(e)})

    return invalid_entries

file_path = "C:/Users/mauri/OneDrive/Escritorio/Challenge Latam/farmers-protest-tweets-2021-2-4.json"
try:
    invalid_entries = find_invalid_entries(file_path)
    if invalid_entries:
        print("Invalid entries found:")
        for entry in invalid_entries:
            print(f"Line: {entry['line']}")
            print(f"Error: {entry['error']}")
            print("-" * 80)
    else:
        print("No invalid entries found.")
except FileNotFoundError:
    print(f"File not found: {file_path}. Please check the file path and try again.")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON file: {e}")
