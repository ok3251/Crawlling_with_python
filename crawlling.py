import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# 바탕화면 경로 설정 및 폴더 경로 지정
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
folder_name = 'Crawlling_folder1'  # 저장할 폴더 이름
folder_path = os.path.join(desktop_path, folder_name)

# 폴더가 존재하지 않으면 생성
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# 시작 날짜와 종료 날짜 설정
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 3, 31)

# 현재 날짜 초기화
current_date = start_date

while current_date <= end_date:
    # 날짜 문자열 생성
    year = current_date.strftime('%Y')
    month = current_date.strftime('%m')
    day = current_date.strftime('%d')
    
    # URL 생성
    main_page_url = f'https://news.naver.com/breakingnews/section/101/260?date={year}{month}{day}'

    response = requests.get(main_page_url)
    main_page_html = response.text

    soup = BeautifulSoup(main_page_html, 'html.parser')

    article_links = []

    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if '/mnews/article/' in href:
            if 'comment/' in href:
                href = href.replace('comment/', '')
            article_links.append(href)

    article_links = list(set(article_links))

    for i, link in enumerate(article_links):
        response = requests.get(link)
        html = response.text

        soup = BeautifulSoup(html, 'html.parser')

        target_element = soup.find(class_='go_trans _article_content')

        if target_element:
            target_text = target_element.get_text()

            # 파일을 날짜와 링크 인덱스 기반으로 저장
            file_path = os.path.join(folder_path, f'Crawlling{year}_{month}_{day}_{i}.txt')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(target_text)
            print(f'{year}-{month}-{day} 데이터가 저장되었습니다.')
        else:
            print(f"해당 클래스 이름을 가진 요소를 찾을 수 없습니다. {link}")

    # 다음 날짜로 이동
    current_date += timedelta(days=1)



