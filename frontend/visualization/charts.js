
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
    },
    options: {
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.label + " Reviews: " + context.raw;
                    }
                }
            }
        }
    }
});
           
}

function renderAvgRating(rating) {
    document.getElementById("avgRating").innerText =
        "⭐ Average Rating: " + rating.toFixed(2);
}

loadAnalytics();
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
                    "#4CAF50",   // Green
                    "#FFC107",   // Yellow
                    "#F44336"    // Red
                ]
            }]
        }
    });

    renderInsight(sentiments);
}

function renderInsight(sentiments) {
    let max = Math.max(
        sentiments.positive,
        sentiments.neutral,
        sentiments.negative
    );

    let message = "";

    if (max === sentiments.positive) {
        message = "Most customer reviews are Positive 👍";
    } else if (max === sentiments.neutral) {
        message = "Most customer reviews are Neutral 🙂";
    } else {
        message = "Most customer reviews are Negative ⚠️";
    }

    document.getElementById("insight").innerText = message;
}
