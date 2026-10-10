import statistics
import sys
import threading
import time
from contextlib import contextmanager

from pynput import keyboard

# Clean Keyboard Inputs on Mac/Linux/Windows
try:
    import termios
except ImportError:  # Windows
    termios = None

if termios is not None:

    def _flush_stdin() -> None:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

else:
    import msvcrt

    def _flush_stdin() -> None:
        while msvcrt.kbhit():
            msvcrt.getch()


def flushed_input(prompt: str = "") -> str:
    """Wie input(), leert vorher aber übrig gebliebene Tastendrücke."""
    _flush_stdin()
    return input(prompt)


@contextmanager
def _no_echo():
    """Schaltet das Tasten-Echo im Terminal aus (Mac/Linux), damit kein ^[ o. ä. erscheint."""
    if termios is None or not sys.stdin.isatty():
        yield
        return

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSADRAIN, new)
    try:
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


class InfusionTracker:
    def __init__(self, drop_factor: int = 20, window: int = 5, use_median: bool = True):
        self.drop_factor = drop_factor
        self.window = window  # Anzahl der letzten Intervalle für die Berechnung
        self.use_median = use_median  # Median ist robuster gegen einzelne Ausreißer
        self._print_lock = threading.Lock()
        self._reset()

    def _reset(self) -> None:
        """Setzt alle Messwerte für eine neue Aufzeichnung zurück."""
        self.timestamps: list[float] = []
        self.start_time: float | None = None
        self.running = True

    def menu(self):
        self._reset()  # jede neue Aufzeichnung startet bei null
        self.run()
        if len(self.timestamps) <= 2:
            return None
        drops_per_min = round(self.get_drops_per_min(), 2)
        ml_per_hour = round(self.get_ml_per_hour(drops_per_min=drops_per_min), 2)
        print("\n---Results---")
        print(f"Drops per Min: {drops_per_min} drops/min")
        print(f"mL per Hour: {ml_per_hour} mL/h")
        return drops_per_min, ml_per_hour

    def clock_display(self) -> None:
        while self.running:
            if self.start_time is not None:
                elapsed = time.time() - self.start_time
                with self._print_lock:
                    print(f"\r\033[K⏱  Elapsed: {elapsed:5.1f}s", end="", flush=True)
            time.sleep(0.1)

    def _recent_drops_per_min(self) -> float | None:
        """Tropfen/min aus den letzten `window` Intervallen."""
        if len(self.timestamps) < 2:
            return None
        recent = self.timestamps[-(self.window + 1):]  # window+1 Stempel = window Intervalle
        intervals = [recent[i] - recent[i - 1] for i in range(1, len(recent))]
        if self.use_median:
            typical_interval = statistics.median(intervals)
        else:
            typical_interval = sum(intervals) / len(intervals)
        if typical_interval <= 0:
            return None
        return 60 / typical_interval

    def on_press(self, key):
        if key == keyboard.Key.esc:
            self.running = False
            return False

        now = time.time()
        self.timestamps.append(now)

        if self.start_time is None:
            self.start_time = now
            with self._print_lock:
                print("\r\033[K⏱  Timer started. Tap again on the next drop.")
            return

        drops_per_min = self._recent_drops_per_min()
        if drops_per_min is None:
            return
        ml_per_hour = self.get_ml_per_hour(drops_per_min)

        with self._print_lock:
            print(
                f"\r\033[KDrop #{len(self.timestamps) - 1}  |  "
                f"{drops_per_min:.1f} drops/min  |  "
                f"{ml_per_hour:.1f} ml/h"
            )

    def run(self) -> None:
        print("\n---Infusion Speed Counter---")
        print("Press any key with each drop. Press ESC to stop.")

        clock_thread = threading.Thread(target=self.clock_display, daemon=True)
        clock_thread.start()

        with _no_echo():
            with keyboard.Listener(on_press=self.on_press) as listener:
                listener.join()
            self.running = False
            clock_thread.join(timeout=0.5)
            time.sleep(0.2)   # Terminal liefert die letzten Zeichen verzögert
            _flush_stdin()    # jetzt alle übrigen Tasten verwerfen

        with self._print_lock:
            print("\r\033[K", end="")  # Statuszeile löschen
        print("\n---Counting Complete---")

    def get_drops_per_min(self) -> float:
        # Endgültiger Wert: nur die letzten `window` Intervalle, nicht alles
        value = self._recent_drops_per_min()
        if value is None:
            raise ValueError("Zu wenige Messpunkte für eine Berechnung.")
        return value

    def get_ml_per_hour(self, drops_per_min: float) -> float:
        return (drops_per_min * 60) / self.drop_factor


if __name__ == "__main__":
    tracker = InfusionTracker(drop_factor=20, window=5)
    while True:
        tracker.menu()
        again = flushed_input("\nNoch eine Infusion messen? (j/n): ").strip().lower()
        if again != "j":
            break
