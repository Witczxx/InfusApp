import threading
import time

from pynput import keyboard

class DripRateTapper:
    def __init__(self, drop_factor=20, window=5):
        self.drop_factor = drop_factor
        self.window = window
        self.timestamps = []
        self.start_time = None
        self.running = True

    def menu(self):
        self.run()
        drops_per_min = self..get_drops_per_min()
        ml_per_hour = self.get_ml_per_hour(drops_per_min=drops_per_min)
        print("\n---Results---")
        print(f"Drops per Min: {round(drops_per_min, 2)} drops/min")
        print(f"mL per Hour: {round(ml_per_hour, 2)} mL/h")
        return drops_per_min, ml_per_hour


    def clock_display(self):
        while self.running:
            if self.start_time is not None:
                elapsed = time.time() - self.start_time
                print(f"\r⏱  Elapsed: {elapsed:5.1f}s", end="", flush=True)
            time.sleep(0.1)

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

        intervals = [
            self.timestamps[i] - self.timestamps[i - 1]
            for i in range(
                max(1, len(self.timestamps) - self.window), len(self.timestamps)
            )
        ]
        avg_interval = sum(intervals) / len(intervals)
        drops_per_min = 60 / avg_interval
        ml_per_hour = (drops_per_min * 60) / self.drop_factor

        print(
            f"\nDrop #{len(self.timestamps) - 1}  |  "
            f"{drops_per_min:.1f} drops/min  |  "
            f"{ml_per_hour:.1f} ml/h"
        )

    def run(self):
        clock_thread = threading.Thread(target=self.clock_display, daemon=True)
        clock_thread.start()
        print("\n---Infusion Speed Counter---")
        print(
            f"Press any key with each drop. Press ESC to stop."
        )
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()
        print("\n\n---Counting Complete---")

    def get_drops_per_min(self):
        #if len(self.timestamps) < 2:
            #return None
        total_time = self.timestamps[-1] - self.timestamps[0]
        total_intervals = len(self.timestamps) - 1
        avg_interval = total_time / total_intervals
        drops_per_min = 60 / avg_interval
        return drops_per_min

    def get_ml_per_hour(self, drops_per_min):
        ml_per_hour = (drops_per_min * 60) / self.drop_factor
        return ml_per_hour

