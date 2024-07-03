import json
import re
from collections import defaultdict
from typing import List, Tuple
from memory_profiler import profile

def extract_mentions(text: str) -> List[str]:
    # Utilizamos regex para encontrar todas las menciones de usuario (@username)
    mention_pattern = re.compile(r'@(\w+)')
    return mention_pattern.findall(text)

@profile
def q3_memory(file_path: str) -> List[Tuple[str, int]]:
    mention_counts = defaultdict(int)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                tweet = json.loads(line)
                if 'content' in tweet:
                    # Utilizamos generadores para evitar almacenar todos los tweets en memoria
                    mentions = extract_mentions(tweet['content'])
                    for mention in mentions:
                        mention_counts[mention] += 1
            except (json.JSONDecodeError, KeyError):
                continue

    # Ordenamos y seleccionamos los top 10 en base a la cuenta de menciones
    top_10_mentions = sorted(mention_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Liberamos memoria explícitamente si es necesario, con la finalidad de poder correr diferentes instancias con menor uso de memoria
    del mention_counts
    
    return top_10_mentions

file_path = "C:/Users/mauri/OneDrive/Escritorio/Challenge Latam/farmers-protest-tweets-2021-2-4.json"
try:
    top_10_mentions = q3_memory(file_path)
    print(top_10_mentions)
except FileNotFoundError:
    print(f"File not found: {file_path}. Please check the file path and try again.")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON file: {e}")
