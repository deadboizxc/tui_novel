def check_conditions(gs, conditions):
    if not conditions:
        return True
        
    if isinstance(conditions, list):
        for cond in conditions:
            if not _check_single_condition(gs, cond):
                return False
        return True
    else:
        return _check_single_condition(gs, conditions)

def _check_single_condition(gs, cond):
    if not isinstance(cond, dict):
        return True
        
    # Проверка флагов
    if "flag" in cond:
        if not gs.flags.get(cond["flag"], False):
            return False
            
    # Проверка предметов
    if "has" in cond:
        # Проверяем, есть ли предмет и его количество > 0
        if cond["has"] not in gs.items or gs.items[cond["has"]] <= 0:
            return False
            
    # Проверка переменных
    if "var" in cond:
        var_name = cond["var"]
        var_value = gs.vars.get(var_name, 0)
        
        if "more" in cond and not (var_value > cond["more"]):
            return False
        if "less" in cond and not (var_value < cond["less"]):
            return False
        if "equal" in cond and not (var_value == cond["equal"]):
            return False
        if "not" in cond and not (var_value != cond["not"]):
            return False
            
    # Проверка монет
    if "coins" in cond:
        current_coins = gs.stats.get("coins", 0)
        if current_coins < cond["coins"]:
            return False
            
    return True
