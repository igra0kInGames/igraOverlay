import pygame
import keyboard
import ctypes
import json
import os

# Стартовый код дл работы {
# overlay = Overlay() # до while True
# внутри while True
# overlay.draw_begin()
# # мой код
# overlay.draw_end()
# }


class Overlay:
    def __init__(self):
        # 1. Загрузка конфигурации из JSON
        self.DEFAULT_CONF = {
            "target_key": "f4",
            "mode": "toggle"  # Доступные режимы: "hold" (зажатие) или "toggle" (переключение)
        }

        if not os.path.exists("conf.json"):
            with open("conf.json", "w", encoding="utf-8") as f:
                json.dump(self.DEFAULT_CONF, f, indent=4)

        with open("conf.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        self.target_key = config.get("target_key", "f4")
        self.mode = config.get("mode", "toggle").lower()  # Читаем режим из JSON

        # Исправление масштабирования экрана в Windows
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:
            pass

        # Инициализация Pygame
        pygame.init()
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h

        # Хромакей (чистый ядовито-зеленый)
        self.CHROMAKEY_RGB = (0, 254, 0)
        GREEN_COLORREF = 65280  # 0x00FF00 для WinAPI

        # Создание окна на весь экран без рамок
        flags = pygame.NOFRAME
        self.screen = pygame.display.set_mode((self.width, self.height), flags)
        pygame.display.set_caption("Overlay Window")

        # Настройка WinAPI
        self.hwnd = pygame.display.get_wm_info()["window"]
        self.GWL_EXSTYLE = -20
        self.WS_EX_LAYERED = 0x80000
        self.WS_EX_TRANSPARENT = 0x00000020

        # Базовый стиль: многослойное окно
        self.base_style = ctypes.windll.user32.GetWindowLongW(self.hwnd, self.GWL_EXSTYLE)

        # По умолчанию включаем клики насквозь
        ctypes.windll.user32.SetWindowLongW(self.hwnd, self.GWL_EXSTYLE,
                                            self.base_style | self.WS_EX_LAYERED | self.WS_EX_TRANSPARENT)

        # Вырезаем зеленый цвет
        LWA_COLORKEY = 0x1
        ctypes.windll.user32.SetLayeredWindowAttributes(self.hwnd, GREEN_COLORREF, 255, LWA_COLORKEY)

        # Окно всегда поверх остальных
        HWND_TOPMOST = -1
        SWP_NOMOVE = 0x0002
        SWP_NOSIZE = 0x0001
        ctypes.windll.user32.SetWindowPos(self.hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)

        self.visible = False
        self._is_pressed = False

        # Привязка событий в зависимости от выбранного режима
        if self.mode == "hold":
            keyboard.on_press_key(self.target_key, self._on_hold_press)
            keyboard.on_release_key(self.target_key, self._on_hold_release)
        else:  # Режим "toggle" (переключение)
            keyboard.on_press_key(self.target_key, self._on_toggle_press)

        # Скрываем оверлей при старте
        ctypes.windll.user32.ShowWindow(self.hwnd, 0)

        mode_text = "Зажмите" if self.mode == "hold" else "Нажмите"
        print(f"Оверлей готов! Режим: [{self.mode.upper()}]. {mode_text} [{self.target_key.upper()}] для управления.")

    def _show_overlay(self):
        """Внутренний метод для включения отображения окна"""
        self.visible = True
        # Убираем флаг WS_EX_TRANSPARENT, чтобы оверлей стал кликабельным
        ctypes.windll.user32.SetWindowLongW(self.hwnd, self.GWL_EXSTYLE, self.base_style | self.WS_EX_LAYERED)
        ctypes.windll.user32.ShowWindow(self.hwnd, 5)  # SW_SHOW
        ctypes.windll.user32.SetForegroundWindow(self.hwnd)

    def _hide_overlay(self):
        """Внутренний метод для скрытия окна"""
        self.visible = False
        # Возвращаем флаг WS_EX_TRANSPARENT, чтобы клики летели сквозь окно
        ctypes.windll.user32.SetWindowLongW(self.hwnd, self.GWL_EXSTYLE,
                                            self.base_style | self.WS_EX_LAYERED | self.WS_EX_TRANSPARENT)
        ctypes.windll.user32.ShowWindow(self.hwnd, 0)  # SW_HIDE

    # --- Обработчики для режима HOLD (зажатие) ---
    def _on_hold_press(self, e):
        if self._is_pressed:
            return
        self._is_pressed = True
        if not self.visible:
            self._show_overlay()

    def _on_hold_release(self, e):
        self._is_pressed = False
        if self.visible:
            self._hide_overlay()

    # --- Обработчик для режима TOGGLE (переключение) ---
    def _on_toggle_press(self, e):
        if self._is_pressed:
            return
        self._is_pressed = True

        # Переключаем состояние окна
        if self.visible:
            self._hide_overlay()
        else:
            self._show_overlay()

        # Сбрасываем флаг зажатия сразу после клика
        self._is_pressed = False

    def update_events(self):
        """Возвращает список событий Pygame, чтобы мы могли ловить мышку"""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False, []
        return True, events

    def draw_begin(self):
        self.screen.fill(self.CHROMAKEY_RGB)

    def draw_end(self):
        pygame.display.flip()
