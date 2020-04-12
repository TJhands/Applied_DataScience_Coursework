import pandas as pd
import numpy as np
from pandas._config import display
import db_config
from tosql import to_sql
import sqlpkg
import arrow
import math
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import matplotlib
from  integrate_data import fill_missing_data
import seaborn as sns
import statsmodels.formula.api as smf
from fancyimpute import KNN
pd.set_option('display.max_columns', 500)
def knn_fill_missing():
    features = fill_missing_data()
    # print(features.describe())

    features = features[
        ['new_dwelling_start', 'new_dwelling_complete', 'homelessness', 'hpi',
         'sales_volume']]
    df = features
    df = df.replace("NULL", np.nan)
    print(df)
    fill_knn = KNN(k=5).fit_transform(df)
    data = pd.DataFrame(fill_knn)
    data.columns = ['new_dwelling_start', 'new_dwelling_complete', 'homelessness', 'hpi',
                    'sales_volume']
    return (data)
# f=knn_fill_missing()
# print(f)



