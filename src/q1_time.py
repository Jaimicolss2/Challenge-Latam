import json
from collections import defaultdict #Libreria utilizada para la comprobacion de lo datos, al ser una gran cantidad de datos esto optimiza la eficiencia del codigo
from typing import List, Tuple
from datetime import datetime, date

def q1_time(file_path: str) -> List[Tuple[date, str]]:
    date_tweet_counts = defaultdict(lambda: defaultdict(int)) #Inicializa el contador de tweets en 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                tweet = json.loads(line)
                if 'user' in tweet and 'date' in tweet:
                    tweet_date = datetime.strptime(tweet['date'], "%Y-%m-%dT%H:%M:%S%z").date()
                    username = tweet['user']['username']
                    date_tweet_counts[tweet_date][username] += 1
            except (json.JSONDecodeError, KeyError):
                continue

    top_10_dates = sorted(date_tweet_counts.keys(), key=lambda x: sum(date_tweet_counts[x].values()), reverse=True)[:10]

    result = [(tweet_date, max(date_tweet_counts[tweet_date].items(), key=lambda x: x[1])[0]) for tweet_date in top_10_dates]

    return result

#Respuesta usando try/except para manejar los casos de error
file_path = "C:/Users/mauri/OneDrive/Escritorio/Challenge Latam/farmers-protest-tweets-2021-2-4.json"
try:
    top_10_dates_users = q1_time(file_path)
    print(top_10_dates_users)
except FileNotFoundError:
    print(f"File not found: {file_path}. Please check the file path and try again.")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON file: {e}")
