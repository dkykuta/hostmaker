from os import listdir
from os.path import isfile, join

class FileManager:
    __shared_state = {}
    def __init__(self):
        self.__dict__ = self.__shared_state
        if 'data_dir' not in self.__shared_state:
            self.data_dir = None
        if 'actives_file' not in self.__shared_state:
            self.actives_file = None
        if 'etchosts_file' not in self.__shared_state:
            self.etchosts_file = '/etc/hosts2'

    def set_data_dir(self, data_dir):
        self.data_dir = data_dir

    def set_actives_file(self, actives_file):
        self.actives_file = actives_file

    def save_file(self, filename, content):
        if self.data_dir:
            fpath = join(self.data_dir, filename)
            with open(fpath, "wb") as f:
                f.write(bytes(content, 'UTF-8'))

    def load_content(self, filename):
        if self.data_dir:
            fpath = join(self.data_dir, filename)
            with open(fpath, "r") as f:
                return f.read()

    def list_files(self):
        print(self.data_dir)
        return [f for f in listdir(self.data_dir) if isfile(join(self.data_dir, f))]

    def get_actives(self):
        if self.actives_file:
            with open(self.actives_file, 'r') as f:
                return [s.strip() for s in f.readlines()]

    def set_actives(self, actives_content):
        if self.actives_file:
            with open(self.actives_file, 'wb') as f:
                f.write(bytes(actives_content, 'UTF-8'))

    def save_etc_hosts(self, content):
        print("saving etchosts")
        if not content.endswith('\n'):
            content = "%s\n" % content
        with open(self.etchosts_file, 'wb') as f:
            f.write(bytes(content, 'UTF-8'))
