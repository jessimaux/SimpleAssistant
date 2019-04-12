#!/usr/bin/env python3
# -*- coding: utf-8-*-
import speech_recognition as sr
from pygame import mixer

class Media(object):
    def __init__(self):
        mixer.init()
        self._recognizer = sr.Recognizer()
        self._microphone = sr.Microphone()
        self._speech_name = "/home/mzlo/Projects/project_sas/speech.mp3"
        self._notification = {'power_on': mixer.Sound('assets/ding.wav'),
                              'callback': mixer.Sound('assets/notification.ogg'),
                              'power_off': mixer.Sound('assets/dong.wav')}
