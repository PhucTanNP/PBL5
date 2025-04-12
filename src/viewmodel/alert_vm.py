# ViewModel: Alert System Logic
import sounddevice as sd
import numpy as np

class AlertViewModel:
    def play_alert(self):
        """Phát cảnh báo âm thanh khi nhận diện biển báo"""
        fs = 44100  # Tần số âm thanh
        seconds = 1  # Thời gian phát
        sound = np.sin(2 * np.pi * 440 * np.arange(fs * seconds) / fs)
        sd.play(sound)
        sd.wait()
