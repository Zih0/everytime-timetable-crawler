from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time


time_url = 'https://everytime.kr/timetable'
login_url = 'https:/everytime.kr/login'

driver = webdriver.Chrome('./chromedriver') # chromedriver 경로
driver.implicitly_wait(3)
driver.get(login_url)
driver.find_element_by_name('userid').send_keys('') # 에브리타임 ID
driver.find_element_by_name('password').send_keys('') #에브리타임 PW
driver.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()
driver.get(time_url)
driver.find_element_by_xpath('//*[@id="container"]/ul/li[1]').click()
scr1 = driver.find_element_by_xpath('//*[@id="subjects"]/div[2]')
#이전 스크롤 길이 재기
last_height = driver.execute_script("return arguments[0].scrollHeight",scr1)

while True:
    # 스크롤 시 데이터 불러오는 시간
    time.sleep(5)
    #데이터 불러오고 스크롤 길이 다시 재기
    new_height = driver.execute_script("return arguments[0].scrollTop = arguments[0].scrollHeight ",scr1)
    #스크롤 길이가 같으면, 모든 데이터를 불러왔으므로 break
    if new_height == last_height:
        break
    last_height = new_height

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
tmp = soup.select('.list tbody tr')
contents = []
for i in tmp:
    # 필요없는 정보는 주석 처리
    contents.append(
    {'학년' : i.select_one('td:nth-child(1)').text,
     '이수구분' : i.select_one('td:nth-child(2)').text,
     '과목번호-분반' : i.select_one('td:nth-child(3)').text,
     '과목명': i.select_one('td:nth-child(4)').text,
     '담당교수': i.select_one('td:nth-child(5)').text,
     '학점': i.select_one('td:nth-child(6)').text,
     '시간': i.select_one('td:nth-child(7)').text,
     '강의실': i.select_one('td:nth-child(8)').text,
     '담은인원': i.select_one('td:nth-child(10)').text,
     '전공': i.select_one('td:nth-child(11)').text,
     '유의사항': i.select_one('td:nth-child(12)').text,
     })

driver.close()
print("수집완료")
df = pd.DataFrame(contents)
df.to_excel('대학교 강의목록.xlsx',encoding='utf-8')
