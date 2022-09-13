from PIL import Image
import os
from .models import OSS_LOCAL_DIR, Directory, Photo

def get_oss_directories():
    oss_dir_set = set()
    for first_path in os.listdir(OSS_LOCAL_DIR):
        if first_path.isnumeric():
            for dir_path in os.listdir(os.path.join(OSS_LOCAL_DIR, first_path)):
                oss_dir_set.add((first_path, dir_path))
    return(oss_dir_set)

