from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse

def testfunc(request):
    return render(request,'recomm_music/testpage.html',{})

# def test(request):
#     msg = "https://www.youtube.com/embed/a0Q5R4u-G50?autohide=0&autoplay=1&controls=0&disablekb=1&modestbranding=1&rel=0&showinfo=0"
#
#     return render(request,'recomm_music/testpage.html',{'linkurl':msg})


from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests

import re
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys         # 원하는 키를 입력가능


def recomm_link(request):

    # 웹페이지 가져와서 파싱
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    soup = bs(html.text,'html.parser')

    # 이제 변환한 데이터에 find( 태그, { 속성 : 속성값} )
    # 를 사용하여 해당 부분만 추려봅시다.
    data1 = soup.find('p',{'class':'cast_txt'})         # 날씨, 어제와 온도 비교 정보
    # pprint(data1)
    data2 = soup.find('span',{'class':'todaytemp'})     # 현재온도 정보
    # pprint(data2)
    data3 = soup.find('span',{'class':'dday'})          # 현재시간 정보
    data4 = soup.findAll('time')                        # 월 정보

    # 내부 텍스트 추출
    weatherfull = data1.text                            # 날씨, 어제온도와 비교정보
    weather = weatherfull.split(',')[0]                 # 날씨정보만 추출
    temp = data2.text
    timeinfo =data3.text
    month = data4[0].text[5:7]

    keyword_dic = {}

    if '비' in weather :
        keyword_dic['weather'] = weather
    elif '눈' in weather:
        keyword_dic['weather']= weather
    else:
        pass

    if int(month) in range(3,6):
        keyword_dic['season'] = '봄'
    elif int(month) in range(6,9):
        keyword_dic['season'] = '여름'
    elif int(month) in range(9,12):
        keyword_dic['season'] = '가을'
    else:
        keyword_dic['season'] = '겨울'

    if int(timeinfo[:2]) >= 6 and int(timeinfo[:2]) <= 18:
        keyword_dic['time'] = '낮'
    else:
        keyword_dic['time'] = '밤'

    a = keyword_dic.values()
    keyword = list(a)

    # 자동으로 유튜브 키워드 검색하기
    driver = webdriver.Chrome('chromedriver')
    driver.get("https://www.youtube.com/")

    time.sleep(3)               # n초간 프로세스를 일시정지함 > 사이트가 로드될 시간 주기위해

    # 검색어 창을 찾아 search 변수에 저장
    search = driver.find_element_by_xpath('//*[@id="search"]')          # 검색창의 xpath: //*[@id="search"]

    # search 변수에 저장된 곳에 값을 전송
    key = keyword[0] + ' ' +keyword[1]+' '+ '노래'
    search.send_keys(key)
    time.sleep(1)

    #search변수에 저장된 곳에 Enter키를 입력
    search.send_keys(Keys.ENTER)

    time.sleep(2)
    # 클릭
    result1= driver.find_element_by_xpath('//*[@id="video-title"]/yt-formatted-string')
    result1.click()

    prelink = driver.current_url
    linkurl = str(prelink).replace('watch?v=', 'embed/')

    return render(request,'recomm_music/testpage.html',{'linkurl':linkurl})

