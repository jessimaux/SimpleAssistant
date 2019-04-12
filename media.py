#!/usr/bin/env python3
# -*- coding: utf-8-*-

import os
import speech_recognition as sr
from gtts import gTTS
from time import sleep
from pygame import mixer

class Media(object):
    def __init__(self):
        mixer.init()
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        self._speech_name = "/home/mzlo/Projects/project_sas/speech.mp3"
        with self._microphone as source:
            self._recognizer.adjust_for_ambient_noise(source)

    def listen(self):
        with self._microphone as source:
            audio = self._recognizer.listen(source, phrase_time_limit=5)
        return audio

    def recognize(self):
        try:
            print('[Sas] Понял, идет распознавание...')
            phrase = self._recognizer.recognize_google(self.listen(), language="ru-RU").lower()
            print(phrase)
            return phrase
        except sr.UnknownValueError:
            print("[GoogleSR] Не удалось распознать речь")
            return
        except sr.RequestError as e:
            print("[GoogleSR] Не удалось получить ответ с сервера; {0}".format(e))
            return

    def play(self, filename):
        mixer.music.stop()
        mixer.music.load(filename)
        mixer.music.play()

    def say(self, phrase):
        try:
            tts = gTTS(text=phrase, lang="ru")
            tts.save(self._speech_name)
        except Exception as e:
            print("[GoogleTTS] Не удалось синтезировать речь: {}".format(e))
            return

        # Play answer
        mixer.music.load(self._speech_name)
        mixer.music.play()

    def terminate(self):
        while mixer.music.get_busy():
            sleep(0.1)
        if os.path.exists(self._speech_name):
            os.remove(self._speech_name)