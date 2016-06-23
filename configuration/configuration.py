from yaml import load
from os.path import isfile


class ConfigurationFileNotExists(Exception):
    def __init__(self, filename):
        message = 'Configuration file not found {0}'.format(filename)
        super(ConfigurationFileNotExists, self).__init__(message)


class ConfigurationKeyNotExists(Exception):
    def __init__(self, filename, key):
        message = 'Configuration key not found in {0} : {1}'.format(
            filename, key
        )
        super(ConfigurationKeyNotExists, self).__init__(message)


class Configurator(object):

    def __init__(self, filename='configuration.yaml'):
        self.filename = filename
        self._cache = {}

    def get(self, key):
        self._load()
        return self._get(key)

    def _load(self):

        if self.filename in self._cache:
            self.configuration = self._cache[self.filename]
        else:
            if not isfile(self.filename):
                raise ConfigurationFileNotExists(self.filename)

            self.reload()

    def _get(self, key):
        if not self.configuration or key not in self.configuration:
            raise ConfigurationKeyNotExists(self.filename, key)

        return self.configuration[key]

    def reload(self):
        with open(self.filename) as f:
            self.configuration = load(f.read())
