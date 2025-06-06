from models import PricingModel
import joblib
import pandas as pd
import numpy as np

def load_data():
    """Load or generate training data"""
    try:
        # Try loading from CSV if it exists
        df = pd.read_csv('ride_requests.csv')
        if len(df) >= 20:  # Minimum samples required
            X = df[['distance_km', 'priority', 'carpool']].values
            y = df['final_price'].values
            return X, y
    except FileNotFoundError:
        pass
    
    # Fallback: Generate synthetic data
    print("Generating synthetic training data...")
    X = np.random.rand(100, 3)  # [distance, priority, carpool]
    y = X[:, 0] * 10 + X[:, 1] * 20 - X[:, 2] * 5 + np.random.rand(100) * 10  # Simulated pricing
    return X, y

def train_model():
    X, y = load_data()
    model = PricingModel()
    model.train(X, y)
    joblib.dump(model, 'pricing_model.pkl')
    print("Model trained and saved")

if __name__ == '__main__':
    train_model()