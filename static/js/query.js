async function generateSQL() {

    const question =
        document.getElementById("question").value.trim();

    const sqlOutput =
        document.getElementById("sqlOutput");

    const modeBadge =
        document.getElementById("modeBadge");

    const explanation =
        document.getElementById("explanation");

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    sqlOutput.textContent = "Generating SQL...";
    modeBadge.textContent = "PROCESSING";

    // Clear previous explanation
    explanation.textContent =
        "Click Explain to understand this SQL query.";

    try {

        const response = await fetch("/api/generate", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });

        const data = await response.json();

        if (!response.ok || !data.success) {

            sqlOutput.textContent =
                "Error: " + (data.error || "Unable to generate SQL.");

            modeBadge.textContent = "ERROR";

            return;
        }

        sqlOutput.textContent = data.sql;

        modeBadge.textContent =
            data.mode === "ai"
                ? "AI MODE"
                : "DEMO MODE";

    }

    catch (error) {

        console.error(error);

        sqlOutput.textContent =
            "Connection error.";

        modeBadge.textContent = "ERROR";
    }
}


// ========================================
// EXECUTE SQL
// ========================================

async function executeSQL() {

    const question =
        document.getElementById("question").value.trim();

    const sql =
        document.getElementById("sqlOutput").textContent.trim();

    const container =
        document.getElementById("resultContainer");

    const status =
        document.getElementById("resultStatus");

    if (!sql || sql.includes("Your generated SQL")) {

        alert("Generate SQL first.");

        return;
    }

    container.innerHTML =
        "<p>Executing query...</p>";

    status.textContent = "RUNNING";

    try {

        const response = await fetch("/api/execute", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question,
                sql: sql
            })

        });

        const data = await response.json();

        if (!response.ok || !data.success) {

            status.textContent = "ERROR";

            container.innerHTML = `
                <div class="error-box">
                    ❌ ${data.error || "Query execution failed."}
                </div>
            `;

            return;
        }

        status.textContent = "SUCCESS";

        if (!data.rows || data.rows.length === 0) {

            container.innerHTML =
                "<p>No rows returned.</p>";

            return;
        }

        createTable(
            data.columns,
            data.rows,
            container
        );

    }

    catch (error) {

        console.error(error);

        status.textContent = "ERROR";

        container.innerHTML =
            "<p>Unable to execute query.</p>";
    }
}


// ========================================
// CREATE RESULT TABLE
// ========================================

function createTable(columns, rows, container) {

    let html =
        "<div class='table-wrapper'><table>";

    html += "<thead><tr>";

    columns.forEach(column => {

        html += `<th>${column}</th>`;

    });

    html += "</tr></thead>";

    html += "<tbody>";

    rows.forEach(row => {

        html += "<tr>";

        columns.forEach(column => {

            html += `
                <td>
                    ${row[column] ?? ""}
                </td>
            `;

        });

        html += "</tr>";

    });

    html += "</tbody></table></div>";

    container.innerHTML = html;
}


// ========================================
// EXPLAIN SQL
// ========================================

async function explainSQL() {

    const sql =
        document.getElementById("sqlOutput").textContent.trim();

    const explanation =
        document.getElementById("explanation");

    // No SQL
    if (!sql || sql.includes("Your generated SQL")) {

        explanation.innerHTML = `
            <div class="error-box">
                ⚠️ Please generate SQL first.
            </div>
        `;

        return;
    }

    // Show loading
    explanation.innerHTML = `
        <div class="loading">
            🤖 AI is analyzing your SQL query...
        </div>
    `;

    try {

        const response = await fetch("/api/explain", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                sql: sql
            })

        });

        const data = await response.json();

        console.log("Explain API response:", data);

        if (!response.ok || !data.success) {

            explanation.innerHTML = `
                <div class="error-box">
                    ❌ ${data.error || "Unable to explain SQL."}
                </div>
            `;

            return;
        }

        // Show actual explanation
        explanation.textContent =
            data.explanation || "No explanation returned.";

    }

    catch (error) {

        console.error("Explain error:", error);

        explanation.innerHTML = `
            <div class="error-box">
                ❌ Unable to connect to AI explanation service.
            </div>
        `;
    }
}


// ========================================
// CLEAR
// ========================================

function clearQuery() {

    document.getElementById("question").value = "";

    document.getElementById("sqlOutput").textContent =
        "Your generated SQL will appear here...";

    document.getElementById("modeBadge").textContent =
        "Waiting";

    document.getElementById("resultStatus").textContent =
        "No result";

    document.getElementById("resultContainer").innerHTML =
        "<p class='empty'>Run a query to see results.</p>";

    document.getElementById("explanation").textContent =
        "SQL explanation will appear here.";
}