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
    return result_sales

def store_dwellings_england_quarter():
    """
    store number of dwellings started and completed in a period of time.
    Three tenures :("PrivateEnterprise","Housing Associations","LocalAuthority" )
    :return:
    """
    sql = sqlpkg.get_area_code()
    area_code = pd.read_sql(sql, ENGINE_ADS, index_col='area_code')
    for year in range(2005,2020):
        for quarter in range(1,5):
            df = pd.read_excel("../data/new_dwelling/LiveTable253a.xlsx", sheet_name=f"{year} Q{quarter}")
            if year < 2014 or (year == 2014 and quarter == 1):
                # 2005 Q1 - 2014 Q1
                df = df.iloc[:, [3, 7, 8, 9, 12, 13, 14]]
            elif year == 2015 or year == 2016 or (year == 2017 and quarter == 1):
                # 2015 Q1 - 2017 Q1
                df = df.iloc[:, [4, 9, 10, 11, 14, 15, 16]]
            else:
                # 2014 Q2 - 2014 Q4     ~
                df = df.iloc[:, [4, 8, 9, 10, 13, 14, 15]]
                # 2017 Q2 - 2019 Q4
                # df = df.iloc[:, [4, 8, 9, 10, 13, 14, 15]]
            df.columns = ["area_code", 'PrivateEnterprise_start', 'HousingAssociations_start', 'LocalAuthority_start', 'PrivateEnterprise_complete', 'HousingAssociations_complete', 'LocalAuthority_complete']
            df = df.dropna(subset = ['PrivateEnterprise_start', 'HousingAssociations_start', 'LocalAuthority_start', 'PrivateEnterprise_complete', 'HousingAssociations_complete', 'LocalAuthority_complete']).reset_index(drop = True)
            df.area_code.iloc[1] = 'E92000001'
            df.drop(0, axis = 0, inplace = True)
            df = df.dropna(subset = ['area_code']).reset_index(drop = True)
            df['new_dwelling_start'] = df.PrivateEnterprise_start+ df.HousingAssociations_start + df.LocalAuthority_start
            df['new_dwelling_complete'] = df.PrivateEnterprise_complete+ df.HousingAssociations_complete + df.LocalAuthority_complete
            df = df.drop(['PrivateEnterprise_start', 'HousingAssociations_start', 'LocalAuthority_start', 'PrivateEnterprise_complete', 'HousingAssociations_complete', 'LocalAuthority_complete'],axis = 1)

            df = df.set_index('area_code').stack().reset_index()
            df.rename({'level_1':'feature_name',0:'feature_value'},axis = 1,inplace = True)
            df.set_index('area_code',inplace = True)
            result = area_code.join(df).drop('area_name', axis=1)
            result['quarter'] = f'Q{quarter}'
            result['year'] = f'{year}'
            result = result.dropna(subset=['feature_name']).reset_index()
            to_sql("features", ENGINE_ADS, result, type="update", chunksize=2000)
            print(f"{year},Q{quarter},success")
            # df = df.groupby(['area_code','year','quarter','feature_name'])['feature_value'].last().unstack(level=3).reset_index()
            # df.to_csv("./data/homeless_england.csv", index=False)
    return  df

def store_total_dwelling_supply():
    """
    store total dwelling provided by local authority
    :return:
    """
    sql = sqlpkg.get_area_code()
    area_code = pd.read_sql(sql, ENGINE_ADS, index_col='area_code')
    df = pd.read_excel("../data/Live_Tables_1006-1009.xlsx", sheet_name='Live Table 1008C')
    df_l = df.iloc[:, [1]]
    df_r = df.iloc[:, 17:31]
    df = df_l.join(df_r)
    df.columns = df.iloc[2].apply(lambda x:x[0:4])
    df = df.rename({"Curr":'area_code'},axis = 1).dropna().reset_index(drop = True)
    df = df.drop(0,axis = 0).replace("..",'None').set_index('area_code')
    df = df.stack().reset_index()
    df.rename({2: 'year', 0: 'feature_value'}, axis=1, inplace=True)
    df = df.set_index('area_code')
    result = area_code.join(df).drop('area_name', axis=1)
    result['quarter'] = 'year'
    result['feature_name'] = 'total_affordable_dwelling_supply'
    result = result.reset_index()
    result.dropna(subset=['area_code','year','feature_name','quarter'],inplace = True)
    to_sql("features", ENGINE_ADS, result, type="update", chunksize=2000)
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
    features = features[['area_code','year','quarter','new_dwelling_start','new_dwelling_complete','homelessness','hpi','sales_volume']]
    features = features.dropna().reset_index(drop = True)
    return features

def fill_missing_data():
    """
       get features and transfer the format to csv (Axial rotation)
       :return:
       """
    sql = sqlpkg.get_features()
    features = pd.read_sql(sql, ENGINE_ADS)
    features = features.fillna('NULL')
    features = features.groupby(['area_code', 'year', 'quarter', 'feature_name'])['feature_value'].last().unstack(
        level=3).reset_index()
    features = features[
        ['area_code', 'year', 'quarter', 'new_dwelling_start', 'new_dwelling_complete', 'homelessness', 'hpi',
         'sales_volume']]
    features = features.dropna().reset_index(drop = True)
    return
if __name__ == '__main__':
    fill_missing_data()
    #1,17-30