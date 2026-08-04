import subprocess
import os
import pandas as pd

def generate_r_analytics_plot(df: pd.DataFrame, output_image_path="r_pricing_analysis.png") -> str:
    """
    purpose: bridges python and r by exporting a dataframe and triggering an external r script for visualization.
    parameters: 
        - df (pd.DataFrame): the current state of the inventory dataframe.
        - output_image_path (str): the destination filename for the generated plot.
    return values: 
        - str: the file path to the generated image, or None if the execution fails.
    errors: 
        - catches all subprocess exceptions and ensures temporary files are cleaned up to prevent memory leaks.
    side effects: 
        - writes and deletes temporary files to the local disk.
        - executes a terminal command.
    """
    
    # define a temporary handoff file to pass memory state from python to r
    temp_csv = "temp_r_data.csv"
    # dump the dataframe to disk so the r script can consume it
    df.to_csv(temp_csv, index=False)
    
    try:
        # execute the r script via terminal subprocess
        # check=True forces python to raise an error if r crashes, rather than failing silently
        subprocess.run(
            ["Rscript", "scripts/visualize_pricing.R", temp_csv, output_image_path],
            check=True, capture_output=True, text=True
        )
        
        
        # return the path so the streamlit ui can render the image
        if os.path.exists(temp_csv):
            os.remove(temp_csv)
        # return the path so the streamlit ui can render the image
        return output_image_path
    except Exception as e:
        # fallback: ensure cleanup happens even if the r script throws a fatal error
        if os.path.exists(temp_csv): os.remove(temp_csv)
        return None

def generate_cross_validation_plot(df):
    """
    purpose: executes a classical econometric audit (cook's distance) in r to cross-validate python's machine learning model.
    parameters: 
        - df (pd.DataFrame): the fully processed dataset, including calculated prices.
    return values: 
        - str: the file path to the diagnostic plot, or None on failure.
    errors: 
        - catches CalledProcessError specifically to log standard error output from r.
    side effects: 
        - writes and deletes temporary audit files to disk.
    """
    input_csv = "temp_audit_data.csv"
    output_image = "r_cooks_distance.png"
    
    # save the current state of the data for r to read
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
        # specifically decode and print the r terminal error for debugging
        print(f"R execution failed: {e.stderr.decode()}")
        return None