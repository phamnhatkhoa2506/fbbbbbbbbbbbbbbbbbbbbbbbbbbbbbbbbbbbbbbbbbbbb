import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = 'https://www.facebook.com/Vuonglan1989'

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.find(
        'meta',
        {'name': 'description'}
    )

    data = {
        'content': content.get('content')
    }

    print(data)