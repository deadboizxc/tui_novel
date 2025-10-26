from .actions import perform_actions, _normalize_target
from .conditions import check_conditions
from .ui import clear_screen, type_text

class SceneManager:
    def __init__(self, story, game_state):
        self.story = story
        self.gs = game_state
    
    def process_current_scene(self):
        """Обрабатывает текущую сцену и возвращает результат"""
        scene = self.story.get(self.gs.current)
        
        if not scene:
            return self._handle_missing_scene()
        
        if not self._check_scene_conditions(scene):
            return self._handle_failed_conditions(scene)
        
        self._display_scene(scene)
        return self._execute_scene_actions(scene)
    
    def _handle_missing_scene(self):
        """Обрабатывает отсутствующую сцену"""
        print(f"[Ошибка: сцена {self.gs.current} не найдена]")
        fallback_scene = self.gs.current.split('.')[0] + '.start'
        if fallback_scene in self.story and fallback_scene != self.gs.current:
            print(f"[Переход к {fallback_scene}]")
            self.gs.current = fallback_scene
            return "scene_changed"
        return "exit"
    
    def _check_scene_conditions(self, scene):
        """Проверяет условия сцены"""
        conditions = scene.get("conditions")
        return check_conditions(self.gs, conditions)
    
    def _handle_failed_conditions(self, scene):
        """Обрабатывает невыполненные условия"""
        print(f"[Условия не выполнены для {self.gs.current}]")
        if "fallback" in scene:
            self.gs.current = _normalize_target(self.gs, scene["fallback"])
            return "scene_changed"
        return "exit"
    
    def _display_scene(self, scene):
        """Отображает сцену"""
        clear_screen()
        print(f"--- {self.gs.current} ---\n")
        
        text = scene.get("text")
        if text:
            type_text(text + "\n")
    
    def _execute_scene_actions(self, scene):
        """Выполняет действия сцены"""
        previous_scene = self.gs.current
        perform_actions(self.gs, scene.get("actions", []))
        
        if self.gs.current != previous_scene:
            return "scene_changed"
        return "continue"
    
    def get_available_choices(self, scene):
        """Возвращает доступные выборы для сцены"""
        return [
            ch for ch in scene.get("choices", [])
            if check_conditions(self.gs, ch.get("conditions"))
        ]
    
    def execute_choice(self, choice):
        """Выполняет выбранный вариант"""
        previous_scene = self.gs.current
        perform_actions(self.gs, choice.get("actions", []))
        
        if self.gs.current != previous_scene:
            return "scene_changed"
        
        next_scene = choice.get("next") or choice.get("jump")
        if next_scene:
            self.gs.current = _normalize_target(self.gs, next_scene)
            return "scene_changed"
        
        print("\n(Конец пути — нет next/jump)")
        return "exit"
