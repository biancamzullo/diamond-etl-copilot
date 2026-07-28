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

def generate_cross_validation_plot(df):
    """
    Passes the final dataframe to R to calculate Cook's Distance 
    and returns the file path to the generated diagnostic plot.
    """
    input_csv = "temp_audit_data.csv"
    output_image = "r_cooks_distance.png"
    
    # save the current state of the data for R to read
    df.to_csv(input_csv, index=False)
    
    try:
        # execute the R script via terminal subprocess
        subprocess.run(
            ["Rscript", "scripts/cross_validation_audit.R", input_csv, output_image],
            check=True,
            capture_output=True
        )
        # clean up the temporary CSV
        if os.path.exists(input_csv):
            os.remove(input_csv)
            
        return output_image
    except subprocess.CalledProcessError as e:
        print(f"R execution failed: {e.stderr.decode()}")
        return None