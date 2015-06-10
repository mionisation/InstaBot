import yaml

class State:
    def __init__(self, path):
        self._path = path
        try:
            f = open(path, 'rb')
        except IOError:
            self._data = {}
            return
        self._data = yaml.load(f)
        f.close()

    def __delitem__(self, key, value):
        del self._data[key]
        self._save()

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self._save()

    def _save(self):
        f = open(self._path, 'wb')
        yaml.dump(self._data, f)
        f.close()

    def increment(self, key, default_value=1):
        try:
            value = self._data[key]
        except KeyError:
            value = default_value
        else:
            value += 1
        self[key] = value
        return value

    def get(self, key, default_value=None):
        try:
            value = self._data[key]
        except KeyError:
            value = default_value
            self[key] = value
        return value
