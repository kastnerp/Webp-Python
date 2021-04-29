from pathlib import Path
import platform
from datetime import datetime
import os
from glob import iglob
import logging

LOG_FILENAME = 'png2web.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


# initializing suffix list
suff_list = ['png', 'jpg', 'jpeg', 'gif']

directory_in_str = Path.cwd()
dir_glob = str(directory_in_str) + '/**/*'

file_list = [f for f in iglob(str(dir_glob), recursive=True) if os.path.isfile(f) and f.endswith(tuple(suff_list))]

for f in file_list:

    file_path = Path(f)
    path_in_str_png = str(file_path)
    path_in_str_webp = str(file_path.parent) + '/' + file_path.stem + ".webp"

    try:
        mtime_png = creation_date(path_in_str_png)
        dt_png = datetime.fromtimestamp(mtime_png)
        # print(dt_png.year, dt_png.month, dt_png.day, dt_png.hour, dt_png.minute, dt_png.second)

        mtime_webp = creation_date(path_in_str_webp)
        dt_webp = datetime.fromtimestamp(mtime_png)

        if (mtime_png > mtime_webp):
            s1 = "Uploaded image newer then webp.", str(path_in_str_png)
            s2 = "Deleting.", str(path_in_str_webp)
            print(datetime.now())
            print(s1)
            print(s2)
            logging.debug(datetime.now())
            logging.debug(s1)
            logging.debug(s2)
            os.remove(path_in_str_webp)

    except:
        print(datetime.now())
        print("Webp doesn't exist.", str(path_in_str_png))
