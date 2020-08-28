
# 최종
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import re
import time
from collections import ChainMap

soup_objects = []

with open('./news_data3.csv', 'w', encoding='euc-kr', newline="") as csvfile:
    wr = csv.writer(csvfile)
    wr.writerow(['title', 'contents'])


# 메인화면에서 내용을 가져올 수 없기 때문에 각각의 기사 href에 들어가서 내용추출
def get_news(href_list):
    response = requests.get(href_list)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = soup.find('div', class_='article_view')
    news = news.get_text().replace('\n', '').replace('\t', '').replace('\xa0', ' ').replace('∙', '').replace('\xa9', '').replace('–', '').replace('\u200b', '')
    # news = re.sub(r'\[\w*\s*]|\(.*\)|<.+>|[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+|"|“|\'|.|기자', '', news)
    return news

cnt = 1
for i in range(1, 3):
    base_url = f'https://news.daum.net/breakingnews/digital?page='
    start_num = i
    URL = base_url + str(start_num)
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    soup_objects.append(soup)
    time.sleep(3)

    news_data = {}

    for soup in soup_objects:
        news_section = soup.select(
            'div[id=kakaoWrap] > div[id=kakaoContent] > div[id=cMain] > div[id=mArticle] > div.box_etc > ul > li')
        for news in news_section:
            a_tag = news.select_one('div.cont_thumb > strong > a')
            href_list = a_tag['href']
            news_sub = a_tag.get_text().replace('\xa0', '')
            news = get_news(href_list)

            news_data = {
                'title': news_sub,
                'contents': news
            }

            with open('./news_data3.csv', 'a', encoding='euc-kr', newline="") as csvfile:
                fieldnames = ['title', 'contents']
                csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
                csvwriter.writerow(news_data)

            print(f"{cnt}개 기사 추출중")
            cnt += 1


