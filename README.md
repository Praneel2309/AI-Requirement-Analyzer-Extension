# AI Requirement Analyzer

An AI-powered Chrome Extension for analyzing software requirements from meeting transcripts.

## Overview

The AI Requirement Analyzer identifies ambiguous and incomplete statements from meeting transcripts, generates clarification questions, incorporates stakeholder responses, produces refined functional and non-functional requirements, and evaluates requirement quality before and after clarification.

## Features

- Meeting transcript analysis
- Ambiguity detection
- AI-generated clarification questions
- Functional requirement generation
- Non-functional requirement generation
- NFR categorization
- Requirement refinement using stakeholder responses
- Before vs. after requirement comparison
- Requirement quality evaluation
- PDF report export
- TXT report export

## Workflow

Meeting Transcript
→ Ambiguity Detection
→ Clarification Questions
→ Stakeholder Responses
→ Initial Requirements
→ Refined Requirements
→ Quality Evaluation
→ PDF/TXT Export

## Technologies Used

- Python
- Flask
- Google Gemini API
- JavaScript
- HTML
- CSS
- Chrome Extensions API
- ReportLab

## Project Structure

```text
AI_Requirement_Analyzer/
├── backend/
├── extension/
├── data/
├── screenshots/
└── README.md
