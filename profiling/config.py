"""Config parser."""
import json

import errors

class ConfigEntry(object):
    def __init__(self):
        self.name = None
        self.call = None
        self.args = []
        self.kwargs = {}
        self.rounds = 1
        self.exception = None


def parse_config(filename):
    try:
        f = open(filename)
        config = f.read()
        f.close()
    except IOError:
        raise errors.ConfigNotFound()

    try:
        config = json.loads(config)
    except ValueError:
        raise errors.ConfigInvalid('Invalid JSON')

    if not isinstance(config, list):
        raise errors.ConfigInvalid('Config not a list')

    entries = []
    for entry in config:
        entries.append(parse_entry(entry))

    return entries


def parse_entry(entry):
    if not isinstance(entry, dict):
        raise errors.ConfigInvalid('Config entry not a dict')

    config_entry = ConfigEntry()

    try:
        if 'class' in entry:
            # If class, get class call, init instance, get method call.
            cls = entry['class']
            cls_modules = cls.split('.')
            cls_module = import_module(cls_modules[:-1])
            cls_call = getattr(cls_module, cls_modules[-1])

            if 'init_args' not in entry:
                raise errors.ConfigInvalid('init_args missing for %s' % (
                                               cls))
            init_args_func = entry['init_args']
            init_args_modules = init_args_func.split('.')
            init_args_module = import_module(init_args_modules[:-1])
            init_args = getattr(init_args_module, init_args_modules[-1])()
            if not isinstance(init_args, tuple):
                raise errors.ConfigInvalid('%s not returning a tuple' % (
                                           init_args_func))
            instance = cls_call(*init_args)

            if 'method' not in entry:
                raise errors.ConfigInvalid('method missing for %s' % (cls))
            method = entry['method']
            config_entry.call = getattr(instance, method)
            config_entry.name = '%s.%s' % (cls, method)

        elif 'func' in entry:
            # If func, get func call.
            func = entry['func']
            config_entry.name = func

            func_modules = func.split('.')
            func_module = import_module(func_modules[:-1])
            config_entry.call = getattr(func_module, func_modules[-1])

        else:
            raise errors.ConfigInvalid('class/func missing')

        if 'args' in entry:
            args_func = entry['args']
            args_modules = args_func.split('.')
            args_module = import_module(args_modules[:-1])
            args = getattr(args_module, args_modules[-1])()
            if not isinstance(args, tuple):
                raise errors.ConfigInvalid('%s not returning a tuple' % (
                                           args_func))
            config_entry.args = args

        if 'kwargs' in entry:
            kwargs_func = entry['kwargs']
            kwargs_modules = kwargs_func.split('.')
            kwargs_module = import_module(kwargs_modules[:-1])
            kwargs = getattr(kwargs_module, kwargs_modules[-1])()
            if not isinstance(kwargs, dict):
                raise errors.ConfigInvalid('%s not returning a dict' % (
                                           kwargs_func))
            config_entry.kwargs = kwargs

        if 'rounds' in entry:
            config_entry.rounds = entry['rounds']
    except Exception as e:
        raise errors.ConfigInvalid(str(e))

    return config_entry


def import_module(modules):
    m = __import__('.'.join(modules))
    for module in modules[1:]:
        m = getattr(m, module)
    return m
