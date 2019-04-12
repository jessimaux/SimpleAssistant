#!/usr/bin/env python3
# -*- coding: utf-8-*-

import re
import wikipedia as wiki

WORDS = ['НАЙДИ', 'ЧТО', 'ЭТО']

speech_name = "/home/mzlo/Projects/project_sas/speech.mp3"
wiki.set_lang("ru")

def wiki_search(text):
    try:
        for word in WORDS:
            text = text.replace(word.lower(), '')
        search_result = wiki.page(text)
        result = re.sub('\([^)]*\)', '', search_result.summary).split('.')
        return result[0]
    except wiki.exceptions.DisambiguationError:
        print('Уточните свой запрос')
    except wiki.exceptions.PageError:
        print('[Wikipedia] Такой страницы не существует')
    except ValueError as e:
        print('[Wikipedia] Ошибка: {}'.format(e))

def handle(text, media):
    wiki_search_phrase = wiki_search(text)
    if wiki_search_phrase:
        print(wiki_search_phrase)
        media.say(wiki_search_phrase)

def isValid(text):
    return bool(re.search(r'найди|это|что', text, re.IGNORECASE))