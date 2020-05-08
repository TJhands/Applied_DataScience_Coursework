from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
import pandas as pd
from sklearn.cluster import KMeans
from integrate_data import get_feature_data,get_feature_data_labeled
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.metrics import  silhouette_score
import random
def xmeansCluster(data):
    initial_centers = kmeans_plusplus_initializer(data, 2).initialize()
    xmeans_instance = xmeans(data, initial_centers, 20)
    xmeans_instance.process()
    clusters = xmeans_instance.get_clusters()
    centers = xmeans_instance.get_centers()

    # visualizer = cluster_visualizer_multidim()
    # visualizer.append_clusters(clusters, data)
    # # visualizer.append_cluster(centers, None, marker='*', markersize=10)
    # visualizer.show()
    return clusters

def cluster(docvectors):
    km = KMeans(n_clusters=4).fit(docvectors)
    return km.labels_

def show_data():
    df = get_feature_data()
    # df = df[['homelessness', 'Male', 'hpi', 'Households_with_one_dependent_child',
    #          'Households_with_three_or_more_dependent_children', 'Other_households_with_two_or_more_adults'
    #     , 'One_person_households__Male', 'age_under29', 'unemployment']]
    vector = df.values
    # labels = cluster(vector)
    # data['label'] = labels
    labels_ = xmeansCluster(vector)
    label = pd.DataFrame(labels_).stack().reset_index(level=1, drop=True).rename('A').to_frame()
    label['label'] = label.index
    label.sort_values(by='A', inplace=True)
    label.set_index('A', inplace=True)
    df = df.join(label)
    tsne = TSNE(random_state=1234)
    a = tsne.fit_transform(vector)
    # a = np.load("tsne_doc2vec_exetools_post.npy",allow_pickle=True)
    result = pd.DataFrame(a)
    d1 = result[df['label'] == 0]
    d2 = result[df['label'] == 1]
    d3 = result[df['label'] == 2]
    d4 = result[df['label'] == 3]
    d5 = result[df['label'] == 4]
    d6 = result[df['label'] == 5]
    d7 = result[df['label'] == 6]
    d8 = result[df['label'] == 7]
    plt.plot(d1[0], d1[1], 'r.', d2[0], d2[1], 'g.', d3[0], d3[1], 'b.',d4[0],d4[1],'y.',
             d5[0], d5[1], 'c.', d6[0], d6[1], 'm.', d7[0], d7[1], 'k.',d8[0],d8[1],'pink')
    plt.xlabel('compressed dimension 1')
    plt.ylabel('compressed dimension 2')
    plt.title('xmeans with 8 clusters')
    plt.savefig('xmeans.png')
    plt.show()
def pair_plot():
    df = get_feature_data()
    df = df[['homelessness','Male','hpi','Households_with_one_dependent_child','Households_with_three_or_more_dependent_children','Other_households_with_two_or_more_adults'
             ,'One_person_households__Male','age_under29','unemployment']]
    vector = df.values
    # labels = cluster(vector)
    # data['label'] = labels
    labels_ = xmeansCluster(vector)
    label = pd.DataFrame(labels_).stack().reset_index(level=1, drop=True).rename('A').to_frame()
    label['label'] = label.index
    label.sort_values(by='A', inplace=True)
    label.set_index('A', inplace=True)
    df_ = df.join(label)
    tsne = TSNE()
    # a = tsne.fit_transform(vector)
    # # a = np.load("tsne_doc2vec_exetools_post.npy",allow_pickle=True)
    # result = pd.DataFrame(a)
    df.columns = [0,1]
    d1 = df[df_['label'] == 0]
    d2 = df[df_['label'] == 1]
    d3 = df[df_['label'] == 2]
    d4 = df[df_['label'] == 3]
    d5 = df[df_['label'] == 4]
    d6 = df[df_['label'] == 5]
    plt.plot(d1[0], d1[1], 'r.', d2[0], d2[1], 'g.', d3[0], d3[1], 'b.',d4[0], d4[1], 'c.', d5[0], d5[1], 'm.', d6[0], d6[1], 'y.')
    plt.xlabel('compressed dimension 1')
    plt.ylabel('compressed dimension 2')
    plt.show()

def kmeans_number():
    clusters = [2,3,4,5,6,7,8,9,10,11,12]
    df = get_feature_data()
    # df = df[['homelessness', 'Male', 'hpi', 'Households_with_one_dependent_child',
    #          'Households_with_three_or_more_dependent_children', 'Other_households_with_two_or_more_adults'
    #     , 'One_person_households__Male', 'age_under29', 'unemployment']]
    vector = df.values
    for i in clusters:
        km = KMeans(n_clusters=i).fit_predict(vector)
        silhouette_avg = silhouette_score(vector, km)
        print(i,'score:',silhouette_avg)

def km():
    df_ = get_feature_data()
    for i in range(20):
        resultList = random.sample(range(1, 22), 4)
        resultList.append(0)
        df = df_.iloc[:,resultList]
        # df_= df[['homelessness']]
        # df = df.drop('homelessness',axis = 1)
        vector = df.values
        km = KMeans(n_clusters=3,random_state=1234).fit(vector)
        labels = km.labels_
        tsne = TSNE(random_state=1234)
        a = tsne.fit_transform(vector)
        # a = np.load("tsne_doc2vec_exetools_post.npy",allow_pickle=True)
        result = pd.DataFrame(a)
        df['label'] = labels
        d1 = result[df['label'] == 0]
        d2 = result[df['label'] == 1]
        d3 = result[df['label'] == 2]
        plt.plot(d1[0], d1[1], 'r.', d2[0], d2[1], 'g.', d3[0], d3[1], 'b.')
        plt.xlabel('compressed dimension 1')
        plt.ylabel('compressed dimension 2')
        plt.title('kmeans with 3 clusters'+str(resultList))
        # plt.savefig('./cluster/kmeans with 3 clusters'+'feature_column'+str(resultList)+'.png')
        plt.show()

def test_tsne():
    df = get_feature_data()
    # df_ = df[['homelessness']]
    # df = df.drop('homelessness',axis = 1)
    vector = df.values
    tsne = TSNE(random_state=1234)
    a = tsne.fit_transform(vector)
    # a = np.load("tsne_doc2vec_exetools_post.npy",allow_pickle=True)
    result = pd.DataFrame(a)
    # d1 = result[df['homelessness'] == 0]
    # d2 = result[df['homelessness'] == 1]
    # d3 = result[df['homelessness'] == 2]
    # plt.plot(d1[0], d1[1], 'r.', d2[0], d2[1], 'g.', d3[0], d3[1], 'b.')
    plt.plot(result[0],result[1],'r.')
    plt.xlabel('compressed dimension 1')
    plt.ylabel('compressed dimension 2')
    plt.title('low dimensional data')
    plt.savefig('tsne.png')
    plt.show()
if __name__ == '__main__':
    # data = get_feature_data()
    # data = data[['homelessness','new_dwelling_start','new_dwelling_complete','hpi','sales_volume']]
    # xmeansCluster(data.values)
    km()