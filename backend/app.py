from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from google import genai

from prompts import (
    AMBIGUITY_PROMPT,
    REQUIREMENT_PROMPT,
    REFINEMENT_PROMPT,
    EVALUATION_PROMPT
)

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def ask_ai(prompt):
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "")
        text = text.replace("```", "")

    return json.loads(text)


@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json

    transcript = data.get("transcript", "")

    if not transcript:
        return jsonify({"error": "Transcript is required"}), 400

    result = ask_ai(
        AMBIGUITY_PROMPT + "\n" + transcript
    )

    return jsonify(result)


@app.route("/requirements", methods=["POST"])
def requirements():

    data = request.json

    transcript = data.get("transcript", "")

    result = ask_ai(
        REQUIREMENT_PROMPT + "\n" + transcript
    )

    return jsonify(result)


@app.route("/refine", methods=["POST"])
def refine():

    data = request.json

    transcript = data.get("transcript", "")
    clarifications = data.get("clarifications", "")

    prompt = (
        REFINEMENT_PROMPT
        + "\n\nTRANSCRIPT:\n"
        + transcript
        + "\n\nCLARIFICATION RESPONSES:\n"
        + clarifications
    )

    result = ask_ai(prompt)

    return jsonify(result)


@app.route("/evaluate", methods=["POST"])
def evaluate():

    data = request.json

    before = data.get("before", {})
    after = data.get("after", {})

    prompt = (
        EVALUATION_PROMPT
        + "\n\nWITHOUT CLARIFICATION:\n"
        + json.dumps(before)
        + "\n\nWITH CLARIFICATION:\n"
        + json.dumps(after)
    )

    result = ask_ai(prompt)

    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "running"
    })

@app.route("/export/pdf", methods=["POST"])
def export_pdf():

    data = request.json

    ambiguities = data.get("ambiguities", [])
    before = data.get("before", {})
    after = data.get("after", {})
    evaluation = data.get("evaluation", {})

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Requirement Analyzer - Requirement Analysis Report",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # Ambiguities
    story.append(
        Paragraph("1. Detected Ambiguities", styles["Heading1"])
    )

    for i, item in enumerate(ambiguities, 1):

        story.append(
            Paragraph(
                f"<b>Issue {i}</b>",
                styles["Heading2"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Statement:</b> {item.get('original_statement', '')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Problem:</b> {item.get('why_it_is_ambiguous', '')}",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"<b>Clarification Question:</b> "
                f"{item.get('clarification_question', '')}",
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 10))

    # Before requirements
    story.append(
        Paragraph(
            "2. Requirements Without Clarification",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            json.dumps(before, indent=2).replace("\n", "<br/>"),
            styles["Code"]
        )
    )

    story.append(Spacer(1, 20))

    # After requirements
    story.append(
        Paragraph(
            "3. Refined Requirements",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            json.dumps(after, indent=2).replace("\n", "<br/>"),
            styles["Code"]
        )
    )

    story.append(Spacer(1, 20))

    # Evaluation
    story.append(
        Paragraph(
            "4. Requirement Quality Evaluation",
            styles["Heading1"]
        )
    )

    story.append(
        Paragraph(
            json.dumps(evaluation, indent=2).replace("\n", "<br/>"),
            styles["Code"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="AI_Requirement_Analysis_Report.pdf"
    )

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
