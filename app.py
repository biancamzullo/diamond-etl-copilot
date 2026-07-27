import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# load environment variables
load_dotenv()


# define target schema (json)
class DiamondSpecs(BaseModel):
    carat: float = Field(description="The carat weight of the diamond. Default to 0.0 if missing.")
    color: str = Field(description="The color grade (D, E, F, G, H, I, J). Default to 'Unknown' if missing.")
    clarity: str = Field(description="The clarity grade (IF, VVS1, VVS2, VS1, VS2, SI1, SI2). Default to 'Unknown'.")
    cut: str = Field(description="The cut grade (Excellent, Very Good, Good, Fair, Poor). Default to 'Unknown'.")
    wholesale_cost: float = Field(description="The raw price/cost of the diamond. Strip out $ and commas. Default to 0.0.")

# setup llm chain 
# using Gemini 3.5 Flash for fast, accurate structured JSON outputs
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

# lorce the LLM to bind to our pydantic schema
structured_llm = llm.with_structured_output(DiamondSpecs)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert diamond buyer. Extract and normalize the diamond specifications from the chaotic text provided. Correct obvious typos (e.g. 'Exclnt' -> 'Excellent')."),
    ("human", "Extract from this chaotic data:\n\n{chaotic_text}")
])

extraction_chain = prompt | structured_llm

def process_row_with_ai(row_dict):
    """Takes a dictionary of a chaotic CSV row and returns a normalized dictionary."""
    # convert the row to a single chaotic string so the LLM has all context
    chaotic_string = " | ".join([f"{k}: {v}" for k, v in row_dict.items()])
    
    try:
        # the chain returns a structured Pydantic object
        normalized_data = extraction_chain.invoke({"chaotic_text": chaotic_string})
        return normalized_data.dict()
    except Exception as e:
        st.error(f"Failed to process row: {e}")
        return {"carat": 0.0, "color": "Error", "clarity": "Error", "cut": "Error", "wholesale_cost": 0.0}

# streamlit ui
st.set_page_config(page_title="Diamond ETL Copilot", layout="wide")

st.title("💎 Supplier ETL & Normalization")
st.markdown("Upload chaotic supplier CSVs. The AI will normalize the specs into a strict schema.")

uploaded_file = st.file_uploader("Upload messy_supplier_inventory.csv", type=["csv"])

# API calls in a loop take time. 
# we add a slider so you can demo just 5-10 rows instantly.
if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    st.subheader("Raw Chaotic Data")
    st.dataframe(df_raw.head())
    
    limit = st.slider("Select number of rows to process (for POC speed)", 1, len(df_raw), 5)
    
    if st.button("Normalize Data with AI"):
        df_subset = df_raw.head(limit)
        
        with st.spinner("AI is cleaning and standardizing the data..."):
            cleaned_rows = []
            
            # iterate through rows and pass to LLM
            for index, row in df_subset.iterrows():
                row_dict = row.to_dict()
                # keep the SKU, AI handles the rest
                sku = row_dict.get("supplier_sku", f"UNKNOWN-{index}")
                
                clean_dict = process_row_with_ai(row_dict)
                clean_dict["supplier_sku"] = sku 
                
                cleaned_rows.append(clean_dict)
                
            df_clean = pd.DataFrame(cleaned_rows)
            
            # reorder columns for a nice display
            df_clean = df_clean[["supplier_sku", "carat", "color", "clarity", "cut", "wholesale_cost"]]
            
            st.success("Normalization Complete!")
            st.subheader("Cleaned & Structured Data")
            st.dataframe(df_clean)