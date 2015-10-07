import __builtin__
import re

skip_re = re.compile("^\s*#.*$")

def open(filename):
    with __builtin__.open(filename) as f:
        return [l.rstrip() for l in f if not skip_re.match(l)]
