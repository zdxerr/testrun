
import os
import json
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent

logger = logging.getLogger(__name__)

class Preferences(dict):
    def __init__(self, path='preferences.json', on_load=lambda self: None):
        super(Preferences, self).__init__()
        self.path = os.path.normcase(os.path.abspath(path))
        self.on_load = on_load
        self.reload()
        self.__observer = Observer()
        self.start()

    def start(self):
        logger.debug("Start observer for `%s`", self.path)
        self.__observer.schedule(Preferences.EventHandler(self), 
                                 path=os.path.dirname(self.path), 
                                 recursive=False)
        self.__observer.start()

    def stop(self):
        logger.debug("Stop observer for `%s`", self.path)
        self.__observer.stop()
        self.__observer.join()

    def reload(self):
        try:
            logger.debug("Read file `%s`", self.path)
            with open(self.path) as pointer:
                self.update(json.load(pointer))
            self.on_load(self)
        except IOError:
            logger.warn("Create file `%s`", self.path)
        except ValueError:
            logger.error("Error in file `%s`", self.path, exc_info=True)
            
    def flush(self):
        """Save change to file."""
        logger.debug("Write file `%s`", self.path)
        with open(self.path, 'w+') as pointer:
            pointer.write(json.dumps(self, indent=4, sort_keys=True))

    class EventHandler(FileSystemEventHandler):
        def __init__(self, preferences):
            super(Preferences.EventHandler, self).__init__()
            self.preferences = preferences

        def on_modified(self, event):
            logging.debug("Modification found in `%s`", event.src_path)
            if self.preferences.path == os.path.normcase(os.path.abspath(event.src_path)):
                self.preferences.reload()