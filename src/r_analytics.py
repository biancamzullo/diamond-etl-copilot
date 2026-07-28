import subprocess
import os
import pandas as pd

def generate_r_analytics_plot(df: pd.DataFrame, output_image_path="r_pricing_analysis.png") -> str:
    temp_csv = "temp_r_data.csv"
    df.to_csv(temp_csv, index=False)
    
    try:
        subprocess.run(
            ["Rscript", "scripts/visualize_pricing.R", temp_csv, output_image_path],
            check=True, capture_output=True, text=True
        )
        if os.path.exists(temp_csv): os.remove(temp_csv)
        return output_image_path
    except Exception as e:
        if os.path.exists(temp_csv): os.remove(temp_csv)
        return None