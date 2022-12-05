import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import style
import  warnings
from yellowbrick.cluster import KElbowVisualizer

warnings.filterwarnings('ignore')
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

wine_df = pd.read_csv('winequality-red.csv', sep=';')


wss=[]
for i in range(1,10):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(wine_df)
    wss.append(kmeans.inertia_)

model = KMeans()
visualizer = KElbowVisualizer(model, k=(1,10), timings=False)
visualizer.fit(wine_df)
visualizer.show()


pca = PCA()
X = pca.fit_transform(wine_df)
kmeans=KMeans(n_clusters=3)
label = kmeans.fit_predict(X)
unique_labels = np.unique(label)

for i in unique_labels:
    plt.scatter(X[label==i,0], X[label==i,1],label=i, s=20)
    plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s=200, c='black', alpha=0.5)
plt.legend()
plt.title('Wine groups')
plt.show()
