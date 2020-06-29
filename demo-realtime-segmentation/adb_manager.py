import os


class ADBSender():
    def __init__(self, file_path='adb_file.txt', target_path='/sdcard/Download/my_log_file.txt'):
        self.file_path = file_path
        self.target_path = target_path

    def send(self, contents=""):
        with open(self.file_path, mode='a', encoding='utf-8-sig') as f:
            f.write(contents + '\n')
        f.close()

        os.system("adb push " + self.file_path + " " + self.target_path)
