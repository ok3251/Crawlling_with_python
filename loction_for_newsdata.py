import os
import requests
from bs4 import BeautifulSoup

# 바탕화면 경로 설정
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

# 최상위 폴더 설정
top_folder_name = 'Crawling_Data'
top_folder_path = os.path.join(desktop_path, top_folder_name)

# 최상위 폴더가 존재하지 않으면 생성
if not os.path.exists(top_folder_path):
    os.makedirs(top_folder_path)

# 뉴스 기사 저장할 위치 목록
locations = ['seoul', 'busan','gyeonggi','incheon','daegu',
             'gwangju','daejeon','sejong','ulsan','gangwon','chungcheong',
             'gyeongsang','jeolla','jeju']

for location in locations:
    # 위치별로 폴더 경로 지정
    folder_name = f'{location}_Crawling_folder'
    folder_path = os.path.join(top_folder_path, folder_name)
    
    # 폴더가 존재하지 않으면 생성
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    content_links = []

    for i in range(1, 2):
        main_page_url = f'https://realestate.daum.net/news/region/{location}?page={i}'
        get_url = requests.get(main_page_url)
        main_page_html = get_url.text

        soup = BeautifulSoup(main_page_html, 'html.parser')

        for part_news in soup.find_all('ul', class_='list_partnews'):
            for a in part_news.find_all('a', href=True):
                href = a['href']
                content_links.append('https:'+href)
    
    content_links = list(set(content_links))
    print(f'{location} 링크 수집 완료: {len(content_links)}개')

    for i, link in enumerate(content_links):
        response = requests.get(link)
        content = response.text

        soup2 = BeautifulSoup(content, 'html.parser')

        target_element = soup2.find(class_='article_view')

        if target_element:
            target_text = target_element.get_text()

            file_path = os.path.join(folder_path, f'Crawling_{location}_{i+1}.txt')
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(target_text)
            print(f'{location}_{i+1} 데이터가 저장되었습니다.')
        else:
            print(f'해당 클래스를 찾을 수 없음 {link}')