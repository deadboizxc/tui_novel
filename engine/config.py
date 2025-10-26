import json
import os
import yaml

CONFIG_FILE_JSON = "config.json"
CONFIG_FILE_YAML = "config.yaml"
DEFAULT_CONFIG = {
    "save_format": "pickle",  # Формат сохранения игры (pickle или json)
    "config_format": "json",  # Формат конфига (json или yaml)
    "save_dir": "saves"       # Папка для сохранений
}

def load_config():
    """Загружает настройки из config.json или config.yaml."""
    if os.path.exists(CONFIG_FILE_JSON):
        try:
            with open(CONFIG_FILE_JSON, "r", encoding="utf-8") as f:
                config = json.load(f)
                config["config_format"] = "json"
                return config
        except Exception as e:
            print(f"[Ошибка загрузки {CONFIG_FILE_JSON}: {e}]")
            return DEFAULT_CONFIG
    elif os.path.exists(CONFIG_FILE_YAML):
        try:
            with open(CONFIG_FILE_YAML, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
                config["config_format"] = "yaml"
                return config
        except Exception as e:
            print(f"[Ошибка загрузки {CONFIG_FILE_YAML}: {e}]")
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    """Сохраняет настройки в указанном формате (json или yaml)."""
    config_format = config.get("config_format", "json")
    config_file = CONFIG_FILE_JSON if config_format == "json" else CONFIG_FILE_YAML

    try:
        # Создаём папку для сохранений, если она указана и не существует
        save_dir = config.get("save_dir", "saves")
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir)

        if config_format == "json":
            with open(CONFIG_FILE_JSON, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        else:  # yaml
            with open(CONFIG_FILE_YAML, "w", encoding="utf-8") as f:
                yaml.safe_dump(config, f, allow_unicode=True)
        print(f"[Настройки сохранены в {config_file}]")

        # Удаляем файл другого формата
        other_file = CONFIG_FILE_YAML if config_format == "json" else CONFIG_FILE_JSON
        if os.path.exists(other_file):
            os.remove(other_file)
    except Exception as e:
        print(f"[Ошибка сохранения {config_file}: {e}]")
