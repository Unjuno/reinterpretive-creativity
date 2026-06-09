from scripts.breakdown_gap import breakdown_gap


def reinterpretation_breakdown_gap(data):
    results = data["results"]
    target = results["reinterpretation"]
    winner_name = max(results, key=lambda name: results[name]["score"])
    winner = results[winner_name]
    return {
        "target_method": "reinterpretation",
        "winner_method": winner_name,
        "gap": breakdown_gap(target, winner),
    }
