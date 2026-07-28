def calculate_retail_price(row: dict) -> float:
    """Applies custom margins and rules to calculate retail pricing."""
    cost = row.get("wholesale_cost", 0.0)
    if cost <= 0:
        return 0.0
    
    markup = 1.35 # base 35% margin
    
    if row.get("cut") in ["Excellent", "Ideal"]:
        markup += 0.05
    if row.get("color") in ["D", "E", "F"]:
        markup += 0.05
        
    return round(cost * markup, 2)