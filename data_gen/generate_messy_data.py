# import pandas for dataframe manipulation, random for chaos injection, and numpy for handling null values
import pandas as pd
import random
import numpy as np

def generate_messy_diamond_data(num_rows=50):
    """
    purpose: generates synthetic, unstructured supplier data to test the etl pipeline's robustness and machine learning thresholds.
    parameters: 
        - num_rows (int): the number of synthetic diamond records to create (default is 50).
    return values: 
        - df (pandas.DataFrame): a dataframe containing the chaotic, unstructured inventory data.
    errors: 
        - none explicitly raised (fails safely unless memory limits are exceeded on massive row counts).
    side effects: 
        - utilizes the global random state, which may affect other random operations if a seed is not set.
    """
    
    # define standard valid diamond attributes to build our baseline truth
    colors = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
    clarities = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2']
    cuts = ['Excellent', 'Very Good', 'Good', 'Fair', 'Poor']
    
    # initialize an empty list to hold our generated rows
    data = []
    
    # iterate through the requested number of rows to build our dataset
    for i in range(num_rows):
       
        # establish a clean, realistic baseline for this specific diamond
        sku = f"SUP-A-{random.randint(1000, 9999)}"
        carat = round(random.uniform(0.5, 3.5), 2)
        color = random.choice(colors)
        clarity = random.choice(clarities)
        cut = random.choice(cuts)
        
        # base realistic price (rough approximation: carat^2 * base_rate)
        base_rate = random.uniform(3000, 5000)
        price = round((carat ** 2) * base_rate, 2)
        
        # inject chaos
        
        # inject 20% chance of adding random supplier jargon to the cut string
        if random.random() < 0.2:
            cut = cut.upper() + " MAKE" # e.g., "EXCELLENT MAKE"
        # inject 10% chance of creating typos by removing vowels
        elif random.random() < 0.1:
            cut = cut.replace("e", "") # typos like "Excllnt"

        # simulate inconsistent casing and hyphens in clarity grades    
        if random.random() < 0.2:
            clarity = clarity.replace("VVS", "VvS-") # inconsistent casing/hyphens
            
        # initialize an empty raw description column
        raw_desc = ""
        if random.random() < 0.3:
            raw_desc = f"{carat}ct-{color}-{clarity} {cut}"
            # wipe out the structured columns to simulate lazy supplier data entry (forces the llm to parse it)
            carat, color, clarity, cut = np.nan, np.nan, np.nan, np.nan
        # simulate 20% chance of partial unstructured data
        elif random.random() < 0.2:
            raw_desc = f"{carat} Carat, Color {color}, {clarity} clarity"
        
        # missing data
        if random.random() < 0.1: carat = np.nan
        if random.random() < 0.1: color = np.nan
        
        # simulate 10% chance of a severe pricing typo
        if random.random() < 0.1:
            # this mathematically breaks the density distribution
            price = round(price * random.choice([0.01, 0.1, 10.0, 50.0]), 2)
            
        # corrupt the price data types by randomly adding strings (dollar signs and commas)
        if random.random() < 0.3:
            price = f"${price:,.2f}"

        # append the final, heavily corrupted row to our dataset    
        data.append({
            "supplier_sku": sku,
            "raw_description": raw_desc,
            "carat_weight": carat,
            "color_grade": color,
            "clarity_grade": clarity,
            "cut_grade": cut,
            "wholesale_cost": price
        })

    # convert the list of dictionaries into a pandas dataframe
    df = pd.DataFrame(data)
    
    # randomly shuffle some column names to simulate poor headers
    df.rename(columns={
        'color_grade': random.choice(['color_grade', 'Colr', 'Color Grade']),
        'wholesale_cost': random.choice(['wholesale_cost', 'Price (USD)', 'Cost'])
    }, inplace=True)
    
    # return the final messy dataframe
    return df


# standard python main execution block
if __name__ == "__main__":
    # generate a 50-row dataset
    df_messy = generate_messy_diamond_data(50) 
    filename = "messy_supplier_inventory.csv"

    # export the dataframe to a csv file without the pandas index column
    df_messy.to_csv(filename, index=False)
    # print confirmation to the console
    print(f"Generated {filename} with 50 rows of chaotic data.")
    
    # print a quick preview of the chaos
    print("\nPreview of the mess:")
    print(df_messy.head(10))