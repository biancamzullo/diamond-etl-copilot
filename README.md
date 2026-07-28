# FRANK DARLING: BESPOKE INVENTORY & SYSTEMS ENGINE

## OVERVIEW
This architecture is a highly opinionated, deterministic ETL pipeline designed to ingest chaotic, unstructured supplier inventory feeds and synthesize them into a heavily structured, retail-ready data warehouse. We do not tolerate data entropy. By combining large language models for semantic parsing, immutable business logic for pricing, and unsupervised machine learning for statistical anomaly detection, this system acts as a ruthless filter between supplier chaos and the Frank Darling storefront.

## LIVE DEMO & INTERFACE PREVIEW

<video src="https://github.com/user-attachments/assets/3497c0d9-2d51-49e2-a7dd-2a4347d71bed" controls="controls" width="100%" style="max-height:640px;">
  Your browser does not support the video tag.
</video>

*The video above demonstrates the pipeline processing chaotic supplier inputs, running batch semantic extraction via Gemini, applying pricing heuristics, and quarantining statistical anomalies in real time.*

## SYSTEM ARCHITECTURE

### 1. The Messy Data Generator (Entropy Simulation)
Real-world diamond supplier data is notoriously fragmented, riddled with typos, and lacks standardized formatting. To rigorously test the pipeline's resilience, the generator artificially synthesizes chaotic data streams. It embeds critical target parameters (carat, color, clarity, cut, wholesale cost) within obfuscated, non-standardized text strings to simulate the worst-case scenario of a raw CSV dump. 

### 2. The AI Normalizer (Semantic Extraction Engine)
Traditional regex fails against unstructured human input. We utilize the Google GenAI SDK (powered by Gemini) to execute batch-prompted semantic normalization. 
*   **Mechanism:** The engine ingests rows in batched arrays, minimizing API latency and preventing rate-limit throttling.
*   **Enforcement:** Output is strictly coerced into a Pydantic schema. The model is permitted zero creative liberty; it acts purely as a semantic parser mapping unstructured text into deterministic, strongly-typed JSON payloads.

### 3. The Pricing Engine (Deterministic Hedonic Logic)
Once specifications are normalized, they pass through a strict, zero-latency pricing heuristic. Asset pricing relies on compounding hedonic markups applied to the normalized wholesale cost.

*   **Base Margin:** A non-negotiable 35% markup applied to the baseline cost.
*   **Cut Premium:** An additional 5% compounding premium applied exclusively to "Excellent" or "Ideal" cut geometries.
*   **Color Premium:** An additional 5% compounding premium applied to high-tier color grades ("D", "E", or "F").

### 4. Statistical Anomaly Detection (The Quarantine Protocol)
We assume all incoming data is hostile or erroneous until proven otherwise. This module utilizes a hybrid ensemble to flag pricing errors before they sync to the retail environment.

*   **Heuristic Guardrails:** Absolute logical boundaries. Any asset with a wholesale cost under 100 USD or a price-per-carat ratio mathematically inconsistent with physical reality (e.g., > 0.5 carats at < 500 USD/ct) is immediately quarantined.
*   **Isolation Forest (Machine Learning):** Unsupervised outlier detection for high-dimensional statistical anomalies. The algorithm isolates observations by randomly selecting a feature and then randomly selecting a split value between the maximum and minimum values of the selected feature.
*   **The Math:** The anomaly score for a given observation is defined as:
   $$s(x, n) = 2^{-\frac{E(h(x))}{c(n)}}$$
    Where h(x) is the path length required to isolate the data point x, and c(n) is the average path length of an unsuccessful search in a Binary Search Tree of n nodes. Data points yielding an anomaly score approaching 1 are flagged for manual review.

### 5. R Analytics (Multivariable Regression)
To audit the integrity of the pricing engine over time, the pipeline invokes an R script (via ggplot2 and standard statistical libraries) to visualize hedonic price distributions.

*   **The Math:** We model the natural logarithm of the retail price as a function of its physical attributes:
   $$\ln(\text{Price}) = \beta_0 + \beta_1(\text{Carat}) + \sum (\beta_i \cdot \text{Attribute}_i) + \epsilon$$
    This regression allows us to isolate the exact marginal contribution of a specific attribute (like moving from VS1 to VVS2) independent of the carat weight, proving the pricing engine's logic holds at scale.

### 6. The Interface (Streamlit UI)
A high-performance, strictly typed frontend application engineered via Streamlit. To enforce the Frank Darling brand standard, Streamlit's native Emotion CSS engine has been entirely overridden via raw inline HTML injection. The interface employs a stark, minimalist hierarchy using the Cormorant Garamond typeface and a strictly controlled palette (Midnight Navy and Royal Blue), ensuring a sterile, highly readable command center for data operations.

### 7. The Output (Shopify-Ready JSON)
The final stage of the pipeline translates the fully normalized, priced, and anomaly-screened data into a strict JSON payload engineered specifically for the Shopify Admin API. This guarantees zero-friction inventory syncing and maps physical asset specifications directly into Shopify Metafields for granular storefront filtering.

```json
{
  "product": {
    "title": "1.50 Carat Round Diamond - E Color, VVS2 Clarity, Ideal Cut",
    "body_html": "<p>Fully vetted, precision-cut loose diamond.</p>",
    "vendor": "Frank Darling Systems",
    "product_type": "Loose Diamond",
    "status": "active",
    "tags": [
      "Shape_Round", 
      "Color_E", 
      "Clarity_VVS2", 
      "Cut_Ideal"
    ],
    "variants": [
      {
        "sku": "FD-DIA-R-150-E-VVS2",
        "price": "7550.00",
        "compare_at_price": null,
        "inventory_management": "shopify",
        "inventory_quantity": 1,
        "weight": 1.50,
        "weight_unit": "ct",
        "requires_shipping": true
      }
    ],
    "metafields": [
      {
        "namespace": "diamond_specs",
        "key": "carat",
        "value": "1.50",
        "type": "number_decimal"
      },
      {
        "namespace": "diamond_specs",
        "key": "color",
        "value": "E",
        "type": "single_line_text_field"
      },
      {
        "namespace": "diamond_specs",
        "key": "clarity",
        "value": "VVS2",
        "type": "single_line_text_field"
      },
      {
        "namespace": "diamond_specs",
        "key": "cut",
        "value": "Ideal",
        "type": "single_line_text_field"
      },
      {
        "namespace": "diamond_specs",
        "key": "wholesale_cost_audited",
        "value": "5200.00",
        "type": "number_decimal"
      }
    ]
  }
}
```
### 8. The Dispatch Protocol (Human-in-the-Loop & Anomaly Quarantine)
While the pipeline is highly automated, pushing supplier data directly to a live retail environment carries inherent business risk. To mitigate this, the final stage of the architecture features a strictly controlled human-in-the-loop dispatch table.

*   **Interactive Review:** Using Streamlit's `st.data_editor`, the output is rendered as an interactive table. Valid diamonds are automatically pre-checked for Shopify export, but operators retain the ability to manually uncheck and withhold any asset.
*   **Immutable Data:** All physical specifications and retail prices are strictly locked (`disabled=True`) in the UI. Users can only approve or deny the export; they cannot manually alter the data, ensuring the pricing engine's logic remains uncorrupted.
*   **The Quarantine Rule (No Auto-Fixing):** If the Isolation Forest algorithm flags a diamond as mathematically anomalous (e.g., a $50,000 diamond listed for $50 due to a supplier typo), the asset is aggressively locked out of the Shopify payload. The system *does not* attempt to auto-fix the anomaly. In high-stakes retail, an AI should never guess a financial correction; it must halt and escalate. Anomalies are permanently unchecked, suppressed from the GraphQL generation, and flagged for manual review via Slack/PagerDuty.

### 9. Business KPI Tracking: Capital Risk Mitigated
Technical metrics only matter if they drive business outcomes. The Streamlit dashboard actively quantifies the pipeline's value by calculating the **Capital Risk Mitigated**. 

When the Isolation Forest quarantines an anomalous asset, the UI aggregates the wholesale cost of the suppressed inventory. Instead of simply reporting "3 anomalies found," the system reports the exact dollar amount of mispriced inventory prevented from syncing to the live Shopify storefront, aligning technical architecture directly with executive financial metrics.

### 10. Statistical Cross-Validation (Machine Learning vs. Econometrics)
To ensure the pipeline’s anomaly detection is mathematically robust, the system cross-validates Python's Unsupervised Machine Learning (Isolation Forest) against R's Classical Econometrics (Cook's Distance). 

In R, Cook's Distance ($D_i$) measures the aggregate change in the fitted model when a specific observation is removed. The mathematical definition relies on the sum of squared differences in predictions:

$$D_i = \frac{\sum_{j=1}^{n} (\hat{y}_j - \hat{y}_{j(i)})^2}{p \cdot MSE}$$

**The Architectural "Flex" (Why ML is Necessary)**
During testing, the pipeline processed a severely mispriced 1.25-carat diamond listed for $81. 
*   **The R Model (Missed It):** Because $1.25$ carats sits near the mean weight of the dataset, it lacked the statistical *leverage* required on the x-axis to heavily skew the linear regression line. It failed to cross the $\frac{4}{n}$ threshold and was ignored by classical metrics.
*   **The Python ML Model (Caught It):** The Isolation Forest does not rely on linear leverage; it evaluates multi-dimensional density. It immediately recognized that a $81 price tag for a 1.25-carat stone violates the fundamental density patterns of the dataset and successfully quarantined it.

This intentional discrepancy proves the necessity of the Machine Learning layer: traditional linear statistical auditing is too brittle to protect a live retail system from non-linear supplier typos.

---
## LOCAL EXECUTION & AUDIT PROTOCOL
This architecture is designed for immediate local deployment for auditing and testing purposes. 

**1. Clone the Architecture**
```bash
git clone <https://github.com/biancamzullo/diamond-etl-copilot.git>
cd <diamond-etl-copilot>
```

**2. Install uv (If not already installed)**
```bash
# On macOS via Homebrew
brew install uv

# On Linux / Windows
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**3. Inject Authentication**
Create a `.env` file in the root directory and supply your Google GenAI API credential:
```text
GOOGLE_API_KEY="your_api_key_here"
```

**4. Ignite the Interface**
`uv` automatically resolves dependencies from `pyproject.toml`, manages the virtual environment, and executes the application in a single command:
```bash
uv run streamlit run app.py
```





