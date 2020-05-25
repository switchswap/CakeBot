class ConfigKeyNotFoundException(Exception):
    def __init__(self, message):
        self.error = message
        super(ConfigKeyNotFoundException, self).__init__(message)
