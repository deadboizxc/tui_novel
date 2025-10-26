# engine/main.py
import os
import sys
import time
from .config import load_config, save_config
from .state import GameState, save_game, load_game, list_saves
from .ui import clear_screen, type_text, prompt_choice, prompt_save, prompt_load, prompt_settings
from .actions import perform_actions, _normalize_target
from .conditions import check_conditions
from .story_loader import load_story

def run(start_scene="intro.start"):
    """Главный игровой цикл визуальной новеллы."""
    story = load_story()
    gs = GameState(start_scene)

    # === Проверка автозагрузки ===
    config = load_config()
    save_dir = config.get("save_dir", "saves")
    if any(os.path.exists(os.path.join(save_dir, f)) for f in list_saves()):
        ans = input("Загрузить сохранение? (y/n): ").lower().strip()
        if ans == "y":
            if loaded := prompt_load():
                gs = loaded

    while True:
        scene = story.get(gs.current)
        if not scene:
            print(f"[Ошибка: сцена {gs.current} не найдена]")
            return

        if not check_conditions(gs, scene.get("conditions")):
            print(f"[Условия не выполнены для {gs.current}]")
            return

        clear_screen()
        print(f"--- {gs.current} ---\n")
        text = scene.get("text")
        if text:
            type_text(text + "\n")

        perform_actions(gs, scene.get("actions"))

        choices = [
            ch for ch in scene.get("choices", [])
            if check_conditions(gs, ch.get("conditions"))
        ]

        if not choices:
            print("\n(Конец сцены)")
            return

        user_input = prompt_choice(choices)

        # -------------------------------
        # 💾 Управление настройками/сохранением/загрузкой/выходом
        # -------------------------------
        if user_input == "s":
            prompt_settings()  # Вызов из ui.py
            input("Enter -> продолжить ")
            continue
        elif user_input == "v":
            prompt_save(gs)
            input("Enter -> продолжить ")
            continue
        elif user_input == "l":
            if loaded := prompt_load():
                gs = loaded
            input("Enter -> продолжить ")
            continue
        elif user_input == "q":
            ans = input("Сохранить перед выходом? (y/n): ").lower()
            if ans == "y":
                prompt_save(gs)
            return

        # -------------------------------
        # Обработка выбора сцены
        # -------------------------------
        try:
            idx = int(user_input) - 1
            if not (0 <= idx < len(choices)):
                raise ValueError
        except ValueError:  # Исправлено с except Value
            print("Неверный ввод.")
            time.sleep(0.5)
            continue

        selected = choices[idx]
        perform_actions(gs, selected.get("actions"))

        next_scene = selected.get("next") or selected.get("jump")
        if not next_scene:
            if gs.history[-1] == gs.current:
                print("\n(Конец пути — нет next/jump)")
                return
        else:
            gs.current = _normalize_target(gs, next_scene)
        gs.history.append(gs.current)
