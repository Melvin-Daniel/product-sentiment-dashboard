/**
 * Chart rendering for sentiment dashboard. Used by app.js.
 * Expects Chart.js to be loaded globally.
 */
(function (global) {
  "use strict";

  let sentimentChartInstance = null;
  let productChartInstance = null;
  let trendChartInstance = null;

  function renderSentimentChart(sentiments, elementId) {
    var el = document.getElementById(elementId || "sentimentChart");
    if (!el) return;
    if (sentimentChartInstance) {
      sentimentChartInstance.destroy();
      sentimentChartInstance = null;
    }
    sentimentChartInstance = new Chart(el, {
      type: "doughnut",
      data: {
        labels: ["Positive", "Neutral", "Negative"],
        datasets: [{
          data: [
            sentiments.positive || 0,
            sentiments.neutral || 0,
            sentiments.negative || 0
          ],
          backgroundColor: ["#4CAF50", "#FFC107", "#F44336"]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: { color: "white", font: { size: 14 } }
          },
          tooltip: {
            callbacks: {
              label: function (context) {
                var total = context.dataset.data.reduce(function (a, b) { return a + b; }, 0);
                var pct = total ? Math.round((context.raw / total) * 100) : 0;
                return context.label + ": " + context.raw + " (" + pct + "%)";
              }
            }
          }
        }
      }
    });
    return sentimentChartInstance;
  }

  function renderInsight(sentiments, elementId) {
    var el = document.getElementById(elementId || "insight");
    if (!el) return;
    var p = sentiments.positive || 0, n = sentiments.neutral || 0, neg = sentiments.negative || 0;
    var max = Math.max(p, n, neg);
    var message = "No reviews yet.";
    if (max > 0) {
      if (max === p) message = "Most customer reviews are Positive 👍";
      else if (max === n) message = "Most customer reviews are Neutral 🙂";
      else message = "Most customer reviews are Negative ⚠️";
    }
    el.textContent = message;
  }

  function renderAvgRating(rating, elementId) {
    var el = document.getElementById(elementId || "avgRating");
    if (!el) return;
    var val = typeof rating === "number" ? rating : parseFloat(rating) || 0;
    el.textContent = "⭐ Average Rating: " + val.toFixed(2);
  }

  function renderTotalReviews(total, elementId) {
    var el = document.getElementById(elementId || "totalReviews");
    if (!el) return;
    el.textContent = "Total Reviews: " + (total || 0);
  }

  function renderKeywords(keywords, elementId) {
    var el = document.getElementById(elementId || "keywordsList");
    if (!el) return;
    if (!keywords || !keywords.length) {
      el.innerHTML = "<li>No keywords yet.</li>";
      return;
    }
    el.innerHTML = keywords.slice(0, 10).map(function (k) {
      return "<li><span class=\"kw-word\">" + escapeHtml(k.word) + "</span> <span class=\"kw-count\">" + k.count + "</span></li>";
    }).join("");
  }

  function renderProductComparison(products, elementId) {
    var el = document.getElementById(elementId || "productChart");
    if (!el) return;
    if (productChartInstance) {
      productChartInstance.destroy();
      productChartInstance = null;
    }
    if (!products || !products.length) {
      return;
    }
    var labels = products.map(function (p) { return p.product; });
    var positives = products.map(function (p) { return p.positive || 0; });
    var neutrals = products.map(function (p) { return p.neutral || 0; });
    var negatives = products.map(function (p) { return p.negative || 0; });

    productChartInstance = new Chart(el, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          { label: "Positive", backgroundColor: "#4CAF50", data: positives },
          { label: "Neutral", backgroundColor: "#FFC107", data: neutrals },
          { label: "Negative", backgroundColor: "#F44336", data: negatives }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: { color: "white", font: { size: 12 } }
          }
        },
        scales: {
          x: {
            ticks: { color: "white" }
          },
          y: {
            ticks: { color: "white" },
            beginAtZero: true
          }
        }
      }
    });
  }

  function renderTrend(trend, elementId) {
    var el = document.getElementById(elementId || "trendChart");
    if (!el) return;
    if (trendChartInstance) {
      trendChartInstance.destroy();
      trendChartInstance = null;
    }
    if (!trend || !trend.dates || !trend.dates.length) {
      return;
    }
    trendChartInstance = new Chart(el, {
      type: "line",
      data: {
        labels: trend.dates,
        datasets: [
          { label: "Positive", borderColor: "#4CAF50", data: trend.positive || [], tension: 0.2 },
          { label: "Neutral", borderColor: "#FFC107", data: trend.neutral || [], tension: 0.2 },
          { label: "Negative", borderColor: "#F44336", data: trend.negative || [], tension: 0.2 }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            labels: { color: "white", font: { size: 12 } }
          }
        },
        scales: {
          x: { ticks: { color: "white" } },
          y: { ticks: { color: "white" }, beginAtZero: true }
        }
      }
    });
  }

  function escapeHtml(s) {
    var div = document.createElement("div");
    div.textContent = s;
    return div.innerHTML;
  }

  global.DashboardCharts = {
    renderSentimentChart: renderSentimentChart,
    renderInsight: renderInsight,
    renderAvgRating: renderAvgRating,
    renderTotalReviews: renderTotalReviews,
    renderKeywords: renderKeywords,
    renderProductComparison: renderProductComparison,
    renderTrend: renderTrend
  };
})(typeof window !== "undefined" ? window : this);
