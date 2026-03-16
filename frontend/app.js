/**
 * Product Sentiment Dashboard – main app logic.
 * Uses API_BASE for all requests. Loads reviews and analytics, handles search/filters and add review.
 */
(function (global) {
  "use strict";

  // Configurable API base – change for production or different backend
  var API_BASE = "http://127.0.0.1:5000";

  var allReviews = [];
  var currentFilter = { sentiment: "", rating: "" };

  function setLoading(loading) {
    var el = document.getElementById("loadingIndicator");
    var list = document.getElementById("reviewsList");
    if (el) el.style.display = loading ? "block" : "none";
    if (list) list.style.visibility = loading ? "hidden" : "visible";
  }

  function showError(message, containerId) {
    var id = containerId || "errorMessage";
    var el = document.getElementById(id);
    if (el) {
      el.textContent = message || "Something went wrong.";
      el.style.display = "block";
    }
  }

  function clearError(containerId) {
    var id = containerId || "errorMessage";
    var el = document.getElementById(id);
    if (el) el.style.display = "none";
  }

  function loadReviews() {
    setLoading(true);
    clearError();
    var url = API_BASE + "/reviews";
    var params = [];
    if (currentFilter.sentiment) params.push("sentiment=" + encodeURIComponent(currentFilter.sentiment));
    if (currentFilter.rating) params.push("rating=" + encodeURIComponent(currentFilter.rating));
    if (params.length) url += "?" + params.join("&");

    fetch(url)
      .then(function (res) { return res.json(); })
      .then(function (result) {
        setLoading(false);
        if (result.status === "error") {
          showError(result.message || "Failed to load reviews.");
          allReviews = [];
          displayReviews([]);
          return;
        }
        var data = result.data;
        if (!Array.isArray(data)) data = [];
        allReviews = data;
        displayReviews(data);
      })
      .catch(function (err) {
        setLoading(false);
        showError("Network error: " + (err.message || "Could not reach server."));
        allReviews = [];
        displayReviews([]);
      });
  }

  function displayReviews(reviews) {
    var list = document.getElementById("reviewsList");
    if (!list) return;
    list.innerHTML = "";
    if (!reviews || reviews.length === 0) {
      var li = document.createElement("li");
      li.textContent = "No reviews found.";
      li.className = "empty";
      list.appendChild(li);
      return;
    }
    reviews.forEach(function (r) {
      var li = document.createElement("li");
      var text = (r.review_text != null ? r.review_text : r.review || "").trim() || "(no text)";
      var sentiment = (r.sentiment || "neutral").toUpperCase();
      var rating = r.rating != null ? r.rating : "–";
      var product = (r.product || "").trim();
      var productLine = product ? "<small>Product: " + product + "</small><br>" : "";
      var fakeProb = typeof r.fake_probability === "number" ? r.fake_probability : 0;
      var badge = "";
      if (fakeProb >= 0.6) {
        badge = '<span class="badge badge-warning">Suspicious (' + (fakeProb * 100).toFixed(0) + '%)</span> ';
      } else if (fakeProb >= 0.3) {
        badge = '<span class="badge badge-soft">Check (' + (fakeProb * 100).toFixed(0) + '%)</span> ';
      }
      li.innerHTML = badge + "<b>" + sentiment + "</b> | ⭐ " + rating + "<br>" + productLine + text;
      list.appendChild(li);
    });
  }

  function searchProduct() {
    var keyword = (document.getElementById("productInput") && document.getElementById("productInput").value) || "";
    keyword = keyword.toLowerCase().trim();
    if (!keyword) {
      displayReviews(allReviews);
      return;
    }
    var filtered = allReviews.filter(function (r) {
      var t = (r.review_text != null ? r.review_text : r.review || "").toLowerCase();
      return t.indexOf(keyword) !== -1;
    });
    displayReviews(filtered);
  }

  function applyFilters() {
    currentFilter.sentiment = (document.getElementById("sentimentFilter") && document.getElementById("sentimentFilter").value) || "";
    currentFilter.rating = (document.getElementById("ratingFilter") && document.getElementById("ratingFilter").value) || "";
    loadReviews();
  }

  function submitReview() {
    var productEl = document.getElementById("newReviewProduct");
    var ratingEl = document.getElementById("newReviewRating");
    var textEl = document.getElementById("newReviewText");
    var msgEl = document.getElementById("submitReviewMessage");
    if (!textEl || !ratingEl) return;
    var product = productEl ? productEl.value.trim() : "";
    var rating = parseInt(ratingEl.value, 10);
    var reviewText = textEl.value.trim();
    if (!reviewText) {
      if (msgEl) { msgEl.textContent = "Please enter review text."; msgEl.style.color = "#f44336"; }
      return;
    }
    if (isNaN(rating) || rating < 1 || rating > 5) {
      if (msgEl) { msgEl.textContent = "Rating must be 1–5."; msgEl.style.color = "#f44336"; }
      return;
    }
    if (msgEl) msgEl.textContent = "Submitting…";
    fetch(API_BASE + "/reviews", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product: product, rating: rating, review_text: reviewText })
    })
      .then(function (res) { return res.json(); })
      .then(function (result) {
        if (result.status === "error") {
          if (msgEl) { msgEl.textContent = result.message || "Submit failed."; msgEl.style.color = "#f44336"; }
          return;
        }
        if (msgEl) { msgEl.textContent = "Review added! Sentiment: " + (result.data && result.data.sentiment ? result.data.sentiment : ""); msgEl.style.color = "#4CAF50"; }
        if (textEl) textEl.value = "";
        loadReviews();
        loadAnalytics();
      })
      .catch(function (err) {
        if (msgEl) { msgEl.textContent = "Network error."; msgEl.style.color = "#f44336"; }
      });
  }

  function loadAnalytics() {
    setLoading(true);
    fetch(API_BASE + "/analytics")
      .then(function (res) { return res.json(); })
      .then(function (result) {
        setLoading(false);
        if (result.status === "error") {
          showError(result.message || "Failed to load analytics.");
          return;
        }
        var d = result.data || {};
        var sentiments = d.sentiment_count || { positive: 0, neutral: 0, negative: 0 };
        var rating = d.average_rating != null ? d.average_rating : 0;
        var total = d.total_reviews != null ? d.total_reviews : 0;
        var keywords = d.top_keywords || [];
        if (global.DashboardCharts) {
          global.DashboardCharts.renderSentimentChart(sentiments);
          global.DashboardCharts.renderInsight(sentiments);
          global.DashboardCharts.renderAvgRating(rating);
          global.DashboardCharts.renderTotalReviews(total);
          global.DashboardCharts.renderKeywords(keywords);
        }
        // update positive share stat
        var posShareEl = document.getElementById("positiveShare");
        if (posShareEl) {
          var totalSent = sentiments.positive + sentiments.neutral + sentiments.negative;
          var pct = totalSent ? Math.round((sentiments.positive / totalSent) * 100) : 0;
          posShareEl.textContent = pct.toString() + "%";
        }
      })
      .catch(function (err) {
        setLoading(false);
        showError("Analytics: " + (err.message || "Could not reach server."));
      });
  }

  function onDomReady() {
    setLoading(true);
    Promise.all([
      fetch(API_BASE + "/reviews").then(function (res) { return res.json(); }),
      fetch(API_BASE + "/analytics").then(function (res) { return res.json(); }),
      fetch(API_BASE + "/analytics/products").then(function (res) { return res.json(); }),
      fetch(API_BASE + "/analytics/trends").then(function (res) { return res.json(); }),
      fetch(API_BASE + "/insights/summary").then(function (res) { return res.json(); })
    ]).then(function (results) {
      var reviewsResult = results[0];
      var analyticsResult = results[1];
      var productsResult = results[2];
      var trendsResult = results[3];
      var insightsResult = results[4];
      setLoading(false);
      if (reviewsResult.status === "error") {
        showError(reviewsResult.message || "Failed to load reviews.");
        allReviews = [];
      } else {
        var data = Array.isArray(reviewsResult.data) ? reviewsResult.data : [];
        allReviews = data;
        displayReviews(data);
      }
      if (analyticsResult.status === "error") {
        showError(analyticsResult.message || "Failed to load analytics.");
      } else {
        var d = analyticsResult.data || {};
        var sentiments = d.sentiment_count || { positive: 0, neutral: 0, negative: 0 };
        var rating = d.average_rating != null ? d.average_rating : 0;
        var total = d.total_reviews != null ? d.total_reviews : 0;
        var keywords = d.top_keywords || [];
        if (global.DashboardCharts) {
          global.DashboardCharts.renderSentimentChart(sentiments);
          global.DashboardCharts.renderInsight(sentiments);
          global.DashboardCharts.renderAvgRating(rating);
          global.DashboardCharts.renderTotalReviews(total);
          global.DashboardCharts.renderKeywords(keywords);
        }
        var posShareEl = document.getElementById("positiveShare");
        if (posShareEl) {
          var totalSent = sentiments.positive + sentiments.neutral + sentiments.negative;
          var pct = totalSent ? Math.round((sentiments.positive / totalSent) * 100) : 0;
          posShareEl.textContent = pct.toString() + "%";
        }
      }

      if (productsResult.status !== "error" && productsResult.data) {
        if (global.DashboardCharts) {
          global.DashboardCharts.renderProductComparison(productsResult.data);
        }
      }

      if (trendsResult.status !== "error" && trendsResult.data) {
        if (global.DashboardCharts) {
          global.DashboardCharts.renderTrend(trendsResult.data);
        }
      }

      if (insightsResult.status !== "error" && insightsResult.data) {
        var summaryEl = document.getElementById("aiSummary");
        if (summaryEl) summaryEl.textContent = insightsResult.data.summary || "";
      }
    }).catch(function (err) {
      setLoading(false);
      showError("Could not reach server: " + (err.message || ""));
    });
    var searchBtn = document.getElementById("searchBtn");
    if (searchBtn) searchBtn.addEventListener("click", searchProduct);
    var filterBtn = document.getElementById("filterBtn");
    if (filterBtn) filterBtn.addEventListener("click", applyFilters);
    var submitBtn = document.getElementById("submitReviewBtn");
    if (submitBtn) submitBtn.addEventListener("click", submitReview);
    var input = document.getElementById("productInput");
    if (input) input.addEventListener("keypress", function (e) { if (e.key === "Enter") searchProduct(); });
  }

  if (typeof document !== "undefined" && document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", onDomReady);
  } else {
    onDomReady();
  }

  global.ProductSentimentApp = {
    loadReviews: loadReviews,
    loadAnalytics: loadAnalytics,
    displayReviews: displayReviews,
    searchProduct: searchProduct,
    applyFilters: applyFilters,
    submitReview: submitReview,
    getApiBase: function () { return API_BASE; }
  };
})(typeof window !== "undefined" ? window : this);
