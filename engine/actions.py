import time
from .animations import spinner_animation, dots_animation, progress_bar
from .config import load_config, save_config

def perform_actions(gs, actions):
    for action in actions or []:
        perform_action(gs, action)

def perform_action(gs, action):
    if not isinstance(action, dict):
        return
    key, value = next(iter(action.items()))

    match key:
        case "set_flag":
            gs.flags[value] = True
        case "add_coin":
            gs.stats["coins"] = gs.stats.get("coins", 0) + int(value)
            print(f"[+{value} coins] → {gs.stats['coins']}")
        case "animate":
            handle_animation(value)
        case "jump":
            gs.current = _normalize_target(gs, value)
        case "set_config_format":
            config = load_config()
            config["config_format"] = value
            save_config(config)
            print(f"[Формат конфига изменён на {value}]")
            time.sleep(0.5)
        case "set_save_format":
            config = load_config()
            config["save_format"] = value
            save_config(config)
            print(f"[Формат сохранения изменён на {value}]")
            time.sleep(0.5)
        case "set_save_dir":
            config = load_config()
            if value == "prompt":
                new_dir = input("").strip()
                if new_dir:
                    config["save_dir"] = new_dir
                    save_config(config)
                    print(f"[Папка сохранений изменена на {new_dir}]")
                else:
                    print("[Папка не изменена]")
            else:
                config["save_dir"] = value
                save_config(config)
                print(f"[Папка сохранений изменена на {value}]")
            time.sleep(0.5)

def handle_animation(anim):
    if isinstance(anim, str):
        anim = {"type": anim, "text": "Анимация", "duration": 3}

    anim_type = anim.get("type", "spinner")
    text = anim.get("text", "...")
    duration = anim.get("duration", 3)

    if anim_type == "spinner":
        spinner_animation(text, duration=duration)
    elif anim_type == "dots":
        dots_animation(text, duration=duration)
    elif anim_type == "bar":
        progress_bar(text, duration=duration)
    else:
        print(f"[Неизвестная анимация: {anim_type}]")

def _normalize_target(gs, target):
    if target == "back":
        return gs.history[-2] if len(gs.history) > 1 else gs.current
    if "." in target:
        return target
    if "." in gs.current:
        prefix = gs.current.split(".", 1)[0]
        return f"{prefix}.{target}"
    return target
