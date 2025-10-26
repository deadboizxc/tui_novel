# engine/animations.py
import sys
import time
import itertools
import threading


def spinner_animation(text="Loading", delay=0.1, duration=3):
    stop_flag = {"stop": False}

    def spin():
        for c in itertools.cycle("/-\\|"):
            if stop_flag["stop"]:
                break
            sys.stdout.write(f"\r{text} {c}")
            sys.stdout.flush()
            time.sleep(delay)
        sys.stdout.write("\r" + " " * (len(text) + 2) + "\r")
        sys.stdout.flush()

    t = threading.Thread(target=spin)
    t.start()
    time.sleep(duration)
    stop_flag["stop"] = True
    t.join()
    sys.stdout.write(f"\r{text} ✔️\n")
    sys.stdout.flush()


def dots_animation(text="Loading", delay=0.4, duration=3):
    stop_flag = {"stop": False}

    def animate():
        dots = ["", ".", "..", "..."]
        i = 0
        while not stop_flag["stop"]:
            sys.stdout.write(f"\r{text}{dots[i % len(dots)]} ")
            sys.stdout.flush()
            i += 1
            time.sleep(delay)
        sys.stdout.write("\r" + " " * (len(text) + 4) + "\r")
        sys.stdout.flush()

    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    stop_flag["stop"] = True
    t.join()
    sys.stdout.write(f"\r{text} ✔️\n")
    sys.stdout.flush()


def progress_bar(text="Progress", duration=3):
    length = 30
    sys.stdout.write(text + "\n[")
    sys.stdout.flush()
    steps = int(duration / 0.1)
    for i in range(steps):
        progress = int((i / steps) * length)
        bar = "=" * progress + " " * (length - progress)
        percent = int((i / steps) * 100)
        sys.stdout.write(f"\r{text}\n[{bar}] {percent}%")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write(f"\r{text}\n[{'=' * length}] 100%\n")
    sys.stdout.flush()
