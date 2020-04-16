import pandas as pd
import numpy as np
import db_config
from tosql import to_sql
import sqlpkg
import arrow
from knnfill import knn_fill_missing
import re
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

def store_population_estimate():
    """
    store Population Estimates for UK, England and Wales, Scotland and Northern Ireland.Provided by administrative area, single year of age and sex.
    :return:
    """
    sql = sqlpkg.get_area_code_england()
    area_code = pd.read_sql(sql, ENGINE_ADS, index_col='area_code')
    df = pd.read_excel('../data/00259ee8-7e0e-406c-b36a-132cbf4315c9.xlsx',sheet_name = 'Dataset')
    df = df.dropna()
    df.columns = df.iloc[0]
    df = df.rename({'Geography':'area_name','Geography code':'area_code'},axis = 1)
    df = df.drop(1,axis = 0).reset_index(drop=True)
    df1 = df[['area_name', 'area_code']]
    df1 = df1[df1['area_code'].apply(lambda x: x.startswith('S'))]
    df1 = df1.drop_duplicates().reset_index(drop = True)
    sql1 = sqlpkg.get_area_code_scotland()
    area_code1 = pd.read_sql(sql1, ENGINE_ADS)
    df1.merge(area_code1,on = 'area_name')

    return

def store_households_estimate_england():
    """
    store households estimate based on2016
    A household is defined as
    one person living alone
    or a group of people (not necessarily related) living at the same address who share cooking facilities and share a living room or sitting room or dining area.
    This includes sheltered accommodation units in an establishment where 50% or more have their own kitchens (irrespective of whether there are other communal facilities)
    and all people living in caravans on any type of site that is their usual residence;
    this will include anyone who has no other usual residence elsewhere in the UK.
    :return:
    """
    df = pd.read_excel('../data/detailedtablesstage1and2/S1 Households.xlsx',sheet_name='Female')
    df = df.iloc[5:,0:20].dropna(axis = 1)
    df.columns = df.columns = df.iloc[0]
    df = df.drop(5,axis = 0).reset_index(drop = True)
    df = df.set_index(['CODE','AREA','AGE GROUP','SEX']).stack().reset_index()
    df.columns = ['area_code','area_name','age_group','category_value','year','value']
    df['category_name'] = 'sex'
    df = df.loc[df.year>= 2011]
    df.year = df.year.apply(lambda x: str(x)[0:4])
    # df1 = df.groupby(['area_code','area_name','year'])['value'].sum().reset_index()
    # df1['age_group'] = 'all'
    # df1['category_name'] = 'total_number'
    # df1['category_value'] = 'total_number'
    to_sql('households',ENGINE_ADS,df)
    # to_sql('households', ENGINE_ADS, df1)
    return df
def nomalise_features():
    """
    normalise homelessness, new_dwelling, sales_volume, affordable_dwelling_supply
    2011-2019 annual
    :return:
    """
    sql1 = sqlpkg.get_features_help_to_buy()
    sql2 = sqlpkg.get_total_households()
    features = pd.read_sql(sql1,ENGINE_ADS,index_col=['area_code','year'])
    households = pd.read_sql(sql2, ENGINE_ADS, index_col=['area_code', 'year'])
    result = features.join(households).dropna()
    result['feature_value_normalised'] = result.feature_value / result.value
    result = result.reset_index().drop('value',axis = 1)
    to_sql('features',ENGINE_ADS,result)
    # sql = sqlpkg.get_features_hpi()
    # hpi = pd.read_sql(sql,ENGINE_ADS)
    # hpi['feature_value_normalised'] = hpi.feature_value
    # to_sql('features', ENGINE_ADS, hpi)
    return
# def knn_fill_missing():
#     features = fill_missing_data()
#     # print(features.describe())
#
#     features = features[
#         ['new_dwelling_start', 'new_dwelling_complete', 'homelessness', 'hpi',
#          'sales_volume']]
#     df = features
#     df = df.replace("NULL", np.nan)
#     print(df)
#     fill_knn = KNN(k=5).fit_transform(df)
#     data = pd.DataFrame(fill_knn)
#     data.columns = ['new_dwelling_start', 'new_dwelling_complete', 'homelessness', 'hpi',
#                     'sales_volume']
#     return (data)
def store_household_features():
    """
    store features related to household type and sex
    household type / total households
    :return:
    """
    sql_all = sqlpkg.get_household_by_all()
    all = pd.read_sql(sql_all,ENGINE_ADS)
    sql_household_type = sqlpkg.get_household_by_househould_type()
    # sql_sex = sqlpkg.get_household_by_sex()
    household = pd.read_sql(sql_household_type,ENGINE_ADS)
    household = household.groupby(['area_code','year','category_value'])['value'].sum().reset_index()
    household.category_value = household.category_value.apply(lambda x: x.replace(' ','_') )
    household.category_value = household.category_value.apply(lambda x: x.replace(':', '_'))
    result = all.merge(household,on= ['area_code','year'],how = 'left')
    result['feature_value_normalised'] = result.value_y / result.value_x
    result['quarter'] = 'Q1'
    result = result.drop('value_x',axis = 1)
    result = result.rename({'category_value':'feature_name','value_y':'feature_value'},axis = 1)
    to_sql('features',ENGINE_ADS,result)
    return

def store_household_age_features():
    """
    store features related to age_group age under 29
    household type / total households
    :return:
    """
    sql_all = sqlpkg.get_household_by_all()
    all = pd.read_sql(sql_all,ENGINE_ADS)
    sql_age = sqlpkg.get_household_by_age()
    household = pd.read_sql(sql_age,ENGINE_ADS)
    household = household.groupby(['area_code','year'])['value'].sum().reset_index()
    result = all.merge(household,on= ['area_code','year'],how = 'left')
    result['feature_value_normalised'] = result.value_y / result.value_x
    result['quarter'] = 'Q1'
    result = result.drop('value_x',axis = 1)
    result['feature_name'] = 'age_under29'
    result = result.rename({'value_y':'feature_value'},axis = 1)
    to_sql('features',ENGINE_ADS,result)
    return

def store_unemployment():
    """
    store unemployment rate
    :return:
    """
    sql_area = sqlpkg.get_area_code()
    area = pd.read_sql(sql_area,ENGINE_ADS)
    area = area[['area_name','area_code']]
    df = pd.read_excel("../data/nomis_2020_04_15_162626.xlsx").dropna()
    df = df.drop(["Unnamed: 2","Unnamed: 4","Unnamed: 6","Unnamed: 8"],axis = 1)
    df.columns = ['area_name','2016','2017','2018','2019']
    df.replace("-",'None',inplace = True)
    df.area_name = df.area_name.apply(lambda x:x.split(':')[1])
    result = area.merge(df, on = 'area_name',how = 'inner' )
    result = result.drop_duplicates().drop('area_name',axis = 1).reset_index(drop = True)
    result = result.set_index('area_code').stack().reset_index()
    result.columns = ['area_code','year','feature_value']
    result['quarter'] = 'Q1'
    result['feature_name'] = 'unemployment'
    result['feature_value_normalised'] = result.feature_value
    to_sql('features',ENGINE_ADS,result)
    return

def store_pay_change():
    """
    store median weekly pay(basic) change
    :return:
    """
    sql_area = sqlpkg.get_area_code()
    area = pd.read_sql(sql_area,ENGINE_ADS)
    area = area[['area_name','area_code']]
    df = pd.read_excel("../data/nomis_2020_04_15_175347.xlsx").dropna()
    df = df.drop(["Unnamed: 2","Unnamed: 4","Unnamed: 6","Unnamed: 8", "Unnamed: 10", "Unnamed: 12"],axis = 1)
    df.columns = ['area_name','male_full_time','male_part_time','female_full_time','female_part_time','full_time','part_time']
    df.replace(["-",'!'],'None',inplace = True)
    df.area_name = df.area_name.apply(lambda x:x.split(':')[1])
    result = area.merge(df, on = 'area_name',how = 'inner')
    result = result.drop_duplicates().drop('area_name',axis = 1).reset_index(drop = True)
    result = result.set_index('area_code').stack().reset_index()
    result.columns = ['area_code','feature_name','feature_value']
    result.feature_value = result.feature_value.apply(lambda x:x / 100 if not isinstance(x,str) else x)
    result['quarter'] = 'Q1'
    result['year'] = '2019'
    result['feature_value_normalised'] = result.feature_value
    to_sql('features',ENGINE_ADS,result)
    result.quarter = 'year'
    to_sql('features', ENGINE_ADS, result)
    return

def get_feature_data_old():
    """
    get features and transfer the format to csv (Axial rotation)
    :return:
    """
    sql = sqlpkg.get_features_nomalised()
    features = pd.read_sql(sql, ENGINE_ADS)
    features = features.groupby(['area_code', 'year', 'quarter', 'feature_name'])['feature_value'].last().unstack(
        level=3).reset_index()
    features = features[['area_code','year','quarter','new_dwelling_start','new_dwelling_complete','homelessness','hpi','sales_volume']]
    features = features.dropna().reset_index(drop = True)
    features.new_dwelling_start = features.new_dwelling_start / max(features.new_dwelling_start)
    features.new_dwelling_complete = features.new_dwelling_complete / max(features.new_dwelling_complete)
    features.homelessness = features.homelessness / max(features.homelessness)
    features.hpi = features.hpi / max(features.hpi)
    features.sales_volume = features.sales_volume / max(features.sales_volume)
    return features

def get_feature_data():
    """
    get features and transfer the format to csv (Axial rotation)
    :return:
    """
    sql = sqlpkg.get_features_nomalised()
    features = pd.read_sql(sql, ENGINE_ADS)
    features = features.fillna('NULL')
    features = features.groupby(['area_code', 'year', 'quarter', 'feature_name'])['feature_value'].last().unstack(
        level=3).reset_index()
    features = features[['area_code','year','quarter',
                         'homelessness',
                         'hpi',
                         'sales_volume',
                         'new_dwelling_start',
                         'new_dwelling_complete',
                         'Households_with_one_dependent_child',
                         'Households_with_three_or_more_dependent_children',
                         'Households_with_two_dependent_children',
                         'One_person_households__Female',
                         'One_person_households__Male',
                         'Other_households_with_two_or_more_adults',
                         'Male',
                         'Female',
                         'age_under29',
                         'unemployment',
                         'male_full_time',
                         'male_part_time',
                         'female_full_time',
                         'female_part_time',
                         'full_time',
                         'part_time',
                         'help_to_buy']]
    features = features.dropna().reset_index(drop = True)

    # fill null value
    data = knn_fill_missing(features.iloc[:,3:])
    data.homelessness = data.homelessness / data.homelessness.max()
    data.hpi = data.hpi / data.hpi.max()
    data.new_dwelling_start = data.new_dwelling_start / data.new_dwelling_start.max()
    data.new_dwelling_complete = data.new_dwelling_complete / data.new_dwelling_complete.max()
    data.sales_volume = data.sales_volume / data.sales_volume.max()
    data.unemployment = data.unemployment / 100
    data.help_to_buy = data.help_to_buy / data.help_to_buy.max()
    return data
def get_feature_data_scotland():
    """
    get features and transfer the format to csv (Axial rotation) scotland
    :return:
    """
    sql = sqlpkg.get_features_nomalised_scotland()
    features = pd.read_sql(sql, ENGINE_ADS)
    features = features.fillna('NULL')
    features = features.groupby(['area_code', 'year', 'quarter', 'feature_name'])['feature_value'].last().unstack(
        level=3).reset_index()
    features = features.dropna().reset_index(drop = True)

    # fill null value
    # data = knn_fill_missing(features.iloc[:,3:])
    # data.homelessness = data.homelessness / data.homelessness.max()
    result = features.iloc[:,3:]
    return result


if __name__ == '__main__':
    nomalise_features()
    #1,17-30