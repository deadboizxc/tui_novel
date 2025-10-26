# engine/conditions.py
def check_conditions(gs, conditions):
    if not conditions:
        return True
    for cond in conditions:
        if "flag" in cond:
            if not gs.flags.get(cond["flag"], False):
                return False
        elif "coins" in cond:
            if gs.stats.get("coins", 0) < cond["coins"]:
                return False
    return True
