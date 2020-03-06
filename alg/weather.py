# -*- coding: utf-8 -*-
import urllib.request, urllib.parse
import json

def get_weather():
    city = "福清"
    code_url = "https://jisutqybmf.market.alicloudapi.com"
    path = '/weather/query'
    appcode = '2049d944ddfb4616bbc77ea1ff98ed1a'
    parameter = urllib.parse.urlencode({"city": city})
    url = code_url + path + "?" + parameter
    request = urllib.request.Request(url)
    request.add_header("Authorization", "APPCODE " + appcode)
    request.encoding = 'utf-8'
    ret = json.loads(urllib.request.urlopen(request).read().decode("utf8", errors='ignore'))
    return ret

def get_near_wind_day(data):
    day_list = data['result']['daily']
    print(day_list)
    for each in day_list:
        wind = each['day']['windpower']
        if "无风" in wind or "软风" in wind or "轻风" in wind or "微风" in wind or "和风" in wind:
            return each['week'][2]
        elif int(wind[-2]) < 5:
            return each['week'][2]
    return "*"


if __name__ == "__main__":
    output = get_weather()
    print(output)