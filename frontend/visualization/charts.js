function renderSentimentChart(data) {
  new Chart(document.getElementById("sentimentChart"), {
    type: "pie",
    data: {
      labels: ["Positive", "Neutral", "Negative"],
      datasets: [{
        data: [data.positive, data.neutral, data.negative]
      }]
    }
  });
}