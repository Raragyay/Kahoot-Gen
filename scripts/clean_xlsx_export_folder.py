import shutil
import time

from constants import base_folder_path

if __name__ == '__main__':
    export_dir = base_folder_path.joinpath("xlsx_export")
    right_now = time.time()
    one_day = 60 * 60 * 24  # time.time and stats.st_mtime measure in seconds
    for folder in export_dir.iterdir():
        stats = folder.stat()
        # use modified instead of created time to avoid ambiguity with unix systems
        last_modified = stats.st_mtime
        if right_now - last_modified > one_day:  # If more than one day has passed since creation
            shutil.rmtree(folder)
    print("all folders older than 1 day have been deleted")
