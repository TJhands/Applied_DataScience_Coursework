import pandas as pd
import numpy as np
import db_config
from tosql import to_sql
import sqlpkg
import arrow
import math
import matplotlib.pyplot as plt
import matplotlib
from  integrate_data import get_feature_data
ENGINE_ADS = db_config.ENGINE_ADS_COURSEWORK

features=get_feature_data()

filter_homeless=104.5
# filter_sales_volume=554.72
# features=features[~features['homelessness'].isin([0])]
# features=features[features["sales_volume"]<554.72]
#features=features[features["homelessness"]>5000]
#features=features[features["homelessness"]<104.5]

x=features["homelessness"]
#x=features["hpi"]
#x=features["sales_volume"]
print(features.describe())
h=x.hist(bins=100)
plt.show()






























#

#


