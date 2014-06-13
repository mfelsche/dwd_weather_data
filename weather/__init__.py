import argparse
import os

__version__ = '0.0.0'


class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))


def is_dir(dirname):
    """
    Checks if a path is an actual directory.
    Tries to create the directory.
    """
    if not os.path.isdir(dirname):
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except Exception as e:
                raise argparse.ArgumentTypeError(
                    "could not create directory {0}".format(dirname))
        else:
            msg = "{0} exists but is not a directory".format(dirname)
            raise argparse.ArgumentTypeError(msg)
    else:
        return dirname
