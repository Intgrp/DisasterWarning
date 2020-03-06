# -*- coding: utf-8 -*-
from pandas.io.parsers import read_csv
import pandas.core.indexes.base

import os
import sys


def readFiles(folder='input/'):
    fileList = os.listdir(folder)
    df=pandas.DataFrame()
    for file in fileList:
        tmp = read_csv(folder + file, skiprows=1, encoding='gbk')
        tmp['风机名称'] = file.split('.')[0]
        df = df.append(tmp)
    return df

def readAXX(datapath):
    if not os.path.exists(datapath):
        sys.exit()
    df = readFiles(folder=datapath)
    data_col = ['风机名称', '描述', '电能质量模块检测有功',
                '齿轮箱输入轴轴温', '齿轮箱油槽温度', '齿轮箱输出轴轴温', '发电机轴承A温度',
                '发电机轴承B温度', '主轴齿箱侧温度', '主轴叶轮侧侧温度', '机舱空气温度',
                '机舱X轴振动值', '变频器IGBT温度', '风速1']
    df = df[data_col]
    df['描述'] = pandas.to_datetime(df['描述'])  # 设置时间那列为日期格式
    df['时间'] = df['描述'].dt.date  # 新建一列date，只保留年月日信息
    df.rename(columns={'机舱空气温度': '机舱空气温度(40℃)',
                       '主轴叶轮侧侧温度': '主轴叶轮侧温度(60℃)',
                       '主轴齿箱侧温度': '主轴齿箱侧温度(60℃)',
                       '齿轮箱油槽温度': '齿轮箱油槽温度(70℃)',
                       '齿轮箱输入轴轴温': '齿轮箱输入轴轴温(80℃)',
                       '齿轮箱输出轴轴温': '齿轮箱输出轴轴温(80℃)',
                       '发电机轴承A温度': '发电机轴承A温度(80℃)',
                       '发电机轴承B温度': '发电机轴承B温度(80℃)',
                       '电能质量模块检测有功': '机组平均负荷(千瓦时)',
                       '风速1': '平均风速(m/s)',
                       '机舱X轴振动值': '机组振动(0.2X轴)',
                       '变频器IGBT温度': '变频器温度(110℃)'}, inplace=True)
    return df

def feature(df,max_col,avg_col):
    out = df.groupby(['风机名称','时间'])[max_col].max()
    out[avg_col] = df.groupby(['风机名称', '时间'])[avg_col].mean()
    return out


