class ProfilingException(Exception):
    pass


class ConfigNotFound(ProfilingException):
    pass


class ConfigInvalid(ProfilingException):
    pass
