"""
Timer Module for Hangman Game
Author: CDU Software Engineering Student

Handles the 15-second countdown timer for each guess.
Had to figure out threading to make this work properly.
"""

import time
import threading


class GameTimer:
    """Timer for the hangman guessing rounds."""
    def __init__(self, timeout_function=None):
        """
        Set up the timer.
        timeout_function gets called when time runs out.
        """
        self.timeout_callback = timeout_function
        self.timer_thread = None
        self.start_time = 0.0
        self.duration = 0
        self.active = False
        # Need this lock to prevent threading issues
        self.lock = threading.Lock()
    def start_timer(self, seconds=15):
        """Start countdown for given number of seconds."""
        if seconds <= 0:
            return
        with self.lock:
            self._stop_current_timer()
            self.duration = seconds
            self.start_time = time.time()
            self.active = True
            # Start the actual timer thread
            self.timer_thread = threading.Timer(seconds, self._time_up)
            self.timer_thread.start()
    def stop_timer(self):
        """Stop the current timer."""
        with self.lock:
            self._stop_current_timer()
    def _stop_current_timer(self):
        """Internal method to clean up timer."""
        self.active = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.cancel()
        self.timer_thread = None
        self.start_time = 0.0
        self.duration = 0
    def _time_up(self):
        """Called when timer expires."""
        with self.lock:
            self.active = False
            if self.timeout_callback:
                # Run callback in separate thread to avoid blocking
                callback_thread = threading.Thread(target=self.timeout_callback)
                callback_thread.daemon = True
                callback_thread.start()
    def get_time_left(self):
        """Get seconds remaining (updates in real time)."""
        with self.lock:
            if not self.active or self.start_time == 0:
                return 0
            elapsed = time.time() - self.start_time
            remaining = max(0, self.duration - elapsed)
            return int(remaining)
    def is_running(self):
        """Check if timer is currently active."""
        with self.lock:
            return self.active
    def get_progress_percent(self):
        """Get how much of the timer has elapsed (0-100%)."""
        with self.lock:
            if not self.active or self.duration == 0:
                return 100.0
            elapsed = time.time() - self.start_time if self.start_time > 0 else 0
            progress = (elapsed / self.duration) * 100.0
            return min(100.0, max(0.0, progress))
