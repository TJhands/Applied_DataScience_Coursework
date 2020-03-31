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

ENGINE_ADS = db_config.ENGINE_ADS_COURSEWORK

pd.set_option('display.max_columns', 500)
sql = sqlpkg.get_features()
features = pd.read_sql(sql, ENGINE_ADS)
features = features.groupby(['area_code', 'year', 'quarter', 'feature_name'])['feature_value'].last().unstack(
        level=3).reset_index()
features=features.dropna()
print((features))
print(features.describe())
features=features[features["sales_volume"]<554.72]
features=features[features["homelessness"]<104.5]
features=features[features['new_dwelling_complete']<290]
#features=features[features['PrivateEnterprise_complete']<230]
#features=features[features['HousingAssociations_complete']<75]
df=features
print(features.columns)
homeless =features["homelessness"]
coo= df.corrwith(homeless)
print(coo)


df=df[["homelessness",'hpi','sales_volume','new_dwelling_complete','PrivateEnterprise_complete','LocalAuthority_complete','HousingAssociations_complete']]
#df.plot.scatter(x='hpi', y='sales_volume')

Train,Test = train_test_split(df, train_size = 0.8, random_state=1234)
fit = smf.ols('homelessness~sales_volume', data = Train).fit()
print(fit.summary())

sns.pairplot(df)
# plt.show()
