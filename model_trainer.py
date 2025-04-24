from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
import joblib

def train_model(X_train, y_train):
    # Train a Random Forest Classifier
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

def save_model(model, filename):
    joblib.dump(model, filename)

model_path = 'ids_model.pkl'
def load_model(model_path):
    return joblib.load(model_path)

if __name__ == "__main__":
    # Usage
    model = train_model(X_train, y_train)
    save_model(model, 'ids_model.pkl')