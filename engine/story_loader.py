# engine/story_loader.py
import os
import yaml

def load_story(path="story"):
    story = {}
    for fname in os.listdir(path):
        if fname.endswith(".yaml"):
            prefix = fname[:-5]  # убираем .yaml
            full_path = os.path.join(path, fname)
            with open(full_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            for key, value in data.items():
                full_key = f"{prefix}.{key}"
                if full_key in story:
                    print(f"[Предупреждение: дубликат сцены {full_key}]")
                story[full_key] = value
    return story
