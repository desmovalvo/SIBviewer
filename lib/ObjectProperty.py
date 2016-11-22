#!/usr/bin/python

# global requirements
from smart_m3.m3_kp_api import *

# local requirements
from constants import *


# the class Resource
class ObjectProperty:

    # initializer
    def __init__(self, oproperty, value_resource):

        """Initializes the ObjectProperty class"""

        self.oproperty = str(oproperty)
        self.value = value_resource
        if self.oproperty == str(rdf + "type"):
            self.color = red
        else:
            self.color = blue


    # getter
    def get_value(self):

        """Returns the value of the data property"""

        return self.value
