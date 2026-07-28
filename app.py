import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# page configuration
st.set_page_config(page_title="Diamond ETL Copilot", layout="wide")

# load environment variables
load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    st.error("🔑 `GOOGLE_API_KEY` missing! Please check your .env file.")
    st.stop()

# clean modular imports
try:
    from src.normalizer import LLMNormalizer
    from src.pricing import calculate_retail_price
    from src.anomaly import HybridAnomalyDetector
    from src.storage import persist_to_duckdb
    from src.r_analytics import generate_r_analytics_plot, generate_cross_validation_plot
except ImportError as e:
    st.error(f"Missing local module: {e}. Please check your 'src/' directory structure.")
    st.stop()

# css
clean_css = """
    <style>
    /* Import the elegant serif specifically for the header */
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&display=swap');

    /* Background Color */
    .stApp { 
        background-color: #F4F3ED !important; 
    } 

    /* Normal text (Almost Black / Deep Dark Blue) */
    .stMarkdown, p, label, .stCheckbox span {
        color: #04091E !important; 
    }

    /* Hide Streamlit Header Links */
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    
    /* Clean button styling */
    .stButton > button {
        background-color: #181492 !important;
        color: #FFFFFF !important;
        border: none !important;
        font-weight: bold !important;
    }
    .stButton > button * {
        color: #FFFFFF !important;
    }
    </style>
"""
st.markdown(clean_css, unsafe_allow_html=True)

#header
col_logo, col_text = st.columns([1, 6], vertical_alignment="center")

with col_logo:
    st.image("https://media.licdn.com/dms/image/v2/C560BAQFfWQhceJZ_HA/company-logo_200_200/company-logo_200_200/0/1630594142816/frankdarling_logo?e=2147483647&v=beta&t=usjgKcG_zRLc5vxOils_dDYwXVLXz4rr33hX8lnDg7g", width=80)

with col_text:
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600&display=swap');
        </style>
        <div style="font-family: 'Cormorant Garamond', Georgia, serif; color: #181492; font-size: 54px; font-weight: 600; line-height: 1; margin-bottom: 8px;">
            FRANK DARLING
        </div>
        <div style="font-family: Arial, sans-serif; color: #181492; font-size: 14px; letter-spacing: 2px; text-transform: uppercase; font-weight: 700;">
            Bespoke Inventory & Systems Engine • Powered by Gemini
        </div>
        """, 
        unsafe_allow_html=True
    )

st.markdown("<hr style='border: 0; height: 1px; background: #D1CFCD; margin-top: 15px; margin-bottom: 25px;'>", unsafe_allow_html=True)

st.markdown("<hr style='border: 0; height: 1px; background: #D1CFCD; margin-top: 15px; margin-bottom: 25px;'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload messy_supplier_inventory.csv", type=["csv"])


# UI pipeline

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    limit = st.slider("Select rows to process", 3, len(df_raw), 15)
    
    st.markdown("<div style='text-align: center; margin-top: 10px;'>", unsafe_allow_html=True)
    run_button = st.button("RUN PIPELINE, DARLING", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if run_button:
        df_subset = df_raw.head(limit)
        normalizer = LLMNormalizer()
        detector = HybridAnomalyDetector()
        
        with st.spinner("Processing Batch through Gemini Engine..."):
            try:
                row_dicts = df_subset.to_dict(orient="records")
                cleaned_rows = normalizer.normalize_batch(row_dicts)
                
                for idx, clean_dict in enumerate(cleaned_rows):
                    if idx < len(df_subset):
                        clean_dict["supplier_sku"] = df_subset.iloc[idx].get("supplier_sku", f"SKU-{idx}")
                
                df_clean = pd.DataFrame(cleaned_rows)
                df_clean["retail_price"] = df_clean.apply(calculate_retail_price, axis=1)
                df_processed = detector.detect(df_clean)
                
                conn = persist_to_duckdb(df_processed)
                st.session_state['df_final'] = conn.execute("SELECT * FROM supplier_inventory").df()
                st.success("Pipeline Complete!")

            except Exception as err:
                st.error(f"Pipeline Exception: {str(err)}")


if 'df_final' in st.session_state:
    df_final = st.session_state['df_final']
    
    anomalies = df_final[df_final['is_anomaly'] == True]
    anomaly_count = len(anomalies)

    # added: business KPIs
    if anomaly_count > 0:
        # calculate the financial risk prevented 
    
        risk_prevented = anomalies['wholesale_cost'].sum() if 'wholesale_cost' in anomalies.columns else 0.00
        
        st.error(f"**PagerDuty / Slack Alert:** Flagged {anomaly_count} pricing anomalies. Suppressing from Shopify sync and escalating to `#ops-diamond-review`.")
        
        # display the KPI metric
        st.metric(
            label="Capital Risk Mitigated (Anomalies Quarantined)", 
            value=f"${risk_prevented:,.2f}",
            delta=f"{anomaly_count} Assets Blocked",
            delta_color="inverse"
        )
    else:
        st.success("No anomalies detected. Safe to sync.")

    # automatically pre-check diamonds that are NOT anomalies.
    if 'Approved' not in df_final.columns:
        df_final.insert(0, 'Approved', ~df_final['is_anomaly'])

    def highlight_anomalies(row):
        return ['background-color: #ffcccc; color: #181492;' if row['is_anomaly'] else '' for _ in row]
    
    st.write("Review the pipeline output below. Uncheck any valid diamond you wish to manually withhold from the Shopify sync.")
    
    disabled_cols = [col for col in df_final.columns if col != 'Approved']
    
    edited_df = st.data_editor(
        df_final.style.apply(highlight_anomalies, axis=1), 
        use_container_width=True,
        hide_index=True,
        column_config={
            "Approved": st.column_config.CheckboxColumn(
                "Approve for Shopify",
                help="Select to include in the Shopify GraphQL export",
            )
        },
        disabled=disabled_cols 
    )

    st.divider()

    # added: dual plot display & GraphQL generation
    st.markdown("<h3 style='text-align: center;'>Statistical Auditing & GraphQL Sync</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.caption("Hedonic Pricing Model (R)")
        plot_path_1 = generate_r_analytics_plot(df_final)
        if plot_path_1:
            st.image(plot_path_1)

    with col2:
        st.caption("Cross-Validation: Cook's Distance (R)")
        plot_path_2 = generate_cross_validation_plot(df_final)
        if plot_path_2:
            st.image(plot_path_2)

    with col3:
        st.caption("Shopify GraphQL Dispatch")
        st.write("Generate payload for manually approved variants.")
        
        if st.button("Generate Dispatch Payload"):
            valid_df = edited_df[(edited_df['Approved'] == True) & (edited_df['is_anomaly'] == False)]
            
            if valid_df.empty:
                st.warning("No valid diamonds selected for export.")
            else:
                variants_payload = []
                for _, row in valid_df.iterrows():
                    variants_payload.append({
                        "sku": row['supplier_sku'],
                        "price": str(row['retail_price']),
                        "inventoryItem": {"tracked": True}
                    })
                    
                graphql_mutation = {
                    "query": "mutation productVariantsBulkUpdate($productId: ID!, $variants: [ProductVariantsBulkInput!]!) { productVariantsBulkUpdate(productId: $productId, variants: $variants) { userErrors { field message } } }",
                    "variables": {
                        "productId": "gid://shopify/Product/987654321",
                        "variants": variants_payload
                    }
                }
                
                st.json(graphql_mutation)
                st.success(f"Payload ready! ({len(valid_df)} variants packaged)")
# footer
st.markdown("<br><hr style='border: 0; height: 1px; background: #D1CFCD;'>", unsafe_allow_html=True)
st.markdown(
    """
    <div style='text-align: center; padding-bottom: 25px;'>
        <p style='font-size: 1.05rem; letter-spacing: 1px;'>
            Pipeline Architecture & ETL Copilot Engineered by <strong>Bianca Zullo</strong>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)