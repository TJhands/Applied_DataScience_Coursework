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

fit = smf.ols('homelessness~'
              'hpi+'
              'sales_volume+'
              'new_dwelling_start+'
              'new_dwelling_complete+'
              'Households_with_one_dependent_child+'
              'Households_with_three_or_more_dependent_children+'
              'Households_with_two_dependent_children+'
              'One_person_households__Female+'
              'One_person_households__Male+'
              'Other_households_with_two_or_more_adults+'
              'Male+'
              'Female+'
              'age_under29+'
              'unemployment+'
              'male_full_time+'
              'male_part_time+'
              'female_full_time+'
              'female_part_time+'
              'full_time+'
              'part_time+'
              'help_to_buy'
              , data = Train).fit()
print(fit.summary())


# x=features["homelessness"]
# h=x.hist(bins=100)
# plt.show()

# sns.pairplot(df)
# plt.show()
ndf=df[['homelessness','hpi',
                         'Households_with_one_dependent_child',
                         'Households_with_three_or_more_dependent_children',
                         'One_person_households__Male',
                         'Other_households_with_two_or_more_adults',
                         'Male',
                         'age_under29',
                         'unemployment',
        ]]
rdf1=df[['homelessness',
                         'Households_with_one_dependent_child',
                         'Households_with_three_or_more_dependent_children',
                         'Other_households_with_two_or_more_adults',

        ]]
rdf1.columns = ['homelessness','h1c','h2c','h2a']
sns.pairplot(rdf1)
plt.show()

rdf2=df[['homelessness','hpi',
                         'unemployment'
        ]]
sns.pairplot(rdf2)
# plt.show()

rdf3=df[['homelessness',
                         'Male',
                         'age_under29'
        ]]

sns.pairplot(rdf3)
# plt.show()


# 真实值与预测值的关系# 设置绘图风格
plt.style.use('ggplot')
# 设置中文编码和负号的正常显示
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'

# 散点图plt.scatter(Test.sales, pred, label = '观测点')
# 回归线
plt.plot([Test.sales.min(), Test.sales.max()], [pred.min(), pred.max()], 'r--', lw=2, label = '拟合线')

# 添加轴标签和标题
plt.title('真实值VS.预测值')
plt.xlabel('真实值')
plt.ylabel('预测值')

# 去除图边框的顶部刻度和右边刻度
plt.tick_params(top = 'off', right = 'off')
# 添加图例
plt.legend(loc = 'upper left')
# 图形展现
plt.show()


cm = np.corrcoef(ndf.values.T)
sns.set(font_scale=1.5)
hm = sns.heatmap(cm,
                 cbar=True,
                 annot=True,
                 square=True,
                 fmt='.2f',
                 annot_kws={'size':12},
                 yticklabels=['hl','hpi','h1c','h2c','1hm','h2a','Male','a29','ur'],
                 xticklabels=['hl','hpi','h1c','h2c','1hm','h2a','Male','a29','ur'])
# plt.show()

