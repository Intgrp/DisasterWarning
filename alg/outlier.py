# -*- coding: utf-8 -*-
from alg.weather import *
import os


def outlier(df, folder='input/'):
    name_list = df['风机名称'].values
    fileList = os.listdir(folder)
    ff = {}
    for e in fileList:
        name = e.split('.')[0]
        if name in name_list:
            ff[name] = 0
        else:
            ff[name] = 1
    return ff

def outliersDetectin(df):
    error_list = df[((df['机舱空气温度(40℃)']<0) | (df['机舱空气温度(40℃)']>40)
                     | (df['主轴叶轮侧温度(60℃)']<0) | (df['主轴叶轮侧温度(60℃)']>60)
                     | (df['主轴齿箱侧温度(60℃)']<0) | (df['主轴齿箱侧温度(60℃)']>60)
                     | (df['齿轮箱油槽温度(70℃)']<0) | (df['齿轮箱油槽温度(70℃)']>70)
                     | (df['齿轮箱输入轴轴温(80℃)']<0) | (df['齿轮箱输入轴轴温(80℃)']>80)
                     | (df['齿轮箱输出轴轴温(80℃)']<0) | (df['齿轮箱输出轴轴温(80℃)']>80)
                     | (df['发电机轴承A温度(80℃)']<0) | (df['发电机轴承A温度(80℃)']>80)
                     | (df['发电机轴承B温度(80℃)']<0) | (df['发电机轴承B温度(80℃)']>80)
                     | (df['机组平均负荷(千瓦时)'] < 0) | (df['机组平均负荷(千瓦时)'] > 2050)
                     | (df['平均风速(m/s)']<0) | (df['平均风速(m/s)']>20)
                     | (df['机组振动(0.2X轴)']<-0.12) | (df['机组振动(0.2X轴)']>0.12)
                     | (df['变频器温度(110℃)']<0) | (df['变频器温度(110℃)']>110))]

    return error_list

def fixinfo(df, df_fault):
    w = get_weather()
    if w['status'] != 0:
        return "get next week fail"
    else:
        day = get_near_wind_day(w)
    col_list = df_fault['温度参数'].values
    wind_name_list = df['风机名称'].unique()
    fix = {}
    for wn in wind_name_list:
        fix[wn] = ""
        ss=""
        df_tmp = df[df['风机名称'] == wn]
        for col in col_list:
            line = df_fault.loc[(df_fault['温度参数'] == col)]
            c_min = line['最小值'].values[0]
            c_max = line['最大值'].values[0]
            df_tmp[col] = df_tmp[col].astype(float)
            if df_tmp.loc[(df_tmp[col]<c_min)].empty:
                mmin=0
            else:
                mmin = len(df_tmp.loc[(df_tmp[col]<c_min)])

            if df_tmp.loc[(df_tmp[col]>c_max)].empty:
                mmax=0
            else:
                mmax = len(df_tmp.loc[(df_tmp[col]>c_max)])
            if (mmin>0) or (mmax>0):
                tmp = line['提醒内容'].values[0]
                tmp = str(tmp).replace('X', wn)
                tmp = str(tmp).replace('Y', day)
                ss += tmp+"\n"
        fix[wn] = ss
    return fix

