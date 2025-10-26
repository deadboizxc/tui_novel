import sys
import time
import itertools

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
