# -*- coding: utf-8 -*-
from json import load


def load_snap_from_json(self, filename):
    """
       Loads DICT with all extracted attributes from json saved file (server or client side).
    """
    with open(filename) as infile:
        SNAPDATA = load(infile)
    return SNAPDATA
