#!/usr/bin/python

# global requirements
from smart_m3.m3_kp_api import *

# the class Resource
class DataProperty:

    # initializer
    def __init__(self, dproperty, value):

        """Initializes the DataProperty class"""

        self.dproperty = str(dproperty)
        self.value = str(value)

        # initialize the object coordinates
        self.x = None
        self.y = None


    # get value
    def get_value(self):

        """Returns the value of the data property"""

        return self.value


    # get coordinates
    def get_coordinates(self):

        """Returns the coordinates for the object node"""

        return self.x, self.y
