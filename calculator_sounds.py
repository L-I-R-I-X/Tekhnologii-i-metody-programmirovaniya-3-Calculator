import sys
import os
from PyQt5.QtMultimedia import QSoundEffect
from PyQt5.QtCore import QUrl


class SoundManager:
    _instance = None
    
    def __init__(self):
        self.sounds = {
            'number': QSoundEffect(),
            'operator': QSoundEffect(),
            'equals': QSoundEffect(),
            'control': QSoundEffect(),
            'error': QSoundEffect(),
            'exit': QSoundEffect(),
        }
        
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        sounds_dir = os.path.join(base_path, 'sounds')
        
        sound_files = {
            'number': 'number.wav',
            'operator': 'operator.wav',
            'equals': 'equals.wav',
            'control': 'control.wav',
            'error': 'error.wav',
            'exit': 'exit.wav',
        }
        
        for sound_type, filename in sound_files.items():
            sound_path = os.path.join(sounds_dir, filename)
            self.sounds[sound_type].setSource(QUrl.fromLocalFile(sound_path))
            self.sounds[sound_type].setVolume(0.5)
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SoundManager()
        return cls._instance
    
    def play(self, sound_type):
        sound = self.sounds.get(sound_type)
        if sound:
            sound.stop()
            sound.play()
    
    def play_number(self):
        self.play('number')
    
    def play_operator(self):
        self.play('operator')
    
    def play_equals(self):
        self.play('equals')
    
    def play_control(self):
        self.play('control')
    
    def play_error(self):
        self.play('error')