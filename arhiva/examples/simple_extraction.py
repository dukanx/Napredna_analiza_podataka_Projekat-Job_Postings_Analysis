"""
Structured extraction example using Llama 3.3 70B.

This example demonstrates:
- structured LLM outputs
- prompt engineering with anti-patterns
- reasoning/extraction separation
- post-processing validation

Run:
    python examples/validated_extraction.py
"""

import os
from typing import List

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


# Schema Definition

class JobAnalysis(BaseModel):

    reasoning: str = Field(
        description="Internal reasoning used during extraction"
    )

    tech_stack: List[str]

    red_flags: List[str]

    green_flags: List[str]


# Prompt

SYSTEM_PROMPT = """You are a Data Extraction Robot. Extract job characteristics as SHORT PHRASES.

CRITICAL RULES:
1. Output 1-5 word phrases ONLY
2. NO sentences, NO explanations, NO commentary
3. Use 'reasoning' field to think, then extract cleanly

CORRECT EXTRACTION:
Input: "Fast-paced startup seeking rockstars who thrive under pressure"
Output: 
  reasoning: "Multiple red flags present: fast-paced, rockstar terminology, pressure culture"
  red_flags: ["fast-paced", "rockstar", "thrive under pressure"]

WRONG EXTRACTION (DO NOT DO THIS):
Output:
  red_flags: ["fast-paced is mentioned which suggests", "there are pressure indicators"]

RED FLAGS - Toxic culture indicators:
- "fast-paced", "wear many hats", "we are a family"
- "rockstar", "ninja", "guru" (unprofessional terminology)
- "work under pressure", "tight deadlines"

GREEN FLAGS - Tangible benefits only:
- Compensation: "401k", "stock options", "bonus"
- Time off: "unlimited PTO", "flexible hours"
- Insurance: "health insurance", "dental"
- Work setup: "remote work", "home office stipend"

TECH STACK - Software/tools/languages only:
- YES: Python, AWS, Docker, React, PostgreSQL
- NO: "Fortune 500", "strong skills", "collaborative team"

Extract EXACT phrases from text. If nothing found, return empty list.
"""


# Validation Layer

def clean_extraction(items: List[str]) -> List[str]:

    cleaned = []

    prose_indicators = [
        "is mentioned",
        "suggests",
        "implies",
        "there are",
        "however"
    ]

    for item in items:

        item = item.strip()

        # Remove commentary leakage
        if any(signal in item.lower() for signal in prose_indicators):
            continue

        # Enforce short phrases
        if len(item.split()) > 6:
            continue

        # Remove noise
        if item.lower() in ["no", "yes", "n/a"]:
            continue

        cleaned.append(item)

    return cleaned


# LLM Setup

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        'Missing GROQ_API_KEY.\n'
        'Example:\n'
        'export GROQ_API_KEY="your_key_here"'
    )

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=GROQ_API_KEY,
    temperature=0
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "{job_posting}")
])

structured_llm = prompt | llm.with_structured_output(JobAnalysis)


# Sample Job Posting

JOB_POSTING = """
Senior Python Developer - Remote

We are a fast-paced startup building cutting-edge AI analytics tools.
Join our founding team and help us disrupt the industry!

Requirements:
- 5+ years Python experience
- Django, Flask
- PostgreSQL, Redis
- Docker, Kubernetes
- AWS (EC2, S3, Lambda)
- Strong problem-solving skills

What we offer:
- Competitive salary + equity
- Remote work with flexible hours
- Health insurance (medical, dental, vision)
- 401k with 4% company match
- Unlimited PTO
- Annual learning budget ($2000)
- Home office stipend

Culture:
We're a team of rockstars who thrive under pressure and wear many hats.
Fast-paced environment where you'll hit the ground running!
"""


# Extraction Pipeline

def extract(job_text: str) -> JobAnalysis:

    result = structured_llm.invoke({
        "job_posting": job_text
    })

    result.tech_stack = clean_extraction(result.tech_stack)
    result.red_flags = clean_extraction(result.red_flags)
    result.green_flags = clean_extraction(result.green_flags)

    return result


# Run Example

if __name__ == "__main__":

    try:

        print("LLM EXTRACTION PIPELINE - VALIDATION EXAMPLE")
        
        result = extract(JOB_POSTING)

        print("REASONING (internal model analysis):") 
        print(f" {result.reasoning}\n")

        print("Tech Stack:")
        for item in result.tech_stack:
            print(f" - {item}")

        print("\nRed Flags:")
        for item in result.red_flags:
            print(f" - {item}")

        print("\nGreen Flags:")
        for item in result.green_flags:
            print(f" - {item}")

    except Exception as e:

        print(f"\nExtraction failed:\n{e}")