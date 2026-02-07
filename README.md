# Circular Economy PHA Life Cycle Assessment (LCA) Toolkit

## Overview
This repository hosts a custom Life Cycle Assessment (LCA) pipeline designed to evaluate the environmental impacts of Polyhydroxyalkanoates (PHA) production. 

Originally developed to validate circular CO₂ economy models, this toolkit has evolved into a prospective analysis engine for ChakraTech’s proprietary Methanol-to-PHA technology, integrating technical process improvements with global policy scenarios.

## Project Evolution & Methodology

### Phase 1: Validation & Replication (Palm Oil to PHA)
**Goal:** Establish a baseline by replicating the results of the study *"Polyhydroxyalkanoates (PHA) production in a circular CO2 economy"* (Elsevier, 2025).
* **Challenge:** Lack of access to the licensed EcoInvent database.
* **Solution:** Built a manual LCI database in Excel by aggregating impact factors from open-source literature for all inputs (materials, chemicals, electricity).
* **Output:** Validated the manual calculation method against the published study's results.

### Phase 2: Proprietary Technology Assessment (Methanol to PHA)
**Goal:** Apply the validated methodology to ChakraTech's specific production process.
* **Process:** Gathered primary LCI data for the Methanol-to-PHA pathway.
* **Pipeline:** Developed a data engineering workflow to export complex LCA calculations from Excel into structured JSON, enabling dynamic visualization and analysis in Python (Matplotlib).

### Phase 3: Prospective LCA & Optimization
**Goal:** Model the future potential of the technology.
* **Methodology:** Performed prospective LCA modeling to quantify how improvements in **conversion rates** and **strain yields** could reduce Global Warming Potential (GWP) over time.
* **Tech Stack:** Python scripts ingest the prospective scenarios from JSON to generate comparative impact charts.

### Phase 4: Policy Integration (Current)
**Collaborators:** UCSD School of Global Policy and Strategy.
* **Objective:** Integrating policy levers (carbon pricing, subsidies, mandates) into the prospective LCA to understand the economic and environmental viability of Methanol-to-PHA alongside other feedstocks.

## Technology Stack
* **Core Logic:** Python (Pandas, NumPy)
* **Visualization:** Matplotlib
* **Data Storage:** Excel (LCI/LCIA calculations) -> JSON (Interchange format)
* **Version Control:** Git/GitHub

## Roadmap: The Move to Automation
The next stage of development focuses on migrating from static Excel-based models to a fully automated, matrix-based LCA framework.
* **Platform:** Migration to **Brightway2**.
* **Data:** Integration with open-source databases (USLCI) or licensed datasets (EcoInvent) to replace manual impact factor aggregation.

## Usage
1.  **Data Ingestion:**
    Ensure raw LCI data is present in the `data/raw` directory (Excel format).
2.  **Processing:**
    Run the extraction script to convert Excel models to JSON:
    ```bash
    python src/extract_lci.py
    ```
3.  **Visualization:**
    Generate impact reports and prospective comparison graphs:
    ```bash
    python src/visualization.py
    ```

---
*Developed during an internship at ChakraTech (Jan 2026 - Present).*
