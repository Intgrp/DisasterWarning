# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


def getHTML(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getLocation(html):
    soup = BeautifulSoup(html, 'html.parser')
    paras = soup.select('.topbar h2')
    return paras


def getWeather(html):
    soup = BeautifulSoup(html, 'html.parser')
    paras = soup.select('.weather_week .txt')
    return paras


def getWet(html):
    soup = BeautifulSoup(html, 'html.parser')
    paras = soup.select('.b2')
    return paras


def getWind(html):
    soup = BeautifulSoup(html, 'html.parser')
    paras = soup.select('.b3')
    return paras

def getToday(html):
    soup = BeautifulSoup(html, 'html.parser')

    city = soup.select('.hhx_index_newHead_l text')[0].get_text()
    date = soup.select('.date')[0].get_text()
    nowtemp = soup.select('.temp .now')[0].get_text()
    weather = soup.select('.temp .txt')[0].get_text()
    wet = soup.select('.info .b2')[0].get_text()
    wind = soup.select('.info .b3')[0].get_text()

    # for t in text:
    #     if len(t) > 0:
    #         # f.writelines(t.get_text() + "\n")
    #         print(t.get_text() + "\n")

    #福清市: 2020-02-02 星期日, 天气多云，当前温度13℃, 整日温度范围:9~17℃ ,风速：0.9，风向：西北风 1级
    ss = city+":"+date+"，当前温度："+nowtemp+" ，天气" + weather + "，风向：" +wind
    return ss



def saveFile(text):
    # f = open('weather.txt', mode='a', encoding='utf-8')
    for t in text:
        if len(t) > 0:
            # f.writelines(t.get_text() + "\n")
            print(t.get_text() + "\n")
    # f.close()


def getAll(url):
    html = getHTML(url)
    today = getToday(html)
    print(today)
    # location = getLocation(html)
    # weather = getWeather(html)
    # wet = getWet(html)
    # wind = getWind(html)

    # print(location.get_text())
    # print(weather.get_text())
    # print(wet.get_text())
    # print(wind.get_text())
    # saveFile(location)
    # saveFile(weather)
    # saveFile(wet)
    # saveFile(wind)


def main():
    beijing = 'https://m.tianqi.com/beijing/'
    changsha = 'https://m.tianqi.com/changsha/'
    fuqing = 'https://m.tianqi.com/fuqing/'
    getAll(fuqing)


# main()