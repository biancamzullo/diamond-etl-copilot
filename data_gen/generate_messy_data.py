import pandas as pd
import random
import numpy as np

def generate_messy_diamond_data(num_rows=50):
    # standard valid sets
    colors = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
    clarities = ['IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2']
    cuts = ['Excellent', 'Very Good', 'Good', 'Fair', 'Poor']
    
    data = []
    
    for i in range(num_rows):
        # base realistic values
        sku = f"SUP-A-{random.randint(1000, 9999)}"
        carat = round(random.uniform(0.5, 3.5), 2)
        color = random.choice(colors)
        clarity = random.choice(clarities)
        cut = random.choice(cuts)
        
        # base realistic price (rough approximation: carat^2 * base_rate)
        base_rate = random.uniform(3000, 5000)
        price = round((carat ** 2) * base_rate, 2)
        
        # inject chaos
        
        # messy strings & typos
        if random.random() < 0.2:
            cut = cut.upper() + " MAKE" # e.g., "EXCELLENT MAKE"
        elif random.random() < 0.1:
            cut = cut.replace("e", "") # typos like "Excllnt"
            
        if random.random() < 0.2:
            clarity = clarity.replace("VVS", "VvS-") # inconsistent casing/hyphens
            
        # 2. combined specs (dumping everything into a raw description)
        raw_desc = ""
        if random.random() < 0.3:
            raw_desc = f"{carat}ct-{color}-{clarity} {cut}"
            # wipe out the structured columns to simulate messy entry
            carat, color, clarity, cut = np.nan, np.nan, np.nan, np.nan
        elif random.random() < 0.2:
            raw_desc = f"{carat} Carat, Color {color}, {clarity} clarity"
        
        # missing data
        if random.random() < 0.1: carat = np.nan
        if random.random() < 0.1: color = np.nan
        
        # pricing anomalies 
        if random.random() < 0.1:
            # huge error: 10x or 100x too cheap or expensive
            price = round(price * random.choice([0.01, 0.1, 10.0, 50.0]), 2)
            
        # string-ify prices (e.g., adding dollar signs or commas)
        if random.random() < 0.3:
            price = f"${price:,.2f}"
            
        data.append({
            "supplier_sku": sku,
            "raw_description": raw_desc,
            "carat_weight": carat,
            "color_grade": color,
            "clarity_grade": clarity,
            "cut_grade": cut,
            "wholesale_cost": price
        })

    df = pd.DataFrame(data)
    
    # randomly shuffle some column names to simulate poor headers
    df.rename(columns={
        'color_grade': random.choice(['color_grade', 'Colr', 'Color Grade']),
        'wholesale_cost': random.choice(['wholesale_cost', 'Price (USD)', 'Cost'])
    }, inplace=True)
    
    return df

if __name__ == "__main__":
    df_messy = generate_messy_diamond_data(50)
    filename = "messy_supplier_inventory.csv"
    df_messy.to_csv(filename, index=False)
    print(f"Generated {filename} with 50 rows of chaotic data.")
    
    # print a quick preview of the chaos
    print("\nPreview of the mess:")
    print(df_messy.head(10))