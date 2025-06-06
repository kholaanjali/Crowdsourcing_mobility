import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

class DQNModel:
    def __init__(self, state_size=3):
        self.state_size = state_size
        self.model = self._build_model()
        
    def _build_model(self):
        model = Sequential([
            Dense(24, input_dim=self.state_size, activation='relu'),
            Dense(24, activation='relu'),
            Dense(1, activation='linear')
        ])
        model.compile(loss='mse', optimizer=Adam(0.001))
        return model
    
    def predict_optimal_price(self, state):
        return self.model.predict(np.array([state]))[0][0]

class PricingModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.rf = RandomForestRegressor(n_estimators=100)
        self.dqn = DQNModel()
        
    def train(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.rf.fit(X_scaled, y)
        
        states = X_scaled
        rewards = y - (X[:,0] * 10)
        self.dqn.model.fit(states, rewards, epochs=50, verbose=0)
        
    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        rf_pred = self.rf.predict(X_scaled)
        dqn_adjustment = np.array([self.dqn.predict_optimal_price(x) for x in X_scaled])
        return (rf_pred + dqn_adjustment) / 2