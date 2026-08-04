# import pandas and numpy for high-performance vectorized operations
import pandas as pd
import numpy as np
# import isolation forest for unsupervised multi-dimensional anomaly detection
from sklearn.ensemble import IsolationForest

class HybridAnomalyDetector:
    """
    purpose: combines strict business heuristics with unsupervised machine learning to act as an automated firewall.
    it prevents mathematically invalid inventory from reaching the shopify storefront.
    """
    
    def __init__(self, contamination=0.15):
        """
        purpose: initializes the machine learning model with a specified sensitivity.
        parameters: 
            - contamination (float): the expected proportion of outliers in the dataset (defaults to 15%).
        return values: 
            - none.
        errors: 
            - none.
        side effects: 
            - instantiates the sklearn model and seeds the random state for reproducible testing.
        """
        # initialize the isolation forest. we use a static random_state so our cross-validation testing remains consistent.
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def detect(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        purpose: executes the ensembled anomaly detection pipeline (heuristics + ml) over a batch dataframe.
        parameters: 
            - df (pd.DataFrame): the processed pandas dataframe containing parsed specs and calculated prices.
        return values: 
            - df (pd.DataFrame): the original dataframe with an appended boolean 'is_anomaly' column.
        errors: 
            - safely handles zero-division math and bypasses ml execution if the dataset is too small.
        side effects: 
            - modifies a copy of the dataframe, leaving the original intact.
        """
        
        # work on a copy of the dataframe to avoid pandas 'SettingWithCopy' memory warnings
        df = df.copy()
        
        # engineer a new feature (price per carat) to feed the machine learning model
        # use np.where for vectorized execution, safely bypassing division-by-zero crashes on null/zero carats
        df["price_per_carat"] = np.where(
            df["carat"] > 0, 
            df["wholesale_cost"] / df["carat"], 
            0
        )

        # these flag obvious garbage that doesn't need complex machine learning
        rule_anomalies = (
            # flag any diamond listed under $100 wholesale
            (df["wholesale_cost"] <= 100) | 
            # flag any diamond over half a carat that is absurdly cheap per carat
            ((df["carat"] > 0.5) & (df["price_per_carat"] < 500)) 
        )

        # only run the model if we have at least 3 rows, otherwise the multi-dimensional math breaks
        if len(df) >= 3:
            # isolate the numeric features to map the density relationship
            features = df[["carat", "wholesale_cost", "price_per_carat"]]
            # fit the model and predict in one step. returns -1 for outliers, 1 for inliers.
            ml_predictions = self.model.fit_predict(features)
            # convert the -1/1 output array into a boolean series matching the dataframe index
            ml_anomalies = ml_predictions == -1
        else:
            # fallback for micro-batches: assume everything is normal if we can't run the ml
            ml_anomalies = pd.Series([False] * len(df))

        # flag row if either Hard Rules or ML triggered
        df["is_anomaly"] = rule_anomalies | ml_anomalies
        return df