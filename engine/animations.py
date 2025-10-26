import sys
import time
import itertools
import random

def spinner_animation(text="Loading", duration=3, delay=0.1):
    """Упрощенная анимация спиннера"""
    end_time = time.time() + duration
    spinner = itertools.cycle("/-\\|")

    while time.time() < end_time:
        c = next(spinner)
        sys.stdout.write(f"\r{text} {c}")
        sys.stdout.flush()
        time.sleep(delay)

    sys.stdout.write("\r" + " "*(len(text)+2) + "\r")
    sys.stdout.flush()

def dots_animation(text="Loading", duration=3, delay=0.4):
    """Упрощенная анимация точек"""
    end_time = time.time() + duration
    dots = ["", ".", "..", "..."]
    i = 0

    while time.time() < end_time:
        sys.stdout.write(f"\r{text}{dots[i % 4]}")
        sys.stdout.flush()
        i += 1
        time.sleep(delay)

    sys.stdout.write("\r" + " "*(len(text)+4) + "\r")
    sys.stdout.flush()

def pulse_text(text="Waiting", duration=3, delay=0.5):
    """Упрощенная пульсирующая анимация"""
    end_time = time.time() + duration
    visible = True

    while time.time() < end_time:
        sys.stdout.write("\r" + (text if visible else " "*len(text)))
        sys.stdout.flush()
        visible = not visible
        time.sleep(delay)

    sys.stdout.write("\r" + " "*len(text) + "\r")
    sys.stdout.flush()

def glitch_effect(text, duration):
    """Глитч-эффект текста"""
    end = time.time() + duration
    while time.time() < end:
        glitch = ''.join(random.choice([c, '█', '▓', '▒', '░']) for c in text)
        print(f"\r{glitch}", end="", flush=True)
        time.sleep(0.1)
    print("\r" + " " * len(text) + "\r", end="")

def static_effect(duration):
    """Эффект помех (статик)"""
    end = time.time() + duration
    while time.time() < end:
        line = ''.join(random.choice(['.', ' ', '▄', '▀', '█']) for _ in range(50))
        print(f"\r{line}", end="", flush=True)
        time.sleep(0.05)
    print("\r" + " " * 50 + "\r", end="")

def progress_bar(total=100, length=30, delay=0.05, text="Progress"):
    """Простой прогресс-бар"""
    for i in range(total + 1):
        filled = int(length * (i / total))
        bar = "#" * filled + "-" * (length - filled)
        percent = int((i / total) * 100)

        sys.stdout.write(f"\r{text}: [{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(delay)

    sys.stdout.write("\n")
    sys.stdout.flush()