import json
from collections import defaultdict #Libreria utilizada para la comprobacion de lo datos, al ser una gran cantidad de datos esto optimiza la eficiencia del codigo
from datetime import datetime, date
from typing import List, Tuple
from memory_profiler import profile

@profile
def q1_time(file_path: str) -> List[Tuple[date, str]]:
    date_tweet_counts = defaultdict(lambda: defaultdict(int)) #Inicializa el contador de tweets en 0

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                tweet = json.loads(line)
                tweet_date = datetime.strptime(tweet['date'], "%Y-%m-%dT%H:%M:%S%z").date()
                username = tweet['user']['username']
                date_tweet_counts[tweet_date][username] += 1
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                continue

    top_10_dates = sorted(date_tweet_counts.items(), key=lambda x: sum(x[1].values()), reverse=True)[:10]
    result = [(tweet_date, max(users.items(), key=lambda x: x[1])[0]) for tweet_date, users in top_10_dates]

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
