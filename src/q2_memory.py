import json
import re
from collections import defaultdict
from typing import List, Tuple
from emoji import UNICODE_EMOJI
from memory_profiler import profile

def is_emoji(char: str) -> bool:
    # Validar si el carácter es un emoji Unicode
    return char in UNICODE_EMOJI['en']

@profile
def q2_memory(file_path: str) -> List[Tuple[str, int]]:
    emoji_counts = defaultdict(int)
    emoji_pattern = re.compile(r'[\U0001F000-\U0001FFFF]|[\U00002000-\U00003FFF]', flags=re.UNICODE)  # Patrón para emojis Unicode
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                tweet = json.loads(line)
                if 'content' in tweet:
                    emojis = emoji_pattern.findall(tweet['content'])
                    valid_emojis = filter(is_emoji, emojis)  # Filtrar solo emojis válidos
                    for emoji in valid_emojis:
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
