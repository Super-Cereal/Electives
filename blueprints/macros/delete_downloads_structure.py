import os

PRE_PATH = '/home/SuperCereal/status-false/'
PRE_PATH = ''


def delete_downloads_structure(path):
    path = PRE_PATH + path
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
