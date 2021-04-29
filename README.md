# Webp-Python

`webp_watchdog.py` will watch for file changes in the directory in which it is executed. If it observes changes to any file with the ending `["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif"]`, it will create a *.webp version of that file in the same folder.

## How to use this

- Copy `python webp_watchdog.py` to your desired directory

- Create service (e.g. with supervisord) that runs `python webp_watchdog.py` in the directory that shall be observed
