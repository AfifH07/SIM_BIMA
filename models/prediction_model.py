from sklearn.linear_model import LogisticRegression
import pickle

class GraduationPredictor:
    def __init__(self):
        self.model = LogisticRegression()
    
    def train(self, X, y):
        """Train model prediksi kelulusan"""
        self.model.fit(X, y)
    
    def predict(self, X):
        """Prediksi kelulusan"""
        return self.model.predict(X)
    
    def save_model(self, filepath):
        """Simpan model"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.model, f)
    
    def load_model(self, filepath):
        """Load model"""
        with open(filepath, 'rb') as f:
            self.model = pickle.load(f)
