import pandas as pd
import numpy as np

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
# print(features.columns)
homeless =features["homelessness"]
coo= df.corrwith(homeless)
print(coo)

# df.plot.scatter(x='hpi', y='sales_volume')


Train,Test = train_test_split(df, train_size = 0.8, random_state=1234)
#y=homelessness
#x=sales_volume+hpi

fit = smf.ols('homelessness~Households_with_one_dependent_child+'
              'Households_with_three_or_more_dependent_children+'
              'Households_with_two_dependent_children+'
              'One_person_households__Female+'
              'One_person_households__Male+'
              'Other_households_with_two_or_more_adults+'
              'Male+'
              'Female+'
              'age_under29', data = Train).fit()
print(fit.summary())


# x=features["homelessness"]
# h=x.hist(bins=100)
# plt.show()

# sns.pairplot(df)
#plt.show()

cm = np.corrcoef(df.values.T)
sns.set(font_scale=1.5)
hm = sns.heatmap(cm,
                 cbar=True,
                 annot=True,
                 square=True,
                 fmt='.2f',
                 annot_kws={'size':15},
                 yticklabels=['hl','nds','ndc','hpi','sv'],
                 xticklabels=['hl','nds','ndc','hpi','sv'])
plt.show()
