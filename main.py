import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta


# Функция для проверки наличия упоминаний Байдена и Трампа
def contains_keywords(text):
    keywords = ["biden", "trump", "democrat", "republican"]
    return any(keyword.lower() in text.lower() for keyword in keywords)


# Функция для извлечения новостей с веб-страницы
def extract_news(last_check_time):
    url = "https://www.nytimes.com/section/politics"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve webpage, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')

    # Найдите все элементы, которые могут содержать статьи
    articles = soup.find_all('div', class_='css-13mho3u')

    news = []

    for article in articles:
        title_tag = article.find('h3')
        summary_tag = article.find('p')
        author_tag = article.find('span', class_='css-1n7hynb')

        if title_tag and summary_tag:
            title = title_tag.text.strip()
            summary = summary_tag.text.strip()
            author = author_tag.text.strip() if author_tag else "Unknown"
            print('work title:', title)

            if contains_keywords(title) or contains_keywords(summary):
                news_time = datetime.now()

                # Проверяем, что новость была опубликована после времени последней проверки
                if news_time > last_check_time:
                    news.append({
                        'title': title,
                        'summary': summary,
                        'author': author,
                        'datetime': news_time.strftime('%Y-%m-%d %H:%M:%S')
                    })

    return news, datetime.now()


# Функция для записи новостей в лог
def log_news(processed_titles, last_check_time):
    news, new_check_time = extract_news(last_check_time)
    new_news = [item for item in news if item['title'] not in processed_titles]

    if new_news:
        with open('NewsLog.txt', 'a', encoding='utf-8') as file:
            for item in new_news:
                file.write(f"Title: {item['title']}\n")
                file.write(f"Summary: {item['summary']}\n")
                file.write(f"Author: {item['author']}\n")
                file.write(f"Datetime: {item['datetime']}\n")
                file.write('\n' + '-' * 50 + '\n')

        # Отладочный вывод
        for item in new_news:
            print(f"Title: {item['title']}")
            print(f"Summary: {item['summary']}")
            print(f"Author: {item['author']}")
            print(f"Datetime: {item['datetime']}")
            print('\n' + '-' * 50 + '\n')

    return [item['title'] for item in new_news], new_check_time


# Запуск скрипта на 4 часа
start_time = datetime.now()
end_time = start_time + timedelta(hours=4)
processed_titles = set()
last_check_time = datetime.now()  # Время последней проверки начинается с текущего момента

while datetime.now() < end_time:
    new_titles, last_check_time = log_news(processed_titles, last_check_time)
    processed_titles.update(new_titles)
    time.sleep(10)  # Ожидание

print("Script has stopped running after 4 hours.")
