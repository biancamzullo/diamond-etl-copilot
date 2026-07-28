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

---

## LOCAL EXECUTION & AUDIT PROTOCOL
This architecture is designed for immediate local deployment for auditing and testing purposes. 

**1. Clone the Architecture**
```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

**2. Isolate the Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Inject Authentication**
Create a `.env` file in the root directory and supply your Google GenAI API credential:
```text
GOOGLE_API_KEY="your_api_key_here"
```

**4. Ignite the Interface**
```bash
streamlit run app.py
```




