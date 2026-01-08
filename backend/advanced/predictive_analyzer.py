# backend/advanced/predictive_analyzer.py - Predictive Analytics
"""
Predictive analytics for forecasting mis-selling risks before they happen.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


class PredictiveAnalyzer:
    """Predicts mis-selling risks using ML models"""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def prepare_features(self, historical_data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for prediction"""
        features = pd.DataFrame()
        
        # Time-based features
        features['days_since_launch'] = (datetime.now() - pd.to_datetime(historical_data.get('launch_date', datetime.now()))).dt.days
        features['month'] = datetime.now().month
        features['quarter'] = datetime.now().quarter
        
        # Historical metrics
        features['avg_sentiment_30d'] = historical_data.get('avg_sentiment_30d', 0.5)
        features['complaint_growth_rate'] = historical_data.get('complaint_growth', 0)
        features['sentiment_trend'] = historical_data.get('sentiment_trend', 0)
        
        # Product features
        features['promised_returns_numeric'] = historical_data.get('promised_returns', '0').str.replace('%', '').astype(float) / 100
        features['risk_category_encoded'] = historical_data.get('risk_category', 'medium').map({
            'low': 1, 'medium': 2, 'high': 3
        }).fillna(2)
        
        return features
    
    def train_model(self, training_data: List[Dict]):
        """Train predictive model on historical data"""
        try:
            df = pd.DataFrame(training_data)
            
            # Prepare features and target
            X = self.prepare_features(df)
            y = df.get('future_risk_score', df.get('risk_score', 0.5))
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled, y)
            self.is_trained = True
            
            return True
        except Exception as e:
            print(f"⚠️ Model training failed: {e}")
            return False
    
    def predict_risk(self, product_data: Dict) -> Dict:
        """Predict future risk for a product"""
        if not self.is_trained:
            # Use simple heuristic if model not trained
            return self._simple_prediction(product_data)
        
        try:
            df = pd.DataFrame([product_data])
            features = self.prepare_features(df)
            features_scaled = self.scaler.transform(features)
            
            predicted_risk = self.model.predict(features_scaled)[0]
            predicted_risk = max(0, min(1, predicted_risk))  # Clamp between 0-1
            
            # Determine risk level
            if predicted_risk >= 0.8:
                risk_level = 'critical'
            elif predicted_risk >= 0.6:
                risk_level = 'high'
            elif predicted_risk >= 0.4:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            return {
                'predicted_risk_score': float(predicted_risk),
                'predicted_risk_level': risk_level,
                'prediction_confidence': 0.85,
                'forecast_horizon': '30 days',
                'predicted_date': (datetime.now() + timedelta(days=30)).isoformat()
            }
        except Exception as e:
            print(f"⚠️ Prediction failed: {e}")
            return self._simple_prediction(product_data)
    
    def _simple_prediction(self, product_data: Dict) -> Dict:
        """Simple heuristic-based prediction"""
        current_risk = product_data.get('risk_score', 0.5)
        sentiment_trend = product_data.get('sentiment_trend', 0)
        complaint_growth = product_data.get('complaint_growth', 0)
        
        # Simple trend-based prediction
        predicted_risk = current_risk + (sentiment_trend * -0.1) + (complaint_growth * 0.2)
        predicted_risk = max(0, min(1, predicted_risk))
        
        return {
            'predicted_risk_score': float(predicted_risk),
            'predicted_risk_level': 'high' if predicted_risk > 0.6 else 'medium' if predicted_risk > 0.4 else 'low',
            'prediction_confidence': 0.65,
            'forecast_horizon': '30 days',
            'predicted_date': (datetime.now() + timedelta(days=30)).isoformat()
        }
    
    def forecast_trends(self, product_data: Dict, days_ahead: int = 30) -> pd.DataFrame:
        """Forecast risk trends over time"""
        current_risk = product_data.get('risk_score', 0.5)
        trend = product_data.get('risk_trend', 0)
        
        dates = pd.date_range(start=datetime.now(), periods=days_ahead, freq='D')
        forecasts = []
        
        for i, date in enumerate(dates):
            # Simple linear trend projection
            forecast_risk = current_risk + (trend * i / days_ahead)
            forecast_risk = max(0, min(1, forecast_risk))
            
            forecasts.append({
                'date': date,
                'predicted_risk': forecast_risk,
                'confidence': max(0.5, 1.0 - (i / days_ahead) * 0.3)
            })
        
        return pd.DataFrame(forecasts)
