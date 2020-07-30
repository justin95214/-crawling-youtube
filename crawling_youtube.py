#1. mysql에서 database를 만들기
#2. mysql에서 table  두개 생성
#3. chromedriver위치를  코드 변경해서 넣어야함
#4. 코드 실행 방법 mysql문 비밀번호 입력 / mysql에서 만든 database이름입력 / 찾고자하는 닉네임 입력


import requests
from bs4 import BeautifulSoup as bs
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table
import warnings

warnings.filterwarnings("ignore")





def get_engine():
    engine = create_engine(engineUrl,convert_unicode=True)
    return engine

def init_db():
    Base.metadata.create_all(engine)

def insertDB(id,scrap_time, title, post_time,user_name,comments,like_count):
    insert_table.execute(id= str(id),
                         scrap_time=scrap_time,
                         title=str(title),
                         post_time=str(post_time),
                         username=str(user_name),
                         comments=comments,
                         likes=like_count
                         )
    print('데이터베이스 삽입완료')

print("chromedriver 반드시 주소변경 !!! ")
driverUrl = 'C:/Users/user/Desktop/chromedriver.exe'

print("mysql비밀번호를 넣으시오")
#mysql비밀번호를 넣으시오

engineUrlinput = input()
print("mysql database이름을 넣으시오")
databaseName = input()

engineUrl = 'mysql+pymysql://root:' +engineUrlinput +'@localhost/' +databaseName +'?charset=utf8mb4'

#'mysql+pymysql://root:j1995214@localhost/youtube?charset=utf8mb4'
get_engine()
engine = get_engine()
print(get_engine())

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
init_db()
#sqlalchemy insert init
conn = engine.connect()
metadata = MetaData(bind=engine)


table = Table('youtube_post', metadata, autoload=True)
table2 = Table('youtube_influencer', metadata, autoload=True)
insert_table=table.insert()
insert_table2 = table2.insert()


conn.execute('SET NAMES utf8;')
conn.execute('SET CHARACTER SET utf8;')
conn.execute('SET character_set_connection=utf8;')



print("닉네임을 입력하시오")
x = []
c = []
b = []
url1 = 'https://www.youtube.com/results?search_query='
url2 = input()
url3 = url1 + url2
print(url3)


response = requests.get(url3)
html = bs(response.text, 'html.parser')
# print(html)
tags = html.select('div.yt-lockup-byline > a ')
# print(tags)

for tag in tags:
    x = (tag['href'])
print(x)


html2= bs(response.text, 'html.parser')
#print(html2)
user_likers= html2.find('span',class_ = 'yt-subscription-button-subscriber-count-unbranded-horizontal yt-subscriber-count')
print("------------------------------------------------------------------------------------------------------------------------")
print("구독자 : "+ user_likers['title'])
likers = int(user_likers['title'].replace(",", "", 3))
print(type(likers))
new_url1 = 'https://www.youtube.com'

new_url2 = x
result_url = new_url1 + new_url2

print(result_url)

insert_table2.execute(username =url2, scrap_time = time.localtime() , followers =likers)


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('disable-gpu')

print('Waiting for minute to program load complete')

path = "driverUrl"

driver = webdriver.Chrome(driverUrl, options=options)
driver.get(result_url + '/videos')
body = driver.find_element_by_tag_name("body")
num_page = 100

while num_page:
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.3)
    num_page -= 1
    # print( num_page)
    try:
        driver.find_element_by_xpath("""//*[@id=" show-more-button"]/button""").click()
    except:
        None

new_html = driver.page_source
print(type(new_html))

html2 = bs(new_html, 'html.parser')
tags3 = html.select('a.yt-uix-tile-link')
for tag1 in tags3:
    b.append(new_url1 + tag1['href'])
    c.append(tag1["title"])

for a in b, c:
    print(a)

print(type(b))
print(range(len(b)))
driver.close()
length = len(b)
print("//---------------------------------------------------------------//")


while length:
    print("//---------------------------------------------------------------//")
    response3 = requests.get(b[length - 1])
    details_html = bs(response3.text, 'html.parser')
    details_tags1 = str(details_html.select('div.watch-view-count'))
    details_tags2 = str(details_html.select('div.video-extras-sparkbars > div.video-extras-sparkbar-likes'))
    details_tags2_2 = str(details_html.select('div.video-extras-sparkbars > div.video-extras-sparkbar-dislikes'))
    details_tags3 = str(details_html.select('div#watch-uploader-info > strong'))
    details_tags4 = details_html.find_all('span', class_='yt-uix-clickcard')
    details_tags5 = details_html.find_all('div', class_ = 'style-scope ytd-item-section-renderer')

    details_tags1 = re.sub('<div.*?>', '', details_tags1, 0, re.I | re.S).strip()
    details_tags1 = re.sub('</div>', '', details_tags1, 0, re.I | re.S).strip()
    details_tags1 = details_tags1.replace("[조회수", "", 1)
    details_tags1 = details_tags1.replace("회]", "", 1)
    details_tags1 = details_tags1.replace(",", "", 3)
    details_tags2 = re.sub('<div.*?:', '', details_tags2, 0, re.I | re.S).strip()
    details_tags2 = re.sub('></div>', '', details_tags2, 0, re.I | re.S).strip()
    details_tags2_2 = re.sub('<div.*?:', '', details_tags2_2, 0, re.I | re.S).strip()
    details_tags2_2 = re.sub('></div>', '', details_tags2_2, 0, re.I | re.S).strip()
    details_tags3 = re.sub('<strong.*?>', '', details_tags3, 0, re.I | re.S).strip()
    details_tags3 = re.sub('</strong>', '', details_tags3, 0, re.I | re.S).strip()

    i = 0;
    for do_and_dis in details_tags4:
        do_and_dis = do_and_dis.get_text().strip()
        #print('{0} / {1}'.format(i, do_and_dis))
        i = i + 1
        if (i == 4):
            do_and_dis = do_and_dis.replace(",", "", 3)
            #print('{0} / {1}' .format(i,do_and_dis))
            like_count = int(do_and_dis) - 1
        elif (i == 6):
            do_and_dis = do_and_dis.replace(",", "", 3)
            # print('{0} / {1}' .format(i,int(do_and_dis) -1))
            dislike_count = int(do_and_dis) - 1



    print('Waiting for minute to program load complete')
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')

    driver2 = webdriver.Chrome(driverUrl)

    driver2.implicitly_wait(3)

    driver2.get(b[length - 1])
    body2 = driver2.find_element_by_tag_name("body")

    num_of_pagedowns = 5
    while num_of_pagedowns:
        body2.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)
        num_of_pagedowns -= 1

    delay = 3
    try:
        element = WebDriverWait(driver2, delay).until(
            EC.presence_of_element_located((By.ID, "sections"))
        )
    finally:
        print("Load Complete")
        html2 = driver2.page_source
        bs2 = BeautifulSoup(html2, 'html.parser')
        comments = bs2.select('h2#count> yt-formatted-string')
        # print(comments)

        comments = str(comments).replace(
            """[<yt-formatted-string class="count-text style-scope ytd-comments-header-renderer">댓글 """, "")
        comments = str(comments).replace("""개</yt-formatted-string>]""", "")
        print(comments)


    #print(new_html2)

    #print("싫어요 :", dislike_count)
    #print("좋아요 :", like_count)
    react = "좋아요 :"+ str(like_count) +"/ 싫어요" + str(dislike_count)
    #print(details_tags5)

    print('데이터 베이스에 삽입.')

    #current_time = time.strftime(current_time, '%Y %m %d ')
    # date_time = 2019-08-09 01:28:03

    insertDB(b[length - 1],time.localtime(),c[length - 1],details_tags3,url2,comments,like_count)

    length -= 1
    if length == 1:
        break