const form = document.getElementById("routeForm");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const payload = {
        driver_id: document.getElementById("driver_id").value,
        date: document.getElementById("date").value,
        locations: document.getElementById("locations").value.split(",")
    };

    const response = await fetch("/predict/daily", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    const data = await response.json();

    document.getElementById("resultContainer").classList.remove("hidden");

    document.getElementById("results").innerHTML = `
        <div class="space-y-4">

            <div>
                <strong>Recommended Route:</strong>
                ${data.recommended_route.join(" → ")}
            </div>

            <div>
                <strong>ETA:</strong>
                ${data.predicted_time_hours} hours
            </div>

            <div>
                <strong>Confidence:</strong>
                ${Math.round(data.confidence * 100)}%
            </div>

            <div>
                <strong>Route Score:</strong>
                ${data.route_score}
            </div>

        </div>
    `;
});

const ctx = document.getElementById('confidenceChart');

new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        datasets: [{
            label: 'Confidence',
            data: [88, 91, 89, 93, 94]
        }]
    }
});