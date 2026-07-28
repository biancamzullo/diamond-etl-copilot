import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

class HybridAnomalyDetector:
    """Combines hard business rules with statistical Isolation Forest ML."""
    
    def __init__(self, contamination=0.15):
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        
        # safer, faster division avoiding zero-division warnings
        df["price_per_carat"] = np.where(
            df["carat"] > 0, 
            df["wholesale_cost"] / df["carat"], 
            0
        )

        # hard rule heuristics (deterministic guardrails)
        rule_anomalies = (
            (df["wholesale_cost"] <= 100) | 
            ((df["carat"] > 0.5) & (df["price_per_carat"] < 500)) 
        )

        # ML isolation forest (statistical outliers)
        if len(df) >= 3:
            features = df[["carat", "wholesale_cost", "price_per_carat"]]
            ml_predictions = self.model.fit_predict(features)
            ml_anomalies = ml_predictions == -1
        else:
            ml_anomalies = pd.Series([False] * len(df))

        # flag row if either Hard Rules or ML triggered
        df["is_anomaly"] = rule_anomalies | ml_anomalies
        return df