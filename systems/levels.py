# levels.py

def get_level(index):
    levels = [
        {
            "name": "Level 1",
            "merch_count": 10,
            "hazard_count": 3,
            "hazard_speed": 120
        },
        {
            "name": "Level 2",
            "merch_count": 12,
            "hazard_count": 5,
            "hazard_speed": 140
        }       
    ]

    # If level exists, return it
    if index < len(levels):
        return levels[index]

    # Infinite scaling for later levels
    base = levels[-1]
    extra = index - len(levels) + 1

    return {
        "name": f"Level {index + 1}",
        "merch_count": base["merch_count"] + extra * 2,
        "hazard_count": base["hazard_count"] + extra,
        "hazard_speed": base["hazard_speed"] + extra * 10
    }
