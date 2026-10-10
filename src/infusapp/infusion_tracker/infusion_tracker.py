import sys
import threading
import time

from pynput import keyboard

# Clean Keyboard Inputs on Mac/Linux/Windows
try:
    import termios

    def _flush_stdin():
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

except ImportError:
    import msvcrt

    def _flush_stdin():
        while msvcrt.kbhit():
            msvcrt.getch()


class InfusionTracker:
    def __init__(self, drop_factor: int = 20, window: int = 5):
        self.drop_factor = drop_factor
        self.window = window  # Anzahl der letzten Intervalle für den Durchschnitt
        self._reset()

    def _reset(self) -> None:
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
                print(f"\r⏱  Elapsed: {elapsed:5.1f}s", end="", flush=True)
            time.sleep(0.1)

    def _recent_drops_per_min(self) -> float | None:
        if len(self.timestamps) < 2:
            return None
        recent = self.timestamps[-(self.window + 1):]  # window+1 Stempel = window Intervalle
        intervals = [recent[i] - recent[i - 1] for i in range(1, len(recent))]
        avg_interval = sum(intervals) / len(intervals)
        return 60 / avg_interval

    def on_press(self, key):
        if key == keyboard.Key.esc:
            self.running = False
            return False

        now = time.time()
        self.timestamps.append(now)

        if self.start_time is None:
            self.start_time = now
            print("\n⏱  Timer started. Tap again on the next drop.")
            return

        drops_per_min = self._recent_drops_per_min()
        if drops_per_min is None:
            return
        ml_per_hour = self.get_ml_per_hour(drops_per_min)

        print(
            f"\nDrop #{len(self.timestamps) - 1}  |  "
            f"{drops_per_min:.1f} drops/min  |  "
            f"{ml_per_hour:.1f} ml/h"
        )

    def run(self) -> None:
        clock_thread = threading.Thread(target=self.clock_display, daemon=True)
        clock_thread.start()
        print("\n---Infusion Speed Counter---")
        print("Press any key with each drop. Press ESC to stop.")
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
        self.running = False
        clock_thread.join(timeout=0.5)
        time.sleep(0.05)
        _flush_stdin()
        print("\n\n---Counting Complete---")

    def get_drops_per_min(self) -> float:
        # Endgültiger Wert: nur die letzten `window` Intervalle, nicht alles
        value = self._recent_drops_per_min()
        if value is None:
            raise ValueError("Zu wenige Messpunkte für eine Berechnung.")
        return value

    def get_ml_per_hour(self, drops_per_min: float) -> float:
        return (drops_per_min * 60) / self.drop_factor
