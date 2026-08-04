import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# define a strict schema for a single diamond record
class DiamondSpecs(BaseModel):
    """
    purpose: acts as a strict schema boundary between the probabilistic llm and our deterministic python logic.
    it forces the llm to return exact types (floats, strings) and strips out unwanted characters.
    """
    carat: float = Field(description="Carat weight. Default to 0.0 if missing.")
    color: str = Field(description="Color grade (D, E, F, G, H, I, J). Default 'Unknown'.")
    clarity: str = Field(description="Clarity grade (IF, VVS1, VVS2, VS1, VS2, SI1, SI2). Default 'Unknown'.")
    cut: str = Field(description="Cut grade (Excellent, Very Good, Good, Fair, Poor). Default 'Unknown'.")
    # explicitly instruct the llm to clean the financial data so it doesn't break python math downstream
    wholesale_cost: float = Field(description="Wholesale price. Strip $ and commas. Default 0.0.")

# define a wrapper model for batch processing
class BatchDiamondSpecs(BaseModel):
    """
    purpose: allows us to send multiple records in a single api call, massively reducing network latency and token costs.
    """
    items: list[DiamondSpecs] = Field(description="List of extracted diamond specifications")

class LLMNormalizer:
    
    def __init__(self, model_name="gemini-3.6-flash"):
        """
        purpose: initializes the llm client securely by fetching the api key from the environment.
        parameters: 
            - model_name (str): the specific gemini model to use (defaults to flash for speed/cost efficiency).
        return values: 
            - none (initializes the object).
        errors: 
            - ValueError: raised immediately if the GOOGLE_API_KEY environment variable is missing, preventing silent failures.
        side effects: 
            - instantiates an active network client connected to google's servers.
        """
        self.model_name = model_name

        # securely fetch the api key (never hardcode secrets in production code)
        api_key = os.getenv("GOOGLE_API_KEY")
        # fail fast if the environment is misconfigured
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        # initialize the official gemini client
        self.client = genai.Client(api_key=api_key)

    def normalize_batch(self, rows_list: list) -> list:
        """
        purpose: takes a batch of messy supplier strings and uses the llm to extract structured json data.
        parameters: 
            - rows_list (list): a list of raw string representations of diamond inventory rows.
        return values: 
            - list: a list of normalized python dictionaries matching the DiamondSpecs schema.
        errors: 
            - catches all general exceptions (network timeouts, rate limits) and returns a safe fallback list.
        side effects: 
            - consumes api quota/tokens. 
            - triggers streamlit ui error toasts if the api fails.
        """
        
        # convert the list of rows into a single, indexed string to feed the llm in one shot
        chaotic_batch_string = "\n".join([f"Row {idx}: {row}" for idx, row in enumerate(rows_list)])
        # engineer a precise prompt defining the persona and the task
        prompt = (
            "You are an expert diamond buyer. Extract and normalize diamond specifications "
            "from the following batch of chaotic text rows. Return a list in the exact order provided.\n\n"
            f"{chaotic_batch_string}"
        )
        
        try:
            # execute the api call using structured outputs
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    # force the llm to conform to our pydantic schema (eliminates json parsing errors)
                    response_schema=BatchDiamondSpecs
                    
                )
            )
            # parse the guaranteed json string into a python dictionary
            result_dict = json.loads(response.text)
            return result_dict.get("items", [])
            
        except Exception as e:
            # graceful degradation: if the api fails (e.g. rate limit), don't crash the whole pipeline
            import streamlit as st
            # surface the error to the operator in the ui
            st.error(f"LLM API Error: {str(e)}")
            # return a list of explicit error objects matching the length of the batch
            # this ensures the ui table still renders but clearly highlights the failure for human review
            return [
                {"carat": 0.0, "color": "Error", "clarity": "Error", "cut": "Error", "wholesale_cost": 0.0} 
                for _ in rows_list
            ]