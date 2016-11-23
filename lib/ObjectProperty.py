#!/usr/bin/python

# global requirements
from smart_m3.m3_kp_api import *

# local requirements
from constants import *


# the class Resource
class ObjectProperty:

    # initializer
    def __init__(self, oproperty, op_subject, op_object):

        """Initializes the ObjectProperty class"""

        self.oproperty = str(oproperty)
        self.s = op_subject
        self.o = op_object
        if self.oproperty == str(rdf + "type"):
            self.color = red
        else:
            self.color = blue
