import pandas as pd
import numpy as np
import db_config
from tosql import to_sql
ENGINE_ADS = db_config.ENGINE_ADS_COURSEWORK




def store_area_code():
    """
    store standard area code to csv and mysql
    :return:
    """
    df = pd.read_excel("../data/DetailedLA_201909.xlsx",sheet_name="A1")
    df = df.iloc[:, [0, 1]].dropna().reset_index(drop=True)[0:329]
    df.columns = ["area_code", 'area_name']
    df.to_csv("./data/area_code.csv",index=False)
    to_sql("areacode",ENGINE_ADS,df, type="update", chunksize=2000)
    return

def store_homelessness_england():
    """
    store number of households assesses as homelessness. column1+column2+column3
    column1: Homeless + priority need + unintentionally homeless (acceptance)
    column2: Homeless + priority need + intentionally homeless
    column3: Homeless + no priority need
    to csv + mysql
    :return:
    """
    df = pd.read_excel("../data/DetailedLA_201909.xlsx", sheet_name="MD1")
    df = df.iloc[:, [0,5, 6, 7]].dropna().reset_index(drop=True)
    df.columns = ["area_code", 'N1','N2','N3']
    df['feature_name'] = 'homelessness'
    df['quarter'] = 'Q3'
    df['year'] = '2019'
    df['feature_value'] = df.N1+df.N2+df.N3
    df.replace("......",'None',inplace = True)
    df.drop(['N1','N2','N3'],axis = 1,inplace = True)
    to_sql("features", ENGINE_ADS, df, type="update", chunksize=2000)
    df = df.groupby(['area_code','year','quarter','feature_name'])['feature_value'].last().unstack(level=3).reset_index()
    df.to_csv("./data/homeless_england.csv", index=False)
    return



if __name__ == '__main__':
    store_homelessness_england()