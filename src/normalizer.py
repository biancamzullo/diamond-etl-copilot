import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

class DiamondSpecs(BaseModel):
    carat: float = Field(description="Carat weight. Default to 0.0 if missing.")
    color: str = Field(description="Color grade (D, E, F, G, H, I, J). Default 'Unknown'.")
    clarity: str = Field(description="Clarity grade (IF, VVS1, VVS2, VS1, VS2, SI1, SI2). Default 'Unknown'.")
    cut: str = Field(description="Cut grade (Excellent, Very Good, Good, Fair, Poor). Default 'Unknown'.")
    wholesale_cost: float = Field(description="Wholesale price. Strip $ and commas. Default 0.0.")

class BatchDiamondSpecs(BaseModel):
    items: list[DiamondSpecs] = Field(description="List of extracted diamond specifications")

class LLMNormalizer:
    
    def __init__(self, model_name="gemini-3.6-flash"):
        self.model_name = model_name
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is not set.")
        self.client = genai.Client(api_key=api_key)

    def normalize_batch(self, rows_list: list) -> list:
        chaotic_batch_string = "\n".join([f"Row {idx}: {row}" for idx, row in enumerate(rows_list)])
        prompt = (
            "You are an expert diamond buyer. Extract and normalize diamond specifications "
            "from the following batch of chaotic text rows. Return a list in the exact order provided.\n\n"
            f"{chaotic_batch_string}"
        )
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=BatchDiamondSpecs
                    
                )
            )
            result_dict = json.loads(response.text)
            return result_dict.get("items", [])
            
        except Exception as e:
            import streamlit as st
            st.error(f"LLM API Error: {str(e)}")
            return [
                {"carat": 0.0, "color": "Error", "clarity": "Error", "cut": "Error", "wholesale_cost": 0.0} 
                for _ in rows_list
            ]