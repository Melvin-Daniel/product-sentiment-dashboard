async function loadAnalytics() {
    try {
        const response = await fetch("http://127.0.0.1:5000/analytics");
        const data = await response.json();

        renderSentimentChart(data.sentiment_counts);
        renderAvgRating(data.average_rating);

    } catch (error) {
        console.error("Error loading analytics:", error);
    }
}

function renderSentimentChart(sentiments) {

    const ctx = document.getElementById("sentimentChart");

    new Chart(ctx, {
        type: "doughnut",   // looks more professional than pie
        data: {
            labels: ["Positive", "Neutral", "Negative"],
            datasets: [{
                data: [
                    sentiments.positive,
                    sentiments.neutral,
                    sentiments.negative
                ],
                backgroundColor: [
                    "#4CAF50",   // green
                    "#FFC107",   // yellow
                    "#F44336"    // red
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

function renderAvgRating(rating) {
    document.getElementById("avgRating").innerText =
        "⭐ Average Rating: " + rating.toFixed(1);
}

loadAnalytics();
