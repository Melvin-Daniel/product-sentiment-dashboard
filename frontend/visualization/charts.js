async function loadAnalytics() {
    try {
        const response = await fetch("http://127.0.0.1:5000/analytics");
        const result = await response.json();

        const sentiments = result.data.sentiment_count;
        const rating = result.data.average_rating;

        renderSentimentChart(sentiments);
        renderAvgRating(rating);

    } catch (error) {
        console.error("Error loading analytics:", error);
    }
}

function renderSentimentChart(sentiments) {

    const ctx = document.getElementById("sentimentChart");

    new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Positive", "Neutral", "Negative"],
            datasets: [{
                data: [
                    sentiments.positive,
                    sentiments.neutral,
                    sentiments.negative
                ],
                backgroundColor: [
                    "#4CAF50",
                    "#FFC107",
                    "#F44336"
                ]
            }]
        }
    });
}

function renderAvgRating(rating) {
    document.getElementById("avgRating").innerText =
        "⭐ Average Rating: " + rating.toFixed(2);
}

loadAnalytics();