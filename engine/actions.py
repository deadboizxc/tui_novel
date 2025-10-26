import time
from .animations import spinner_animation, dots_animation, pulse_text

def perform_actions(gs, actions):
    for action in actions or []:
        perform_action(gs, action)

def perform_action(gs, action):
    if isinstance(action, dict):
        key, value = next(iter(action.items()))
        match key:
            case "set_flag": 
                gs.flags[value] = True
            case "unset_flag": 
                gs.flags[value] = False
            case "jump": 
                gs.current = _normalize_target(gs, value)
            case "add_coin": 
                _update_stat(gs, "coins", int(value))
            case "remove_coin": 
                _update_stat(gs, "coins", -int(value))
            case "animate": 
                _handle_animation(value)
            case _: 
                print(f"[Неизвестное действие: {key}]")
        return

    if isinstance(action, str):
        parts = action.split()
        if not parts: return
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None
        if cmd == "jump" and arg: 
            gs.current = _normalize_target(gs, arg)
        elif cmd == "add_coin" and arg: 
            _update_stat(gs, "coins", int(arg))
        else: 
            print(f"[Неизвестная строковая команда: {action}]")

def _normalize_target(gs, target):
    if "." not in target and "." in gs.current:
        chapter = gs.current.split(".")[0]
        return f"{chapter}.{target}"
    return target

def _update_stat(gs, key, delta):
    old = gs.stats.get(key, 0)
    new = max(0, old + delta)
    gs.stats[key] = new
    print(f"[{'+' if delta >=0 else ''}{delta} {key}] → {new}")

def _handle_animation(anim):
    if isinstance(anim, str):
        anim_type, text, duration = anim, "Анимация", 3
    elif isinstance(anim, dict):
        anim_type = anim.get("type", "spinner")
        text = anim.get("text", "Анимация")
        duration = anim.get("duration", 3)
    else:
        print(f"[Ошибка анимации: {anim}]")
        return

    # Запускаем анимацию
    if anim_type == "spinner":
        spinner_animation(text, duration)
    elif anim_type == "dots":
        dots_animation(text, duration)
    elif anim_type == "pulse":
        pulse_text(text, duration)
    else:
        print(f"[Неизвестная анимация: {anim_type}]")
