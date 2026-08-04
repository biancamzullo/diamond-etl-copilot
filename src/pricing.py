def calculate_retail_price(row: dict) -> float:
    """
    purpose: executes deterministic financial business rules to calculate final retail pricing. 
    this explicitly isolates pricing math away from the llm to prevent hallucinations in live e-commerce data.
    parameters: 
        - row (dict): a normalized dictionary representing a single diamond's specifications.
    return values: 
        - float: the calculated retail price rounded to two decimal places.
    errors: 
        - gracefully handles missing keys using .get(), preventing keyerrors.
    side effects: 
        - none. this is a pure function (same input always equals the same output).
    """
    
    # safely extract the wholesale cost, defaulting to 0.0 to prevent mathematical crashes
    cost = row.get("wholesale_cost", 0.0)

    # immediately reject invalid or missing costs (anomalies will be flagged later)
    if cost <= 0:
        return 0.0
    
    # establish the foundational business margin (35% markup)
    markup = 1.35 
    
    # apply dynamic premium markups based on physical attributes
    # add 5% margin for premium cut grades
    if row.get("cut") in ["Excellent", "Ideal"]:
        markup += 0.05

    # add another 5% margin for premium color grades (colorless)
    if row.get("color") in ["D", "E", "F"]:
        markup += 0.05

    # return the final calculated price, strictly rounded for financial currency representation   
    return round(cost * markup, 2)