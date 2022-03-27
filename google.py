#모듈들 import함
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import os
import time

char = str(input("다운로드 할 것의 검색어 : "))
img_num = int(input("다운로드 받을 사진의 수 : ")) + 1
dir = str(input("이미지를 다운로드 받을 폴더의 이름 : "))
os.mkdir(dir)


#크롬 브라우저로 이미지 검색 링크로 들어감
driver = webdriver.Chrome()
driver.get("https://www.google.co.kr/imghp?hl=ko&ogbl")

#검색창에 들어감
elem = driver.find_element_by_name("q")
#입력값을 검색창에 입력함
elem.send_keys(char)
#엔터를 누름
elem.send_keys(Keys.RETURN)

#이미지를 많이 다운받을 수 있도록 스크롤을 자동으로 내림
SCROLL_PAUSE_TIME = 1
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # 바닥까지 스크롤을 내림
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 페이지가 로드 되는걸 기다림
    time.sleep(SCROLL_PAUSE_TIME)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height: # 스크롤이 끝까지 내려갔다면
        try: #결과 더 보기 버튼 누르기
            driver.find_element_by_css_selector(".mye4qd").click()
        except: #버튼이 없으면 스크롤 내리기 종료
            break
    last_height = new_height

# css 셀렉터가 rg_i Q4LuWd인 이미지를 찾음
images = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")

# 이미지들 다운로드
count = 1
for image in images:
    try:
        image.click() # 이미지를 클릭
        time.sleep(2) # 2초 기다림
        #클릭 한 이미지의 링크를 변수에 집어넣음
        img_URL = driver.find_element_by_css_selector(".n3VNCb").get_attribute("src")
        #클릭 한 이미지의 링크를 이용하여 다운로드 함
        urllib.request.urlretrieve(img_URL, "./"+dir+"/"+str(count)+".jpg")
        count += 1
        # 다운로드 받고 싶은 숫자만큼 다운로드 받았다면 종료
        if count == img_num:
            break
    except: # 만약 오류가 난다면 다음 이미지로 넘어감
        pass

# 브라우저 닫기
driver.close()