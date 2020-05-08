from integrate_data import get_feature_data,get_feature_data_labeled
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
def neural_network():
    df = get_feature_data_labeled()

    y = df[['homelessness']].values
    X = df.drop('homelessness',axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size = 0.33, random_state = 42)
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
    hidden_layer_sizes = (5, 2), random_state = 1)
    clf.fit(X_train, y_train)
    score = clf.score(X_test,y_test)
    return

if __name__ == '__main__':
    neural_network()