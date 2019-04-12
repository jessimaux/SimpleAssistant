self._dict = {'Приветствие': ['доброе утро', 'привет', 'хай'],
              'Как дела': ['как дела', 'как настроение', 'как твое настроение'],
              'Поиск': ['найди ', 'найди мне ', 'найди в википедии ', 'что это такое ', 'что это', 'это',
                        'дай определение'],
              'Выключение': ['пока', 'прощай', 'выключись']}

def detect_command(self, phrase):
    for key, value in self._dict.items():
        for command_word in value:
            if phrase.find(command_word) != -1:
                if key == 'Приветствие':
                    self.say('Привет')
                    return
                elif key == 'Как дела':
                    self.say('Все хорошо')
                    return
                elif key == 'Поиск':
                    phrase = phrase.replace(command_word, '')
                    wiki_search_phrase = self.wiki_search(phrase)
                    if wiki_search_phrase:
                        print(wiki_search_phrase)
                        self.say(wiki_search_phrase)
                    return
                elif key == 'Выключение':
                    raise KeyboardInterrupt

    wiki_search_phrase = self.wiki_search(phrase)
    if wiki_search_phrase:
        print(wiki_search_phrase)
        self.say(wiki_search_phrase)




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





    def wiki_search(self, phrase):
        try:
            search_result = wiki.page(phrase)
            result = re.sub('\([^)]*\)', '', search_result.summary).split('.')
            return result[0]
        except wiki.exceptions.DisambiguationError:
            self.say('Уточните свой запрос')
            print('Уточните свой запрос')
        except wiki.exceptions.PageError:
            print('[Wikipedia] Такой страницы не существует')
        except ValueError as e:
            print('[Wikipedia] Ошибка: {}'.format(e))


    '''
    def google_search(self, phrase):
        try:
            search_results = google.search(phrase, pages=1)
            print(search_results[0].description)
        except Exception as e:
            print('[GoogleSearch] Что-то пошло не так: {}'.format(e))
    '''
