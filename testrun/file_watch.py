#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from pprint import pprint 

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("Got it!", event)
        if isinstance(event, (FileModifiedEvent, )):
            print(event.src_path) 
            print(event.event_type) 


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()