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
        
        # Получаем правильный путь (для .exe и для исходников)
        if getattr(sys, 'frozen', False):
            # Запущено из .exe (PyInstaller)
            base_path = sys._MEIPASS
        else:
            # Запущено из исходников
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        sounds_dir = os.path.join(base_path, 'sounds')
        
        # Настраиваем пути к звуковым файлам
        sound_files = {
            'number': 'number.wav',
            'operator': 'operator.wav',
            'equals': 'equals.wav',
            'control': 'control.wav',
            'error': 'error.wav',
            'exit': 'exit.wav',
        }
        
        # Загружаем звуки
        for sound_type, filename in sound_files.items():
            sound_path = os.path.join(sounds_dir, filename)
            self.sounds[sound_type].setSource(QUrl.fromLocalFile(sound_path))
            self.sounds[sound_type].setVolume(0.5)  # Громкость 50%
    
    @classmethod
    def get_instance(cls):
        """Получить единственный экземпляр SoundManager (Singleton)"""
        if cls._instance is None:
            cls._instance = SoundManager()
        return cls._instance
    
    def play(self, sound_type):
        """Воспроизвести звук по типу"""
        sound = self.sounds.get(sound_type)
        if sound:
            sound.stop()  # Остановить предыдущее воспроизведение
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