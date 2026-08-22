const API = "http://127.0.0.1:5000";


let beforeRequirements = null;
let afterRequirements = null;
let ambiguityResults = null;
let evaluationResults = null;


async function post(endpoint, data) {

    const response = await fetch(
        `${API}${endpoint}`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );

    return await response.json();
}


document
    .getElementById("analyzeBtn")
    .addEventListener("click", async () => {

        const transcript =
            document.getElementById("transcript").value;

        const result =
            await post("/analyze", {
                transcript: transcript
            });
        ambiguityResults = result;

        const container =
            document.getElementById("questions");

        container.innerHTML =
            "<h2>Clarification Questions</h2>";

        result.ambiguities.forEach((item, index) => {

            container.innerHTML += `
                <div class="card">

                    <p>
                        <b>Issue ${index + 1}</b>
                    </p>

                    <p>
                        <b>Statement:</b>
                        ${item.original_statement}
                    </p>

                    <p>
                        <b>Problem:</b>
                        ${item.why_it_is_ambiguous}
                    </p>

                    <p class="question">
                        Question:
                        ${item.clarification_question}
                    </p>

                </div>
            `;

        });

    });


document
    .getElementById("requirementsBtn")
    .addEventListener("click", async () => {

        const transcript =
            document.getElementById("transcript").value;

        beforeRequirements =
            await post("/requirements", {
                transcript: transcript
            });

        document.getElementById("results").innerHTML =
            `
            <h2>Requirements Without Clarification</h2>

            <pre>
${JSON.stringify(beforeRequirements, null, 2)}
            </pre>
            `;

    });


document
    .getElementById("refineBtn")
    .addEventListener("click", async () => {

        const transcript =
            document.getElementById("transcript").value;

        const clarifications =
            document.getElementById("clarifications").value;

        afterRequirements =
            await post("/refine", {
                transcript: transcript,
                clarifications: clarifications
            });

        document.getElementById("results").innerHTML =
            `
            <h2>Refined Requirements</h2>

            <pre>
${JSON.stringify(afterRequirements, null, 2)}
            </pre>
            `;

    });


document
    .getElementById("evaluateBtn")
    .addEventListener("click", async () => {

        if (!beforeRequirements || !afterRequirements) {

            alert(
                "Generate both before and after requirements first."
            );

            return;
        }

        const result =
            await post("/evaluate", {
                before: beforeRequirements,
                after: afterRequirements
            });
        evaluationResults = result;

        document.getElementById("results").innerHTML +=
            `
            <h2>Quality Evaluation</h2>

            <pre>
${JSON.stringify(result, null, 2)}
            </pre>
            `;
        document.getElementById("exportButtons").style.display = "block";

    });

document
    .getElementById("exportTxtBtn")
    .addEventListener("click", () => {

        if (
            !beforeRequirements ||
            !afterRequirements ||
            !evaluationResults
        ) {
            alert("Please complete the requirement comparison first.");
            return;
        }

        const report = `
AI REQUIREMENT ANALYZER
=======================

1. DETECTED AMBIGUITIES
=======================

${JSON.stringify(ambiguityResults, null, 2)}


2. REQUIREMENTS WITHOUT CLARIFICATION
=====================================

${JSON.stringify(beforeRequirements, null, 2)}


3. REFINED REQUIREMENTS
=======================

${JSON.stringify(afterRequirements, null, 2)}


4. REQUIREMENT QUALITY EVALUATION
=================================

${JSON.stringify(evaluationResults, null, 2)}
`;

        const blob = new Blob(
            [report],
            { type: "text/plain" }
        );

        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;
        a.download = "AI_Requirement_Analysis_Report.txt";

        a.click();

        URL.revokeObjectURL(url);
    });

document
    .getElementById("exportPdfBtn")
    .addEventListener("click", async () => {

        if (
            !beforeRequirements ||
            !afterRequirements ||
            !evaluationResults
        ) {
            alert("Please complete the requirement comparison first.");
            return;
        }

        const response = await fetch(
            `${API}/export/pdf`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    ambiguities: ambiguityResults
                        ? ambiguityResults.ambiguities
                        : [],

                    before: beforeRequirements,

                    after: afterRequirements,

                    evaluation: evaluationResults
                })
            }
        );

        if (!response.ok) {
            alert("Failed to generate PDF.");
            return;
        }

        const blob = await response.blob();

        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");

        a.href = url;
        a.download =
            "AI_Requirement_Analysis_Report.pdf";

        a.click();

        URL.revokeObjectURL(url);
    });
