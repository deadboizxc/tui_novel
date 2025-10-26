# engine/ui.py
import os
import sys
import time
from .config import load_config, save_config
from .state import list_saves, save_game, load_game

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def type_text(text, delay=None):  # Исправлено: delay=None
    config = load_config()
    # Загружаем delay из конфига, если не передан явно
    delay = config.get("type_delay", 0.02) if delay is None else delay
    # Заменяем плейсхолдеры в тексте
    text = text.format(
        config_format=config.get("config_format", "json"),
        save_format=config.get("save_format", "pickle"),
        save_dir=config.get("save_dir", "saves")
    )
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    print("")

def prompt_choice(choices):
    for i, ch in enumerate(choices, 1):
        print(f"{i}) {ch.get('text', '...')}")
    print("\n[s] Настройки  [v] Сохранить  [l] Загрузить  [q] Выйти")
    return input("> ").strip().lower()

def prompt_settings():
    config = load_config()
    while True:
        clear_screen()
        print("--- Настройки игры ---\n")
        print(f"1) Каталог сохранений: {config.get('save_dir', 'saves')}")
        print(f"2) Формат сохранений: {config.get('save_format', 'pickle')}")
        print(f"3) Формат конфигурации: {config.get('config_format', 'json')}")
        print(f"4) Задержка текста: {config.get('type_delay', 0.02)} сек")
        print("\n[b] Назад")
        choice = input("> ").strip().lower()

        if choice == "1":
            new_dir = input("Введите путь к каталогу сохранений: ").strip()
            if new_dir:
                config['save_dir'] = new_dir
        elif choice == "2":
            new_fmt = input("Введите формат сохранений (json/pickle): ").strip().lower()
            if new_fmt in ['json', 'pickle']:
                config['save_format'] = new_fmt
            else:
                print("[Ошибка: допустимо только json или pickle]")
                time.sleep(0.5)
        elif choice == "3":
            new_cfg = input("Введите формат конфигурации (json/yaml): ").strip().lower()
            if new_cfg in ['json', 'yaml']:
                config['config_format'] = new_cfg
            else:
                print("[Ошибка: допустимо только json или yaml]")
                time.sleep(0.5)
        elif choice == "4":
            try:
                new_delay = float(input("Введите задержку текста в секундах: ").strip())
                config['type_delay'] = max(0, new_delay)
            except ValueError:
                print("[Ошибка: введите число]")
                time.sleep(0.5)
        elif choice == "b":
            break
        else:
            print("[Неверный выбор]")
            time.sleep(0.5)

        save_config(config)
        print("[Настройки сохранены]")
        time.sleep(0.5)

def prompt_save(gs):
    config = load_config()
    save_dir = config.get("save_dir", "saves")
    os.makedirs(save_dir, exist_ok=True)
    saves = list_saves()
    ext = ".json" if config.get("save_format") == "json" else ".dat"

    clear_screen()
    print("--- Сохранение ---\n")
    if saves:
        print("Существующие сохранения:")
        for i, s in enumerate(saves, 1):
            print(f"{i}) {s}")
    print(f"\n[n] Новое сохранение")
    print("[b] Назад")
    choice = input("> ").strip().lower()

    if choice == "n":
        name = input(f"Введите имя файла (без расширения): ").strip()
        if name:
            save_file = os.path.join(save_dir, f"{name}{ext}")
            save_game(gs, save_file)
            print("[Сохранено]")
            time.sleep(0.5)
    elif choice == "b":
        return
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(saves):
                save_file = os.path.join(save_dir, saves[idx])
                save_game(gs, save_file)
                print("[Сохранено]")
                time.sleep(0.5)
            else:
                print("Неверный выбор")
        except ValueError:
            print("Неверный ввод")
            time.sleep(0.5)

def prompt_load():
    config = load_config()
    save_dir = config.get("save_dir", "saves")
    saves = list_saves()
    if not saves:
        print("[Нет сохранений]")
        time.sleep(0.5)
        return None

    clear_screen()
    print("--- Загрузка ---\n")
    for i, s in enumerate(saves, 1):
        print(f"{i}) {s}")
    print("\n[b] Назад")
    choice = input("> ").strip().lower()

    if choice == "b":
        return None

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(saves):
            return load_game(os.path.join(save_dir, saves[idx]))
        else:
            print("Неверный выбор")
    except ValueError:
        print("Неверный ввод")
    time.sleep(0.5)
    return None
