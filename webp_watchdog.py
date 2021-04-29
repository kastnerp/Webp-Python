import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import webp
from pathlib import Path
from datetime import datetime
import os
from PIL import Image
import logging
import os, errno


def silentremove(filename):
    try:
        os.remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred


if __name__ == "__main__":
    patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif"]
    ignore_patterns = ["*-1.jpg"]
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)


    def get_save_path(event):
        return Path.cwd() / Path(event.src_path).parent / Path(str(Path(event.src_path).stem) + ".webp")


    # def on_created(event):
    #     print(f"{event.src_path} created.")
    #     logging.debug(f"{event.src_path} created.")
    #     # Save an image
    #     save_path = get_save_path(event)
    #     print("Save Path:", save_path)
    #
    #     write_webp(event.src_path, save_path)

    def on_deleted(event):
        print("Received deleted event - %s." % event.src_path)
        logging.debug("Received deleted event - %s." % event.src_path)
        save_path = get_save_path(event)
        try:
            os.remove(save_path)
        except:
            print("File did not exist", save_path)


    def on_modified(event):

        print("Received modified event - %s." % event.src_path)
        logging.debug("Received modified event - %s." % event.src_path)
        save_path = get_save_path(event)
        print("Save Path:", save_path)

        write_webp(event.src_path, save_path)


    def load_image(path):
        return Image.open(path)


    def write_webp(file_path, save_path):
        logging.debug(datetime.now())
        logging.debug("Save Path: " + str(save_path))
        try:
            webp.save_image(load_image(file_path), save_path, quality=80)
        except:
            print("Could not convert", save_path)
            logging.error(datetime.now())
            logging.error("Could not convert " + str(save_path))


    # my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    # my_event_handler.on_moved = on_moved

    path = "."
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    LOG_FILENAME = 'webp_watchdog.log'
    silentremove(LOG_FILENAME)
    logging.basicConfig(filename=LOG_FILENAME, level=logging.ERROR)

    logging.debug(datetime.now())
    logging.debug("Observing directory...")
    print("Observing directory...")
    my_observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()

        # init_size = -1
        # while True:
        #    current_size = os.path.getsize(event.src_path)
        #    if current_size == init_size:
        #        break
        #    else:
        #        init_size = os.path.getsize(event.src_path)
        #        time.sleep(2)
        # print("file copy has now finished")
