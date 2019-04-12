#!/usr/bin/env python3
# -*- coding: utf-8-*-

# TODO:
# !-Дебаг-!:
# переписать принты на логгер
# Модули:
# приветствие, как дела, чем занимаешься - добавить (С)
# вк апи (чек сообщений, музыка), (A)
# почта апи (чек почты),
# калькулятор, (B)
# опенсв(приветствие по фото, база)
# Функционал: ргб лента под действия и музыку - при переносе на распбери

import pkgutil
import snowboydecoder
import media

class SimpleAssisstant:
    def __init__(self):
        self.modules = self.get_modules()
        self._media = media.Media()
        self._notification = {'power_on': 'assets/ding.wav',
                              'callback': 'assets/notification.ogg',
                              'power_off': 'assets/dong.wav'}
        self._model = 'models/Sas.pmdl'
        self._sensitivity = 0.43
        self._detector = snowboydecoder.HotwordDetector(self._model, sensitivity=self._sensitivity)

    def detectedCallback(self):
        self._media.play(self._notification['callback'])
        print('[Sas] Я вас слушаю...')
        phrase = self._media.recognize()
        if phrase:
            self.query(phrase.split())

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
                        module.handle(' '.join(texts), self._media)
                    except Exception:
                        print('[Sas_module] Failed to execute module')
                    else:
                        print("[Sas_module] Handling of phrase '%s' by module '%s' completed" % (text, module.__name__))
                    finally:
                        return
        print("[Sas_module] No module was able to handle any of these phrases: %r" % texts)

    def start(self):
        self._media.play(self._notification['power_on'])
        self._detector.start(detected_callback=self.detectedCallback,
                             sleep_time=0.03)

    def clean_up(self):
        print('[Sas] Выключение')
        self._media.play(self._notification['power_off'])
        self._media.terminate()
        self._detector.terminate()

if __name__ == "__main__":
    app = SimpleAssisstant()
    try:
        app.start()
    except KeyboardInterrupt:
        app.clean_up()