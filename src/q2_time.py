import json
import re
from collections import defaultdict
from typing import List, Tuple
from emoji import UNICODE_EMOJI

def extract_emojis(text: str) -> List[str]:
    return [char for char in text if char in UNICODE_EMOJI['en']]

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    emoji_counts = defaultdict(int)
    emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                tweet = json.loads(line)
                if 'content' in tweet:
                    emojis = emoji_pattern.findall(tweet['content'])
                    for emoji in emojis:
                        emoji_counts[emoji] += 1
            except (json.JSONDecodeError, KeyError):
                continue

    top_10_emojis = sorted(emoji_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return top_10_emojis

# Ejemplo de uso
file_path = "C:/Users/mauri/OneDrive/Escritorio/Challenge Latam/farmers-protest-tweets-2021-2-4.json"
try:
    top_10_emojis = q2_time(file_path)
    print(top_10_emojis)
except FileNotFoundError:
    print(f"File not found: {file_path}. Please check the file path and try again.")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON file: {e}")
