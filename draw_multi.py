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

# df=features
df= features[['homelessness','new_dwelling_start','new_dwelling_complete','hpi','sales_volume']]
# print(features.columns)
df.columns = ['hl','nds','ndc','hpi','sv']
homeless =df["hl"]
coo= df.corrwith(homeless)
print(coo)

# df.plot.scatter(x='hpi', y='sales_volume')


Train,Test = train_test_split(df, train_size = 0.8, random_state=1234)
#y=homelessness
#x=sales_volume+hpi

fit = smf.ols('hl~sv+hpi+hpi+nds+ndc', data = Train).fit()
print(fit.summary())

pred = fit.predict(exog = Test)
RMSE = np.sqrt(mean_squared_error(Test.hl, pred))
# x=features["homelessness"]
# h=x.hist(bins=100)
# plt.show()
# 真实值与预测值的关系# 设置绘图风格
plt.style.use('ggplot')
# 设置中文编码和负号的正常显示
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'

plt.scatter(Test.hl, pred)
# 回归线
# plt.plot([Test.homelessness.min(), Test.homelessness.max()], [pred.min(), pred.max()], 'r--', lw=2, label = '拟合线')

# 添加轴标签和标题
plt.title('True value VS. Predicted Value')
plt.xlabel('True Value')
plt.ylabel('Predictive Value')

# 去除图边框的顶部刻度和右边刻度
plt.tick_params(top = 'off', right = 'off')
# # 添加图例
# 图形展现
plt.savefig('./result.png')
plt.show()
sns.pairplot(df)
plt.savefig('./result1.png')
plt.show()
