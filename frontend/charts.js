/**
 * Chart rendering for sentiment dashboard. Used by app.js.
 * Expects Chart.js to be loaded globally.
 */
(function (global) {
  "use strict";

  let chartInstance = null;

  function renderSentimentChart(sentiments, elementId) {
    var el = document.getElementById(elementId || "sentimentChart");
    if (!el) return;
    if (chartInstance) {
      chartInstance.destroy();
      chartInstance = null;
    }
    chartInstance = new Chart(el, {
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
    return chartInstance;
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
    renderKeywords: renderKeywords
  };
})(typeof window !== "undefined" ? window : this);
