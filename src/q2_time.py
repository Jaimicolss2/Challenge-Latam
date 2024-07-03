import json
import re
from collections import defaultdict
from typing import List, Tuple

def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    emoji_counts = defaultdict(int)
    emoji_pattern = re.compile(r'[\U0001F300-\U0001F64F]|[\U0001F680-\U0001F6FF]|[\U0001F700-\U0001F77F]|[\U0001F780-\U0001F7FF]|[\U0001F800-\U0001F8FF]', flags=re.UNICODE)

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

if __name__ == "__main__":
    file_path = "C:/Users/mauri/OneDrive/Escritorio/Challenge Latam/farmers-protest-tweets-2021-2-4.json"
    try:
        top_10_emojis = q2_memory(file_path)
        print(top_10_emojis)
    except FileNotFoundError:
        print(f"File not found: {file_path}. Please check the file path and try again.")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file: {e}")
