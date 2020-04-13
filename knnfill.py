import pandas as pd
import numpy as np
# from  integrate_data import fill_missing_data
from fancyimpute import KNN

pd.set_option('display.max_columns', 500)
def knn_fill_missing(df):
    df = df.replace("NULL", np.nan)
    # print(df)
    fill_knn = KNN(k=5).fit_transform(df)
    data = pd.DataFrame(fill_knn)
    data.columns = df.columns
    return (data)
# f=knn_fill_missing()
# print(f)


if __name__ == '__main__':
    a = pd.DataFrame([[1,2,1,1],[2,3,4,2],[12,'NULL',21,1],[1,12,"NULL",1]],columns = ['a','b','c','d'])
    data = knn_fill_missing(a)
    print()