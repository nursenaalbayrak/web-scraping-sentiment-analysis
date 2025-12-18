def calculate_confidence(results):
    if not results:
        return "Low"

    total = len(results)
    neutral = sum(1 for r in results if r["sentiment"] == "Neutral")
    ratio = neutral / total

    if total < 5:
        return "Low"
    elif ratio > 0.6:
        return "Low"
    elif ratio > 0.3:
        return "Medium"
    else:
        return "High"
