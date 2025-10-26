# engine/story_loader.py
import os
import yaml
from pathlib import Path

def load_story(path="story"):
    story = {}
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Папка не найдена: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Указанный путь не является папкой: {path}")

    yaml_files = list(path.glob("*.yaml")) + list(path.glob("*.yml"))

    if not yaml_files:
        print(f"[Предупреждение: в папке {path} не найдено .yaml или .yml файлов]")
        return story

    for file_path in yaml_files:
        prefix = file_path.stem  # имя файла без расширения
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"[Ошибка при чтении {file_path.name}: {e}]")
            continue

        if not isinstance(data, dict):
            print(f"[Предупреждение: {file_path.name} не содержит словарь на верхнем уровне]")
            continue

        for key, value in data.items():
            full_key = f"{prefix}.{key}"
            if full_key in story:
                print(f"[Предупреждение: дубликат сцены {full_key} в {file_path.name}]")
            story[full_key] = value

    return story
