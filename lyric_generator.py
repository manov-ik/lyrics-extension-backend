import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

def format_lyrics(text):
    match = re.search(r'(Male :|Female :|Chorus :)', text)
    lyrics_start = text[match.start():]
    formatted_lyrics = re.sub(r'(?<!^)(?=[A-Z])', '\n', lyrics_start)
    return formatted_lyrics

def get_link(query,max_results=3):
    query = "tamil2lyrics lyrics "+query
    headers = {'User-Agent': 'Mozilla/5.0'}
    query_encoded = urllib.parse.quote_plus(query)
    url = f"https://html.duckduckgo.com/html/?q={query_encoded}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.find_all('a', {'class': 'result__a'}, limit=max_results):
        title = result.get_text()
        link = result.get('href')
        results.append({'title': title, 'link': link})

    raw_link = results[0]["link"]
    parsed = urllib.parse.urlparse("https:" + raw_link)
    query_params = urllib.parse.parse_qs(parsed.query)

    real_url = query_params.get('uddg', [None])[0]
    return real_url

def generate_lyrics(title, is_retry=False):
    try:
        if is_retry:
            song_name = title.lower()
        else:
            song_name = title.split('|')[0]
            print(song_name)
        
        # Set headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = get_link(query=song_name)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content_div = soup.find('div', id='English')
        
        if content_div:
            lyrics_text = content_div.get_text(strip=True)
            return format_lyrics(lyrics_text)
        else:
            return "Could not find lyrics content"
            
    except Exception as e:
        return f"Error: {str(e)}"
