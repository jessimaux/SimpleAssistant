#!/usr/bin/env python3
# -*- coding: utf-8-*-

# TODO:
# !-Дебаг-!:
# переписать принты на логгер
# Модули:
# wikipedia
# приветствие, как дела, чем занимаешься - добавить (С)
# google
# вк апи (чек сообщений, музыка), (A)
# почта апи (чек почты),
# калькулятор, (B)
# опенсв(приветствие по фото, база)
# Функционал: ргб лента под действия и музыку - при переносе на распбери

import speech_recognition as sr
import os
import pkgutil
import snowboydecoder
from time import sleep
from pygame import mixer

class SimpleAssisstant:
    def __init__(self):
        self.modules = self.get_modules()
        mixer.init()
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        self._speech_name = "/home/mzlo/Projects/project_sas/speech.mp3"
        self._notification = {'power_on': mixer.Sound('assets/ding.wav'), 'callback': mixer.Sound('assets/notification.ogg'), 'power_off': mixer.Sound('assets/dong.wav')}
        self._model = 'models/Sas.pmdl'
        self._sensitivity = 0.43
        self._detector = snowboydecoder.HotwordDetector(self._model, sensitivity=self._sensitivity)

    def detectedCallback(self):
        mixer.music.stop()
        self._notification['callback'].play()
        print('[Sas] Я вас слушаю...')
        with self._microphone as source:
            audio = self._recognizer.listen(source, phrase_time_limit=5)
        try:
            print('[Sas] Понял, идет распознавание...')
            phrase = self._recognizer.recognize_google(audio, language="ru-RU").lower()
            print(phrase)
        except sr.UnknownValueError:
            print("[GoogleSR] Не удалось распознать речь")
            return
        except sr.RequestError as e:
            print("[GoogleSR] Не удалось получить ответ с сервера; {0}".format(e))
            return

        self.query(phrase.split())

    def detectedStopCallback(self):
        mixer.music.stop()
        print('[Sas] Отмена последнего действия')

    def get_modules(self):
        locations = ['/home/mzlo/Projects/project_sas/modules']
        modules = []
        for finder, name, ispkg in pkgutil.walk_packages(locations):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except Exception:
                print("[PkgUtil] Skipped module '%s' due to an error." % name)
            else:
                if hasattr(mod, 'WORDS'):
                    print("[PkgUtil] Found module '%s' with words: %r" % (name, mod.WORDS))
                    modules.append(mod)
                else:
                    print("[PkgUtil] Skipped module '%s' because it misses the WORDS constant." % name)
        modules.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY')
                     else 0, reverse=True)
        return modules

    def query(self, texts):
        for module in self.modules:
            for text in texts:
                if module.isValid(text):
                    print("[Sas_module] '%s' is a valid phrase for module '%s'" % (text, module.__name__))
                    try:
                        module.handle(' '.join(texts))
                    except Exception:
                        print('[Sas_module] Failed to execute module')
                    else:
                        print("[Sas_module] Handling of phrase '%s' by module '%s' completed" % (text, module.__name__))
                    finally:
                        return
        print("[Sas_module] No module was able to handle any of these phrases: %r" % texts)

    def start(self):
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)
        self._notification['power_on'].play()
        print(self._recognizer.energy_threshold)
        self._detector.start(detected_callback=self.detectedCallback,
                             sleep_time=0.03)

    def clean_up(self):
        print('[Sas] Выключение')
        self._notification['power_off'].play()
        while mixer.music.get_busy():
            sleep(0.1)
        self._detector.terminate()
        if os.path.exists(self._speech_name):
            os.remove(self._speech_name)

def main():
    app = SimpleAssisstant()
    try:
        app.start()
    except KeyboardInterrupt:
        app.clean_up()

main()