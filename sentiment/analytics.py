def sentiment_summary(results):

    pos = 0
    neg = 0
    neu = 0

    for r in results:

        if r["sentiment_label"] == "positive":
            pos += 1

        elif r["sentiment_label"] == "negative":
            neg += 1

        else:
            neu += 1

    total = len(results)

    return {

        "positive_percent": round((pos/total)*100,2),

        "negative_percent": round((neg/total)*100,2),

        "neutral_percent": round((neu/total)*100,2)

    }
