# -*- coding: utf-8 -*-
import requests
import re
import json
import datetime

def windguru_get():
    url = 'https://old.windguru.cz/int/index.php?sc=694741'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    #https://www.windguru.cz/694741
    result = re.findall(r"wg_fcst_tab_data_\d = ([^;]*)", response.text)
    # result = re.findall(r"(wg_fcst_tab_data_1 = )([\s\S]*)(;\nvar wgopts_1){1}", response.text)
    data_json = json.loads(result[0])
    fcst = data_json['fcst']['3']
    initdate= fcst['initdate']
    dy = datetime.datetime.strptime(initdate, '%Y-%m-%d %H:%M:%S').date()
    dt = [str(dy), fcst['hr_weekday'], fcst['hr_d'], fcst['hr_h']]
    out = [dt, fcst['WINDSPD'], fcst['GUST'], fcst['WINDDIR'], fcst['TMP']]
    return out

if __name__=='__main__':
    url = 'https://old.windguru.cz/int/index.php?sc=694741'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    result = re.findall(r"wg_fcst_tab_data_\d = ([^;]*)", response.text)
    # print(response.text)
    data_json = json.loads(result[0])
    print(data_json['fcst']['3'])
    # fcst = data_json['fcst']
    # tmp = fcst['3']['TMP']
    # tcdc = fcst['3']['TCDC']
    # hcdc = fcst['3']['HCDC']
    # mcdc = fcst['3']['MCDC']
    # lcdc = fcst['3']['LCDC']
    # rh = fcst['3']['RH']
    # gust = fcst['3']['GUST']
    # slp = fcst['3']['SLP']
    # flhgt = fcst['3']['FLHGT']
    # apcp = fcst['3']['APCP']
    # windspd = fcst['3']['WINDSPD']
    # winddir = fcst['3']['WINDDIR']
    # smern = fcst['3']['SMERN']
    # tmpe = fcst['3']['TMPE']
    # pcpt = fcst['3']['PCPT']
    # hr_weekday = fcst['3']['hr_weekday']
    # hr_h = fcst['3']['hr_h']
    # hr_d = fcst['3']['hr_d']
    # hours = fcst['3']['hours']
    # vars = fcst['3']['vars']
    # initdate = fcst['3']['initdate']
    # init_d = fcst['3']['init_d']
    # init_dm = fcst['3']['init_dm']
    # init_h = fcst['3']['init_h']
    # initstr = fcst['3']['initstr']
    # model_name = fcst['3']['model_name']
    # model_longname = fcst['3']['model_longname']
    # id_model = fcst['3']['id_model']
    # update_last = fcst['3']['update_last']
    # update_next = fcst['3']['update_next']
    # img_param = fcst['3']['img_param']
    # img_var_map = fcst['3']['img_var_map']
