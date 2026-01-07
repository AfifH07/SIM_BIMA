from sklearn.cluster import KMeans

class StudentClustering:
    def __init__(self, n_clusters=3):
        self.model = KMeans(n_clusters=n_clusters)
    
    def fit_predict(self, X):
        """Clustering siswa berdasarkan performa"""
        return self.model.fit_predict(X)
