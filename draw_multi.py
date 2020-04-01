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
from  integrate_data import get_feature_data
import seaborn as sns
import statsmodels.formula.api as smf



pd.set_option('display.max_columns', 500)


features=get_feature_data()
print(features.describe())
# features=features[features["homelessness"]<104.5]

df=features
df= features[['homelessness','new_dwelling_start','new_dwelling_complete','hpi','sales_volume']]
# print(features.columns)
homeless =features["homelessness"]
coo= df.corrwith(homeless)
print(coo)

# df.plot.scatter(x='hpi', y='sales_volume')


Train,Test = train_test_split(df, train_size = 0.8, random_state=1234)
#y=homelessness
#x=sales_volume+hpi

fit = smf.ols('homelessness~sales_volume+hpi+hpi+new_dwelling_start+new_dwelling_complete', data = Train).fit()
print(fit.summary())


# x=features["homelessness"]
# h=x.hist(bins=100)
# plt.show()

sns.pairplot(df)
#plt.show()
