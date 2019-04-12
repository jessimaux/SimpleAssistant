#!/usr/bin/env python3
# -*- coding: utf-8-*-

import re
import wikipedia as wiki
from gtts import gTTS
from pygame import mixer

WORDS = ['НАЙДИ', 'ЧТО', 'ЭТО']

speech_name = "/home/mzlo/Projects/project_sas/speech.mp3"
mixer.init()
wiki.set_lang("ru")

def say(phrase):
    try:
        tts = gTTS(text=phrase, lang="ru")
        tts.save(speech_name)
    except Exception as e:
        print("[GoogleTTS] Не удалось синтезировать речь: {}".format(e))
        return

    # Play answer
    mixer.music.load(speech_name)
    mixer.music.play()

def wiki_search(text):
    try:
        for word in WORDS:
            text = text.replace(word.lower(), '')
        search_result = wiki.page(text)
        result = re.sub('\([^)]*\)', '', search_result.summary).split('.')
        return result[0]
    except wiki.exceptions.DisambiguationError:
        say('Уточните свой запрос')
        print('Уточните свой запрос')
    except wiki.exceptions.PageError:
        print('[Wikipedia] Такой страницы не существует')
    except ValueError as e:
        print('[Wikipedia] Ошибка: {}'.format(e))

def handle(text):
    wiki_search_phrase = wiki_search(text)
    if wiki_search_phrase:
        print(wiki_search_phrase)
        say(wiki_search_phrase)

def isValid(text):
    return bool(re.search(r'найди|это|что', text, re.IGNORECASE))