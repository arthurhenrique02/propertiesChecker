import os
import time


# create a func to wait for download
def wait_download_or_move(base_path, file_name, timeout=60):
    # get start time
    start_time = time.time()

    # loop until timeout
    while time.time() - start_time < timeout:
        # get files in download folder
        files = os.listdir(base_path)
        if any(file_name in file for file in files):
            return True
        time.sleep(1)

    return False
