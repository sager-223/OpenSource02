import re

from pymongo import MongoClient
import pandas as pd
import numpy as np
import pymysql

def pre_process(df):
    """
    数据预处理函数
    :param df: dataFrame
    :return: df
    """

    # 将数据中车的行驶路程单位万公里去掉 方便后续计算 比如：1.2万公里
    df['car_run'] = df['car_run'].apply(lambda x:x.split('万公里'))

    # 将数据中car_push字段中有未上牌的数据删除
    df['car_push'] = df['car_push'].apply(lambda x:x if not x=="未上牌" else np.nan)

    # 删除字段中存在有NAN的数据
    df.dropna(inplace=True)

    return df



def car_brand_count_top10(df):
    """
    计算不同品牌的数量的前十名
    :param df: dataFrame
    :return: df
    """
    # 按照汽车的品牌进行分类
    grouped = df.groupby('car_series')['car_run'].count().reset_index().sort_values(by="car_run",ascending=False)[:10]
    data = [[i['car_series'],i['car_run']] for i in grouped.to_dict(orient="records")]
    print(data)
    return data

def car_use_year_count(df):
    """
    计算二手车的使用时间
    :param df: dataFrame
    :return: df
    """
    # 处理汽车的变卖时间
    date = pd.to_datetime(df['car_push'])
    date_value = pd.DatetimeIndex(date)
    df['car_push_year'] = date_value.year
    # 转换数据类型为int
    df['car_time_style'] = df['car_time_style'].astype(np.int)
    df['car_push_year'] = df['car_push_year'].astype(np.int)
    df['cae_use_year'] = df['car_push_year']-df['car_time_style']
    # 对车的使用年限进行分类
    grouped = df.groupby('cae_use_year')['car_series'].count().reset_index()
    # 将使用年限为负的字段删除 并根据使用年限进行分组  分为 <一年 一年~三年 >三年
    grouped = grouped.query('cae_use_year>=0')
    grouped.loc[:,'cae_use_year'] = grouped.loc[:,'cae_use_year'].apply(lambda x:"<一年" if x==0 else x )
    grouped.loc[:,'cae_use_year'] = grouped.loc[:,'cae_use_year'].apply(lambda x:"一年~三年" if not x =='<一年' and x>0 and x<3 else x )
    grouped.loc[:,'cae_use_year'] = grouped.loc[:,'cae_use_year'].apply(lambda x:">三年" if not x =='<一年' and not x=="一年~三年" and x>=3 else x )
    # 再根据不同使用年限进行分组
    grouped_use_year = grouped.groupby('cae_use_year')['car_series'].sum().reset_index()
    data = [[i['cae_use_year'],i['car_series']] for i in grouped_use_year.to_dict(orient="records")]
    print(data)
    return data

def car_place_count(df):
    """
    计算不同地区的二手车数量
    :param df: dataFrame
    :return: df
    """
    grouped =  df.groupby('car_place')['car_series'].count().reset_index()
    data = [[i['car_place'],i['car_series']] for i in grouped.to_dict(orient="records")]
    print(data)
    return data

def car_month_count(df):
    """
    计算每个月的二手车数量
    :param df: dataFrame
    :return: df
    """
    # 处理汽车的变卖时间
    date = pd.to_datetime(df['car_push'])
    date_value = pd.DatetimeIndex(date)
    month = date_value.month
    df['car_push_month'] = month

    # 对汽车变卖的月份进行分组
    grouped = df.groupby('car_push_month')['car_series'].count().reset_index()
    data = [[i['car_push_month'],i['car_series']] for i in grouped.to_dict(orient="records")]
    print(data)
    return data

def save(cursor,sql,data):
    result = cursor.executemany(sql,data)
    if result:
        print('插入成功')

if __name__ == '__main__':
    # 1 从MongoDB中获取数据
    # 初始化MongoDB数据连接
    # client = MongoClient()
    # collections = client['test']['car_home']
    # 获取MongoDB数据
    # cars = collections.find({},{'_id':0})

    # 2 读取xlsx文件数据（已将MongoDB中数据转换成xlsx格式）
    cars = pd.read_excel('./carhome.xlsx',engine='openpyxl')

    # 将数据转换成dataFrame类型
    df = pd.DataFrame(cars)
    print(df.info())
    print(df.head())

    # 对数据进行预处理
    df = pre_process(df)

    # 计算不同品牌的数量的前十名
    data1 = car_brand_count_top10(df)

    # 计算二手车的使用时间
    data2 = car_use_year_count(df)

    # 计算不同地区的二手车数量
    data3 = car_place_count(df)

    # 计算每个月的二手车数量
    data4 = car_month_count(df)

    # 创建mysql连接
    conn = pymysql.connect(user='root',password='123456',host='localhost',port=3306,database='car_home',charset='utf8')
    try:
        with conn.cursor() as cursor:
            # 计算不同品牌的数量的前十名
            sql1 = 'insert into db_car_brand_top10(brand,count) values(%s,%s)'
            save(cursor,sql1,data1)

            # 计算二手车的使用时间
            sql2 = 'insert into db_car_area(area,count) values(%s,%s)'
            save(cursor,sql2,data2)

            # 计算不同地区的二手车数量
            sql3 = 'insert into db_car_use_year(year_area,count) values(%s,%s)'
            save(cursor, sql3, data3)

            # 计算每个月的二手车数量
            sql4 = 'insert into db_car_month(month,count) values(%s,%s)'
            save(cursor,sql4,data4)

            conn.commit()
    except pymysql.MySQLError as error:
        print(error)
        conn.rollback()