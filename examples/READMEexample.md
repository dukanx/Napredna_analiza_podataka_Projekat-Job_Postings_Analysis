# Extraction Examples

This folder contains usage examples for the LLM extraction pipeline.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install langchain langchain-groq pydantic
```

### 3. Set API Key

```bash
export GROQ_API_KEY="your_groq_api_key"
# On Windows: set GROQ_API_KEY=your_groq_api_key
```

Get your API key at: https://console.groq.com/keys

### 4. Run Example

```bash
python simple_extraction.py
```

## Notes

This example demonstrates the core extraction pipeline used in the main analysis:
- Few-shot prompting with explicit anti-patterns
- Reasoning field separation (cognitive workspace)
- Multi-stage validation (schema + post-processing filters)

For batch processing and retry logic, see the main notebook.

Full architectural details: [`LLM_PIPELINE.md`](../LLM_PIPELINE.md)