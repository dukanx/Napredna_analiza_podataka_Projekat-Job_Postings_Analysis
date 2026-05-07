
# LLM Extraction Pipeline – Technical Documentation

Scalable structured data extraction from unstructured IT job postings using Llama 3.3 70B.

This document explains the architecture, validation strategy, and engineering decisions behind the LLM extraction pipeline used in the main analysis.

---

# Table of Contents

- [Architecture Overview](#architecture-overview)
- [Core Challenge](#core-challenge)
- [Pipeline Design](#pipeline-design)
- [Validation Strategy](#validation-strategy)
- [Reliability & Batch Processing](#reliability--batch-processing)
- [Code Structure](#code-structure)
- [Example Workflow](#example-workflow)
- [Quality Metrics](#quality-metrics)
- [Key Learnings](#key-learnings)
- [Future Improvements](#future-improvements)

---

# Architecture Overview

The extraction pipeline converts raw job descriptions into validated structured data through multiple stages:

```text
Raw Job Posting
        │
        ▼
LLM Extraction Layer
(Llama 3.3 70B via Groq API)
        │
        ▼
Schema Validation
(Pydantic)
        │
        ▼
Post-Processing & Filtering
        │
        ▼
Clean Structured Dataset
````

Each layer addresses a different class of problems:

| Layer             | Responsibility                                    |
| ----------------- | ------------------------------------------------- |
| LLM extraction    | Semantic understanding and information extraction |
| Schema validation | Structural correctness and type validation        |
| Post-processing   | Noise reduction and semantic cleanup              |

The system was designed with a **defense-in-depth validation philosophy**, where multiple layers compensate for the unreliability of probabilistic model outputs.

---

# Core Challenge

## Schema Compliance ≠ Semantic Quality

The primary challenge was not generating valid JSON — it was generating *high-quality structured information*.

Early versions of the pipeline frequently produced outputs that were structurally correct but semantically unusable.

### Expected Output

```python
{
    "red_flags": ["fast-paced", "work weekends"],
    "green_flags": ["remote work", "401k match"]
}
```

### Early Failure Example

```python
{
    "red_flags": [
        "fast-paced is not mentioned but there are other red flags like",
        "no",
        "work under pressure is not mentioned"
    ]
}
```

Although technically valid under:

```python
List[str]
```

the outputs violated extraction requirements:

* phrases became explanations
* commentary leaked into structured fields
* low-information noise polluted the dataset

At scale, even a modest failure rate becomes significant.

With approximately 1,500 job postings, a 10% contamination rate would produce more than 150 corrupted records requiring cleanup.

---

# Pipeline Design

## 1. Few-Shot Prompting with Explicit Anti-Patterns

A major improvement came from teaching the model both:

* what to do
* what *not* to do

```python
SYSTEM_PROMPT = """
Extract job characteristics.

CRITICAL:
Output SHORT PHRASES ONLY (1-5 words).

CORRECT:
Input: "Fast-paced startup seeking rockstars..."
Output: {"red_flags": ["fast-paced", "rockstar"]}

WRONG:
Output: {"red_flags": ["fast-paced is mentioned which suggests..."]}

NO SENTENCES.
NO EXPLANATIONS.
EXTRACT ONLY.
"""
```
> **Note:** The actual system prompt is ~100 lines and includes:
> - Detailed red flag / green flag criteria with examples
> - Vibe score rubric (1-10 scale with specific indicators)
> - Tech stack extraction rules
> - Edge case handling for ambiguous phrases
> 
> The above example captures the core anti-pattern teaching strategy.

Providing explicit negative examples significantly reduced:

* prose contamination
* explanation leakage
* verbose outputs

This proved more effective than schema enforcement alone.

---

## 2. Separation of Reasoning and Extraction

Another important design decision was separating analytical reasoning from structured extraction.

```python
class JobPostingAnalysis(BaseModel):

    reasoning: str

    tech_stack: List[str]

    red_flags: List[str]

    green_flags: List[str]
```

The `reasoning` field acts as temporary cognitive workspace for the model.

After validation:

* reasoning is discarded
* only structured fields are retained

This separation reduced contamination between:

* analytical commentary
* final extraction output

and noticeably improved consistency.

---

# Validation Strategy

The pipeline uses multiple validation layers to catch different failure modes.

## Post-Processing Filters

```python
def clean_extraction(items: List[str]) -> List[str]:

    cleaned = []

    for item in items:

        prose_signals = [
            "is mentioned",
            "suggests",
            "implies",
            "there are",
            "but"
        ]

        # Filter verbose commentary
        if any(signal in item.lower() for signal in prose_signals):
            continue

        # Enforce short phrases
        if len(item.split()) > 6:
            continue

        # Remove low-information noise
        if item.lower() in ["no", "yes", "n/a"]:
            continue

        cleaned.append(item)

    return cleaned
```

---

## Multi-Layer Validation

The validation strategy operates across three independent layers:

| Layer                   | Purpose                |
| ----------------------- | ---------------------- |
| Prompt constraints      | Behavioral guidance    |
| Pydantic validation     | Structural enforcement |
| Post-processing filters | Semantic cleanup       |

Each layer catches different classes of failures.

This layered approach proved substantially more reliable than relying solely on prompting.

---

# Reliability & Batch Processing

The pipeline includes retry handling and controlled concurrency for stable large-scale extraction.

```python
def process_batch(jobs, max_retries=3):

    attempts = 0

    while attempts < max_retries:

        try:

            results = llm.batch(
                jobs,
                max_concurrency=5
            )

            return results

        except RateLimitError:

            wait_time = 10 + (attempts * 5)

            time.sleep(wait_time)

            attempts += 1

    raise Exception("Max retries exceeded")
```

Key reliability features:

* retry handling
* controlled concurrency
* graceful failure recovery
* rate limit mitigation

The system was intentionally designed assuming:

* failures will happen
* outputs will occasionally degrade
* retries are necessary

This mindset is similar to distributed systems engineering.

---

# Code Structure

```text
ProjekatNAP.ipynb
│
├── Extraction Layer
│   ├── LLM setup
│   ├── Pydantic schemas
│   ├── Prompt templates
│   ├── Batch processing
│   └── Validation pipeline
│
├── Network Analysis
│
└── Correlation Analysis
```

The extraction layer is modular and designed for reuse in future structured extraction tasks.

---

# Example Workflow

> **Note:** The following examples are simplified for readability.
> The actual implementation uses LangChain orchestration together with Pydantic validation.

## Basic Extraction Example

```python
from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY
)

response = llm.invoke(job_text)
```

---

## Batch Processing Example

```python
def extract_batch(job_postings):

    results = []

    for batch in chunks(job_postings, size=5):

        batch_results = process_batch(batch)

        results.extend(batch_results)

    return results
```

---

# Quality Metrics

## Final Pipeline Performance

| Metric                      | Value                          |
| --------------------------- | ------------------------------ |
| Successful Extractions      | ~97% (1,460 / 1,500 jobs)      |
| Manual Validation Precision | ~95% (sample validation, n=50) |
| Processing Time             | ~12 minutes                    |

---

## Common Failure Modes

| Failure Type                | Mitigation              |
| --------------------------- | ----------------------- |
| Rate limit errors           | Retry logic             |
| Malformed structured output | Schema validation       |
| Verbose outputs             | Post-processing filters |
| Empty responses             | Retry handling          |

---

# Key Learnings

## 1. Schema Validation Alone Is Insufficient

Structured outputs still require behavioral constraints.

Reliable extraction systems need:

* prompt engineering
* schema validation
* semantic filtering

—not just JSON formatting.

---

## 2. Separation of Concerns Improves Output Quality

Allowing the model to reason separately from the final structured output reduces contamination between:

* analysis
* extraction

This significantly improves consistency.

---

## 3. Validation Should Be Layered

Different validation mechanisms catch different classes of failures.

No single layer is sufficient on its own.

---

## 4. LLMs Should Be Treated as Probabilistic Components

The system was designed under the assumption that:

* failures are inevitable
* retries are necessary
* outputs may degrade
* graceful recovery matters

This mindset is essential when building scalable AI systems.

---

# Future Improvements

Potential improvements to the extraction pipeline:

* **Native schema-constrained generation** – leverage function calling APIs for stricter output enforcement
* **Systematic prompt evaluation** – A/B testing framework for comparing prompt variants
* **Domain-specific fine-tuning** – custom model trained specifically on job posting extraction
---



# Run Example

```bash
python examples/simple_extraction.py
```

