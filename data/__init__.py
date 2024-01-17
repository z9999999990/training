#!/usr/bin/env python3
# coding: utf-8


"""
Helper module for loading external data.
"""


import os
import inspect
import importlib


def preload_module_data(data_name):
    """
    Preload data from problem of calling module.
    """
    mod = importlib.import_module(data_name)
    if not hasattr(mod, "load"):
        raise AttributeError(f"module {mod} has no attribute 'load'")

    return mod.load()


class _DataLoader:
    """
    Helper class for loading external data.
    """

    def __init__(self):
        self.cache = None

    def reset(self):
        """
        Reset cache.
        """
        self.cache = None

    def preload(self, data_name):
        """
        Preload data from problem of specified module.
        """
        mod = importlib.import_module(data_name)
        if not hasattr(mod, "load"):
            raise AttributeError(f"module {mod} has no attribute 'load'")

        data = mod.load()
        self.cache = data
        return data

    def try_preload(self, data_name):
        """
        Preload data from problem of specified module.
        """
        try:
            return self.preload(data_name)

        except ImportError:
            return None

    def load(self):
        """
        Load data dynamically from problem of calling module or preloaded cache.
        """
        if self.cache is not None:
            return self.cache

        stack = inspect.stack()
        caller_frame_info = stack[2]
        caller_filename = os.path.basename(caller_frame_info.filename)
        caller_module_name = caller_filename[:-3]  # remove ".py"
        data_module = f"data.{caller_module_name}"
        return self.preload(data_module)


_data_loader = _DataLoader()


def load():
    """
    Lsoad data dynamically from problem of calling module or preloaded cache.
    """
    return _data_loader.load()


def preload(data_name):
    """
    Preload data from problem of specified module.
    """
    return _data_loader.preload(data_name)


def try_preload(data_name):
    """
    Preload data from problem of specified module.
    """
    return _data_loader.try_preload(data_name)


def reset():
    """
    Reset cache.
    """
    _data_loader.reset()
