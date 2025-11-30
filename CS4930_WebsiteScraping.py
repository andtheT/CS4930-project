# pip install requests
# pip install beautifulsoup4

# pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup

#Fetch and parse the page
def scrape_static_content(url):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }
    response = requests.get(url,headers=headers)
    soup=BeautifulSoup(response.content,'html.parser')
    #Find the main content container 
    # content_div= soup.find_all(['div', 'section'], class_='article--viewer_content')
    content_div = soup.find('div', id='mw-content-text')
    print("Static Content from Website")
    
    if content_div:
        parser_output = content_div.find('div', class_='mw-parser-output')
        if parser_output:
            for para in parser_output.find_all('p'):
                text=para.get_text(strip=True)
                if text:
                    print(text)
        else:
            print("mw-parser-output not found inside mw-content-text.")
    else:
        print("No article content found.")

if __name__ == "__main__":
    scrape_static_content("https://en.wikipedia.org/wiki/Enigma_machine")