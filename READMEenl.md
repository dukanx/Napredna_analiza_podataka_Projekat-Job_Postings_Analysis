# IT Job Market Dynamics Analysis

LLM-powered extraction and network analysis of technologies from LinkedIn job postings.

| | |
|---|---|
| **Course** | Advanced Data Analysis |
| **Author** | Nikola Dukić |
| **Dataset** | LinkedIn Job Postings 2023/2024 (Kaggle) |
| **Scope** | 1,460 IT job postings |

---

## Overview

This project explores the IT job market using a hybrid approach that combines:

1. **LLM-based information extraction** from unstructured job descriptions  
2. **Graph-based analysis** of technology ecosystems  
3. **Statistical analysis** of hiring patterns and candidate engagement  

The core contribution is a **production-oriented LLM pipeline** that transforms noisy, unstructured text into structured, analyzable data.

---

## AI Implementation

This project demonstrates production-grade LLM integration. For technical details on:
- LLM output quality control challenges  
- Prompt engineering strategies  
- Validation pipeline architecture  
- Code structure and usage examples  

See: **[`LLM_PIPELINE.md`](LLM_PIPELINE.md)**

---

## Research Questions

1. **Technology Ecosystem** — How are technologies connected? What are the dominant clusters?  
2. **Salary vs. Skill Breadth** — Does broader knowledge correlate with higher salaries?  
3. **Job Posting Tone** — Do red/green flags influence candidate engagement?  

---

## Methodology

### 1. LLM-Based Extraction

A large language model (**Llama 3.3 70B via Groq API**) is used to extract structured data from raw job descriptions.

Extracted attributes include:
- technology stack (tools, languages, platforms)  
- job tone (red flags / green flags)  
- benefits and compensation signals  

The pipeline is designed with **strict structured output constraints**, ensuring:
- short-phrase extraction (no free-form text)  
- schema validation via Pydantic  
- post-processing cleanup for edge cases  

---

### 2. Network Analysis

A **co-occurrence graph** is built from extracted technologies:

- **Nodes** → technologies  
- **Edges** → co-occurrence within the same job posting  

Applied techniques:
- **Louvain community detection** for cluster discovery  
- **Centrality metrics** (degree, betweenness) for identifying key technologies  

---

### 3. Correlation Analysis

Statistical analysis includes:

- Pearson correlation between **skill diversity** and salary  
- correlation between **job tone** and conversion rate (applications / views)  
- comparison between **technical vs. non-technical roles**  

---

## Results

### 1. Technology Ecosystem

- Identified **7 distinct technology clusters** (after graph cleaning)  
- **Python** and **AWS** emerge as central “bridge” technologies  
- Modularity score: **~0.28**, indicating meaningful but overlapping clusters  

---

### 2. Salary vs. Skill Breadth

| Dataset | Pearson r | Interpretation |
|---|---|---|
| All roles | 0.13 | weak positive correlation |
| Technical roles only | -0.08 | negligible |

**Key Insight — “Cluster 0 Effect”:**

The observed correlation is driven entirely by the difference between:
- non-technical roles (0 clusters, lower salaries)  
- technical roles (1+ clusters, higher salaries)  

Within technical roles, **skill breadth has no meaningful impact on salary**.

> The market does not reward generalists. Specialization and seniority dominate.

---

### 3. Job Tone vs. Candidate Engagement

| Factor | Correlation with conversion rate | Interpretation |
|---|---|---|
| Red flags | -0.09 | negligible negative |
| Green flags | -0.07 | negligible |
| Vibe score | ~0.00 | no effect |

**Key Insight:**

Candidates largely ignore job posting rhetoric.  
Application decisions are driven by **structural factors**:
- job title  
- company  
- salary  
- location  

—not by tone or benefits marketing.

---

## Practical Implications

### For Candidates

- Focus on **specialization**, not broad but shallow knowledge  
- **Python** and **AWS** act as “passport technologies” across domains  
- Job posting tone is not a reliable signal of company quality  

---

### For Employers

- Tone and wording have minimal impact on application rates  
- Clear role definition and **salary transparency** matter more  

---

## Limitations

- **LLM extraction limitations** — even large models introduce noise without strict constraints  
- **Dataset bias** — limited to LinkedIn postings (missing startups, direct hiring, local markets)  
- **Conversion rate metric** — applications/views is an imperfect proxy for engagement  

---

## Tech Stack

| Category | Technologies |
|---|---|
| LLM | Llama 3.3 70B (Groq API), LangChain |
| Data Processing | Pandas, SciPy |
| Graph Analysis | NetworkX, python-louvain |
| Visualization | Matplotlib, Seaborn, PyVis |
| Validation | Pydantic |

---

## Getting Started

### Requirements

```bash
pip install pandas scipy seaborn networkx python-louvain groq langchain
```

## Configuration

Set your Groq API key:

```python
GROQ_API_KEY = "your_api_key_here"
```

# Running the Analysis

### Open and run:
`ProjekatNAP.ipynb`

### Execution Flow
1. **LLM extraction**
2. **Network analysis**
3. **Correlation analysis**

> **Note:** Full dataset extraction may take time. It is recommended to test on a subset first.

### Key Takeaway
This project shows that LLMs can be used as structured data extractors at scale, but only when combined with:
*   **Strict prompting strategies**
*   **Schema validation**
*   **Defensive post-processing**

**In other words:** LLMs are powerful, but not reliable — unless you engineer them to be.
