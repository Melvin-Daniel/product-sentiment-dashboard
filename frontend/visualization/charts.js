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
