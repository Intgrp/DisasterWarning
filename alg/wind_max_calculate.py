# -*- coding: utf-8 -*-
from alg.function import *
import warnings
import pandas as pd
warnings.simplefilter(action="ignore", category=FutureWarning)

def wind_calc(df):
    max_col = ['齿轮箱输入轴轴温(80℃)', '齿轮箱油槽温度(70℃)', '齿轮箱输出轴轴温(80℃)',
               '发电机轴承A温度(80℃)','发电机轴承B温度(80℃)', '主轴齿箱侧温度(60℃)',
               '主轴叶轮侧温度(60℃)', '机舱空气温度(40℃)',
               '机组振动(0.2X轴)', '变频器温度(110℃)']
    avg_col = ['机组平均负荷(千瓦时)', '平均风速(m/s)']
    df = feature(df, max_col, avg_col)
    df = df.reset_index()
    output_col = ['风机名称', '时间', '机舱空气温度(40℃)', '主轴叶轮侧温度(60℃)', '主轴齿箱侧温度(60℃)',
                  '齿轮箱油槽温度(70℃)', '齿轮箱输入轴轴温(80℃)', '齿轮箱输出轴轴温(80℃)',
                  '发电机轴承A温度(80℃)', '发电机轴承B温度(80℃)', '机组平均负荷(千瓦时)',
                  '平均风速(m/s)', '机组振动(0.2X轴)', '变频器温度(110℃)']
    return df[output_col]

if __name__=='__main__':
    threshold_df = pd.read_excel("../ExcelInfo/故障列表提示内容.xls")
    print(threshold_df)

