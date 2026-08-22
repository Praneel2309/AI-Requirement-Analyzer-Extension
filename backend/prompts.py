AMBIGUITY_PROMPT = """
You are an expert Software Requirements Engineer.

Analyze the following meeting transcript.

Your task is to identify statements that are:
1. vague
2. ambiguous
3. incomplete
4. subjective
5. missing measurable constraints

For every problematic statement, provide:
- original_statement
- issue
- why_it_is_ambiguous
- clarification_question

Return ONLY valid JSON in this format:

{
  "ambiguities": [
    {
      "original_statement": "...",
      "issue": "...",
      "why_it_is_ambiguous": "...",
      "clarification_question": "..."
    }
  ]
}

Meeting transcript:
"""


REQUIREMENT_PROMPT = """
You are an expert Software Requirements Engineer.

Analyze the meeting transcript below and generate software requirements.

Generate:

1. Functional Requirements
2. Non-Functional Requirements

For every requirement provide:
- id
- requirement
- category
- source
- measurable_criteria
- ambiguity_level

NFR categories may include:
- Performance
- Security
- Reliability
- Fairness
- Explainability
- Accuracy
- Usability
- Scalability

Return ONLY valid JSON:

{
  "functional_requirements": [],
  "non_functional_requirements": []
}

Meeting transcript:
"""


REFINEMENT_PROMPT = """
You are an expert Software Requirements Engineer.

You are given:
1. Original meeting transcript
2. Clarification questions
3. Stakeholder answers

Using all three, generate refined Functional and Non-Functional Requirements.

The refined requirements must be:
- specific
- measurable where possible
- testable
- unambiguous
- implementation independent where possible

Return ONLY valid JSON:

{
  "functional_requirements": [],
  "non_functional_requirements": []
}

Original transcript:
"""


EVALUATION_PROMPT = """
You are a Software Requirements Engineering evaluator.

Compare two sets of requirements:

A. Requirements generated WITHOUT clarification
B. Requirements generated WITH clarification

Evaluate both using:

1. Completeness
2. Clarity
3. Specificity
4. Testability
5. Unambiguity

Give each criterion a score from 1 to 10.

Also provide:
- overall_before
- overall_after
- improvement_percentage
- explanation

Return ONLY JSON:

{
  "before": {
    "completeness": 0,
    "clarity": 0,
    "specificity": 0,
    "testability": 0,
    "unambiguity": 0,
    "overall": 0
  },
  "after": {
    "completeness": 0,
    "clarity": 0,
    "specificity": 0,
    "testability": 0,
    "unambiguity": 0,
    "overall": 0
  },
  "improvement_percentage": 0,
  "explanation": ""
}
"""
