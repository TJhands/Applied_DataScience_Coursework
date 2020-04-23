from pyclustering.cluster.xmeans import xmeans
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.cluster import cluster_visualizer_multidim
from collections import  Counter
import pandas as pd
from sklearn.cluster import KMeans
from integrate_data import get_feature_data
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
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
    vector = df.values
    # labels = cluster(vector)
    # data['label'] = labels
    labels_ = xmeansCluster(vector)
    label = pd.DataFrame(labels_).stack().reset_index(level=1, drop=True).rename('A').to_frame()
    label['label'] = label.index
    label.sort_values(by='A', inplace=True)
    label.set_index('A', inplace=True)
    df = df.join(label)
    tsne = TSNE()
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
    plt.plot(d1[0], d1[1], 'r.', d2[0], d2[1], 'go', d3[0], d3[1], 'b*',d4[0],d4[1],'y',
             d5[0], d5[1], 'c', d6[0], d6[1], 'm', d7[0], d7[1], 'black',d8[0],d8[1],'pink')
    plt.show()
if __name__ == '__main__':
    # data = get_feature_data()
    # data = data[['homelessness','new_dwelling_start','new_dwelling_complete','hpi','sales_volume']]
    # xmeansCluster(data.values)
    show_data()