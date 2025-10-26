import pickle
import json
import os
from .config import load_config

class GameState:
    def __init__(self, start_scene="prologue.start"):
        self.current = start_scene
        self.history = [start_scene]
        self.vars = {"pills_taken": 0, "sanity": 100, "loop_count": 0}
        self.items = {}  # Изменено с set() на {} для хранения предметов с количеством
        self.flags = {}
        self.stats = {"coins": 100}

    def __repr__(self):
        return f"<{self.current} | coins: {self.stats.get('coins')} | items: {self.items}>"


def save_game(gs, save_file=None):
    """Сохраняет игровое состояние в указанном файле."""
    config = load_config()
    save_format = config.get("save_format", "pickle")
    save_dir = config.get("save_dir", "saves")

    # Создаём папку, если не существует
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Если save_file не указан, используем имя по умолчанию
    save_file = save_file or os.path.join(save_dir, "save.dat" if save_format == "pickle" else "save.json")

    if save_format == "json":
        try:
            data = {
                "current": gs.current,
                "history": gs.history,
                "flags": gs.flags,
                "stats": gs.stats
            }
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[Сохранено в {save_file}]")
        except Exception as e:
            print(f"[Ошибка сохранения в JSON: {e}]")
    else:  # pickle
        try:
            with open(save_file, "wb") as f:
                pickle.dump(gs, f)
            print(f"[Сохранено в {save_file}]")
        except Exception as e:
            print(f"[Ошибка сохранения в Pickle: {e}]")

def load_game(save_file=None):
    """Загружает игровое состояние из указанного файла."""
    config = load_config()
    save_format = config.get("save_format", "pickle")
    save_dir = config.get("save_dir", "saves")

    save_file = save_file or os.path.join(save_dir, "save.dat" if save_format == "pickle" else "save.json")

    if not os.path.exists(save_file):
        print(f"[Файл {save_file} не найден]")
        return None

    if save_format == "json":
        try:
            with open(save_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                gs = GameState(data["current"])
                gs.history = data["history"]
                gs.flags = data["flags"]
                gs.stats = data["stats"]
                return gs
        except Exception as e:
            print(f"[Ошибка загрузки JSON: {e}]")
            return None
    else:  # pickle
        try:
            with open(save_file, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            print(f"[Ошибка загрузки Pickle: {e}]")
            return None

def list_saves():
    """Возвращает список файлов сохранений в папке."""
    config = load_config()
    save_dir = config.get("save_dir", "saves")
    save_format = config.get("save_format", "pickle")
    ext = ".json" if save_format == "json" else ".dat"

    if not os.path.exists(save_dir):
        return []

    return [f for f in os.listdir(save_dir) if f.endswith(ext)]








