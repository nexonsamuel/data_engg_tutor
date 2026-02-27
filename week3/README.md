# MedProfile — LLM-Powered Medication Intelligence Demo

**Project Overview**  
MedProfile is a tool-enabled LLM application designed to provide structured medication profiles by integrating multiple data sources. It demonstrates deterministic tool calling, multi-source data integration, and safe healthcare data handling. The project progresses across three phases, starting from a single-source prototype to a multi-tool, multi-aspect system.

---

# Folder Structure (Phase 2 / Phase 3 Multi-Source Architecture)
```
medprofile/
│
├── app/
│ ├── main.py
│ ├── config.py
│ │
│ ├── llm/
│ │ ├── client.py
│ │ ├── prompts.py
│ │ └── tools.py
│ │
│ ├── tools/
│ │ └── drug_profile_tool.py
│ │
│ ├── services/
│ │ ├── openfda_client.py
│ │ ├── rxnorm_service.py
│ │ └── atc_service.py
│ │
│ ├── db/
│ │ ├── database.py
│ │ ├── rxnorm.db
│ │ └── atc.db
│ │
│ └── models/
│ └── schemas.py
│
├── data/
│ ├── rxnorm_raw/
│ └── atc_raw/
│
├── scripts/
│ ├── import_rxnorm.py
│ └── import_atc.py
│
├── requirements.txt
├── README.md
└── run.py

```

**Notes on Folder Structure:**  
- `llm/` isolates all AI logic (prompts, tool definitions, LLM calls).  
- `tools/` contains the exposed tools for the LLM — Phase 2 and Phase 3 have separate tool files for clarity.  
- `services/` encapsulates API and database interactions — keeps LLM logic separate from raw data retrieval.  
- `db/` stores processed databases for RxNorm and ATC.  
- `scripts/` contain utilities to convert raw CSV or text files into usable databases.  

---

# Phase 1 — Single Tool, Single Source

**Objective:**  
Create a simple LLM tool demonstrating controlled tool calling using one external API.

**Scope:**  
- Input: A single medication name from the user.  
- Tool: `get_drug_label(drug_name)`  
- Data Source: OpenFDA API  

**Folder Structure:**  
```
medprofile/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── llm/
│   │   ├── client.py
│   │   ├── prompts.py
│   │   └── tools.py            # Defines get_drug_label tool
│   │
│   ├── tools/
│   │   └── drug_label_tool.py  # Queries OpenFDA API
│   │
│   ├── models/
│   │   └── schemas.py          # Output schema definitions
│   │
│   ├── requirements.txt
│   ├── README.md
│   └── run.py
```

**Outputs:**  
- Brand name  
- Generic name  
- Active ingredient  
- Purpose / indication  
- Key warnings  

**Instructions:**  
1. Create a system prompt instructing the LLM to **always call `get_drug_label`** and **not generate medical advice**.  
2. Implement the tool to query the OpenFDA API, retrieve label data, and structure it clearly.  
3. Have the LLM summarize the returned structured data in simple, readable language.  
4. Validate that the system handles missing drugs or errors gracefully.  

**Goal:**  
Showcase deterministic tool usage and safe, readable healthcare information.

---

# Phase 2 — Multi-Source Aggregation

**Objective:**  
Extend the single-tool system to integrate multiple structured data sources while maintaining a single exposed tool to the LLM.

**Scope:**  
- Input: A single medication name.  
- Tool: `get_drug_profile(drug_name)`  
- Data Sources:  

| Source   | Type     | Purpose |
|----------|----------|---------|
| OpenFDA  | API      | Label + warnings |
| RxNorm   | SQLite   | Normalize brand ↔ generic names |
| ATC      | SQLite   | Classify drug by therapeutic category |

**Folder Structure:**  
```
medprofile/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── llm/
│   │   ├── client.py
│   │   ├── prompts.py
│   │   └── tools.py            # Defines get_drug_profile tool
│   │
│   ├── tools/
│   │   └── drug_profile_tool.py  # Multi-source aggregation logic
│   │
│   ├── services/
│   │   ├── openfda_client.py
│   │   ├── rxnorm_service.py
│   │   └── atc_service.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── rxnorm.db
│   │   └── atc.db
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── data/
│   │   ├── rxnorm_raw/
│   │   └── atc_raw/
│   │
│   ├── scripts/
│   │   ├── import_rxnorm.py
│   │   └── import_atc.py
│   │
│   ├── requirements.txt
│   ├── README.md
│   └── run.py
```

**Outputs:**  
- Input name  
- Normalized generic name  
- RxNorm identifier  
- ATC code  
- Drug class  
- Purpose  
- Key warnings  

**Instructions:**  
1. Normalize the user input via RxNorm to handle different brand or generic names.  
2. Query ATC classification database to identify the drug's therapeutic class.  
3. Retrieve regulatory label data and warnings from OpenFDA.  
4. Merge all data into a single structured output.  
5. The LLM formats the merged data into a readable summary for the user.  

**Goal:**  
Demonstrate **multi-source integration** with a **single tool interface**, showing the ability to merge API and database data deterministically.

---

# Phase 3 — Multi-Tool / Multi-Aspect Extension

**Objective:**  
Introduce multi-drug reasoning and therapeutic alternatives while internally orchestrating multiple tools, without exposing complexity to the user.

**Scope:**  
- Input: One or more medication names.  
- Tool: `get_drug_insights(drugs: list[str])`  
- Internal Data Sources: OpenFDA, RxNorm, ATC, plus interaction / alternatives logic  

**Behavior:**  

| Input Type        | Output / Tool Behavior                                                                 |
|------------------|--------------------------------------------------------------------------------------|
| Single drug       | Returns normalized profile + therapeutic alternatives within the same drug class.    |
| Two or more drugs | Returns normalized profiles + checks for drug-drug interactions and severity.        |

**Folder Structure:**  

```
medprofile/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── llm/
│   │   ├── client.py
│   │   ├── prompts.py
│   │   └── tools.py              # Defines get_drug_profile + get_drug_insights tools
│   │
│   ├── tools/
│   │   ├── drug_profile_tool.py
│   │   └── drug_insights_tool.py  # Multi-drug insights & interaction logic
│   │
│   ├── services/
│   │   ├── openfda_client.py
│   │   ├── rxnorm_service.py
│   │   ├── atc_service.py
│   │   └── interaction_service.py  # New service to check interactions
│   │
│   ├── db/
│   │   ├── database.py
│   │   ├── rxnorm.db
│   │   ├── atc.db
│   │   └── interactions.db          # New interaction database (optional)
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── data/
│   │   ├── rxnorm_raw/
│   │   ├── atc_raw/
│   │   └── interactions_raw/        # Raw interaction data (optional)
│   │
│   ├── scripts/
│   │   ├── import_rxnorm.py
│   │   ├── import_atc.py
│   │   └── import_interactions.py   # New import script (optional)
│   │
│   ├── requirements.txt
│   ├── README.md
│   └── run.py
```

**Outputs:**  
- Normalized profiles for each input drug  
- ATC classification and drug class  
- Key warnings  
- Therapeutic alternatives for single drugs  
- Interaction information for multiple drugs  

**Instructions:**  
1. Determine if the user input contains a single or multiple medications.  
2. For each drug, normalize names and fetch classification and label warnings (Phase 2 logic).  
3. If more than one drug is provided, check for interactions and merge interaction data.  
4. If only one drug is provided, fetch therapeutic alternatives from the same ATC class.  
5. Return a structured output that the LLM can summarize clearly for the user.  

**Goal:**  
Demonstrate **multi-tool orchestration**, **conditional reasoning based on user input**, and **multi-source merging** while maintaining a single, clean interface for the LLM.

---

# Key Principles Across All Phases

- **Tool-First Design:** The LLM must rely on tools for all data; never generate medical information from memory.  
- **Deterministic Outputs:** All outputs are structured and based on data sources.  
- **Safe Healthcare Handling:** No diagnosis or treatment recommendations. Only factual summaries.  
- **Extensible Architecture:** Folder structure allows easy addition of new tools, data sources, or features.  
- **Readable Summaries:** The LLM formats all structured output for layman-friendly display.  

---

# Progressive Growth

| Phase | Complexity | LLM Exposure | Multi-Source Integration | Multi-Tool Logic |
|-------|------------|--------------|--------------------------|----------------|
| 1     | Basic      | Single tool  | Single API               | None           |
| 2     | Intermediate | Single tool | API + RxNorm + ATC      | None           |
| 3     | Advanced    | Single tool  | Multi-source + logic     | Conditional multi-tool |
