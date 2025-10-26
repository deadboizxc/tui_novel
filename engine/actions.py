import time
from .animations import (
    spinner_animation,
    dots_animation,
    pulse_text,
    static_effect,
    glitch_effect,
)

def perform_actions(gs, actions):
    if not actions:
        return

    action_messages = []  # Собираем все сообщения действий
    
    for action in actions:
        if not isinstance(action, dict):
            continue

        for key, value in action.items():
            message = _handle_action(gs, key, value)
            if message:
                action_messages.append(message)
    
    # Выводим все действия одним блоком с отступами
    if action_messages:
        print()  # Отступ сверху
        print("=" * 40)
        print("ДЕЙСТВИЯ:")
        for msg in action_messages:
            print(f"  {msg}")  # Отступ для каждого действия
        print("=" * 40)
        print()  # Отступ снизу

def _handle_action(gs, key, value):
    """Обрабатывает действие и возвращает сообщение для отображения"""
    match key:
        case "jump":
            gs.current = value
            return f"→ ПЕРЕХОД: {value}"
        case "set_flag":
            gs.flags[value] = True
            return f"✓ ФЛАГ: {value}"
        case "unset_flag":
            gs.flags[value] = False
            return f"✗ ФЛАГ: {value}"
        case "add_coin":
            old_coins = gs.stats.get("coins", 0)
            new_coins = old_coins + int(value)
            # Проверяем, чтобы монеты не ушли в минус
            if new_coins < 0:
                new_coins = 0
            gs.stats["coins"] = new_coins
            if int(value) >= 0:
                return f"💰 +{value} монет → {new_coins}"
            else:
                return f"💰 {value} монет → {new_coins}"
        case "remove_coin":
            old_coins = gs.stats.get("coins", 0)
            new_coins = max(0, old_coins - int(value))
            gs.stats["coins"] = new_coins
            return f"💰 -{value} монет → {new_coins}"
        case "increment":
            gs.vars[value] = gs.vars.get(value, 0) + 1
            return f"📈 +1 {value} → {gs.vars[value]}"
        case "decrement":
            gs.vars[value] = max(0, gs.vars.get(value, 0) - 1)
            return f"📉 -1 {value} → {gs.vars[value]}"
        case "set_var":
            messages = []
            for k, v in value.items():
                gs.vars[k] = v
                messages.append(f"⚙️ {k} = {v}")
            return "\n  ".join(messages)  # Отступ для многострочных сообщений
        case "add_item":
            if isinstance(value, str):
                # Добавляем предмет с количеством 1
                gs.items[value] = gs.items.get(value, 0) + 1
                return f"🎁 +{value}"
            elif isinstance(value, dict):
                messages = []
                for item, count in value.items():
                    gs.items[item] = gs.items.get(item, 0) + count
                    messages.append(f"🎁 +{count} {item}")
                return "\n  ".join(messages)  # Отступ для многострочных сообщений
            elif isinstance(value, list):
                # Обработка списка предметов (для обратной совместимости)
                messages = []
                for item in value:
                    gs.items[item] = gs.items.get(item, 0) + 1
                    messages.append(f"🎁 +{item}")
                return "\n  ".join(messages)
        case "remove_item":
            if value in gs.items:
                gs.items[value] = max(0, gs.items.get(value, 0) - 1)
                if gs.items[value] == 0:
                    del gs.items[value]
                return f"🎁 -{value}"
        case "animate":
            if isinstance(value, dict):
                anim_type = value.get("type", "glitch")
                text = value.get("text", "")
                duration = value.get("duration", 2)
                delay = value.get("delay")
            else:
                anim_type, text, duration = "glitch", "", 2
                delay = None

            # Обработка всех типов анимаций с передачей delay
            if anim_type == "glitch":
                glitch_effect(text, duration)
            elif anim_type == "static":
                static_effect(duration)
            elif anim_type == "spinner":
                if delay is not None:
                    spinner_animation(text, duration, delay)
                else:
                    spinner_animation(text, duration)
            elif anim_type == "dots":
                if delay is not None:
                    dots_animation(text, duration, delay)
                else:
                    dots_animation(text, duration)
            elif anim_type == "pulse":
                if delay is not None:
                    pulse_text(text, duration, delay)
                else:
                    pulse_text(text, duration)
            else:
                return f"❓ Неизвестная анимация: {anim_type}"
            return f"🎬 Анимация: {anim_type}"
        case _:
            return f"❓ Неизвестное действие: {key}"
    
    return None  # Если действие не требует сообщения


def _normalize_target(gs, target):
    """Нормализует цель перехода, добавляя главу если нужно"""
    if "." not in target and "." in gs.current:
        chapter = gs.current.split(".")[0]
        return f"{chapter}.{target}"
    return target
