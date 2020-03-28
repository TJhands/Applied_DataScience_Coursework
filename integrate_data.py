import pandas as pd
import numpy as np
import db_config
from tosql import to_sql
import sqlpkg
import arrow
ENGINE_ADS = db_config.ENGINE_ADS_COURSEWORK




def store_area_code():
    """
    store standard area code to csv and mysql.
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
    df = pd.read_excel("../data/homelessness/Detailed_LA_Level_Tables_201712.xlsx", sheet_name="Section 1")
    df = df.iloc[4:335, [0, 9, 16, 23]].reset_index(drop=True)
    df.columns = ["area_code", 'N1','N2','N3']
    df.replace(" ",np.nan,inplace = True)
    df = df.dropna(subset = ['N1','N2','N3'])
    # df.area_code.iloc[327] = 'E92000001'
    # df.area_code.iloc[328] = 'E12000007'
    df['feature_name'] = 'homelessness'
    df['quarter'] = 'Q4'
    df['year'] = '2017'
    df.replace("-", 0, inplace=True)
    df.area_code.iloc[-1] = '-'
    # df = df.drop(326, axis=0)
    df['feature_value'] = df.N1+df.N2+df.N3
    df.drop(['N1','N2','N3'],axis = 1,inplace = True)
    df.replace("......", 'None', inplace=True)
    to_sql("features", ENGINE_ADS, df, type="update", chunksize=2000)
    # df = df.groupby(['area_code','year','quarter','feature_name'])['feature_value'].last().unstack(level=3).reset_index()
    # df.to_csv("./data/homeless_england.csv", index=False)
    return

def store_homelessness_england_year():
    """
    store number of households assesses as homelessness. column1+column2+column3
    column1: Homeless + priority need + unintentionally homeless (acceptance)
    column2: Homeless + priority need + intentionally homeless
    column3: Homeless + no priority need
    to csv + mysql
    :return:
    """
    sql = sqlpkg.get_homelessness()
    df = pd.read_sql(sql,ENGINE_ADS)
    df= df.groupby(['feature_name','year','area_code']).sum().reset_index()
    df['quarter'] = 'year'
    to_sql("features", ENGINE_ADS, df, type="update", chunksize=2000)
    # df = df.groupby(['area_code','year','quarter','feature_name'])['feature_value'].last().unstack(level=3).reset_index()
    # df.to_csv("./data/homeless_england.csv", index=False)
    return
def store_hpi_sales():
    """
    store house price index and sales data to mysql.
    Intercept data for the third quarter of 2019.
    :return:
    """
    sql = sqlpkg.get_area_code()
    area_code = pd.read_sql(sql,ENGINE_ADS,index_col='area_code')
    indices = pd.read_csv("../data/HPI/Indices-2019-12.csv").drop('Region_Name',axis=1)
    sales = pd.read_csv("../data/HPI/Sales-2019-12.csv").drop('Region_Name', axis=1)
    # indices.Date = indices.Date.apply(lambda x: arrow.get(x).date())
    # sales.Date = sales.Date.apply(lambda x: arrow.get(x).date())
    for year in range(2018,2020):
        for quarter in range(1,5):
            indices_ = indices.loc[indices['Date'].apply(lambda x: True if x >= arrow.get(f'{year}-{3 * quarter - 2}-01').format("YYYY-MM-DD") and x <= arrow.get(f'{year}-{3 * quarter}-01').format('YYYY-MM-DD') else False)]
            sales_ = sales.loc[sales['Date'].apply(lambda x: True if x >= arrow.get(f'{year}-{3 * quarter - 2}-01').format("YYYY-MM-DD") and x <= arrow.get(f'{year}-{3 * quarter}-01').format('YYYY-MM-DD') else False)]
            indices_ = indices_.groupby('Area_Code').mean()
            sales_ = sales_.groupby('Area_Code').mean()
            result = area_code.join(indices_).drop('area_name',axis = 1)
            result['year'] = '{}'.format(year)
            result['quarter'] = f'Q{quarter}'
            result['feature_name'] = 'hpi'
            result = result.rename({'Index':'feature_value'},axis = 1).reset_index()
            result_sales = area_code.join(sales_).drop('area_name', axis = 1)
            result_sales['year'] = '{}'.format(year)
            result_sales['quarter'] = f'Q{quarter}'
            result_sales['feature_name'] = 'sales_volume'
            result_sales = result_sales.rename({'Sales_Volume': 'feature_value'},axis = 1).reset_index()
            to_sql("features", ENGINE_ADS, result, type="update", chunksize=2000)
            to_sql("features", ENGINE_ADS, result_sales, type="update", chunksize=2000)
    return

def get_feature_data():
    """
    get features and transfer the format to csv (Axial rotation)
    :return:
    """
    sql = sqlpkg.get_features()
    features = pd.read_sql(sql, ENGINE_ADS)
    features = features.groupby(['area_code', 'year', 'quarter', 'feature_name'])['feature_value'].last().unstack(
        level=3).reset_index()
    return
if __name__ == '__main__':
    store_homelessness_england()