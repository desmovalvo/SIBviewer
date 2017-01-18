#!/usr/bin/python

# global requirements
from smart_m3.m3_kp_api import *

# the class Resource
class DataProperty:

    # initializer
    def __init__(self, dproperty, resource, value):

        """Initializes the DataProperty class"""

        self.resource = resource
        self.dproperty = str(dproperty)
        self.value = str(value)

        # initialize the object coordinates
        self.x = None
        self.y = None
        self.z = None

        # initialize the graphic item
        self.gitem_object = None
        self.gitem_objectlabel = None
        self.gitem_predicate = None
        self.gitem_predicatelabel = None


    # get value
    def get_value(self):

        """Returns the value of the data property"""

        return self.value


    # get coordinates
    def get_coordinates(self):

        """Returns the coordinates for the object node"""

        return self.x, self.y, self.z


    # set coordinates
    def set_coordinates(self, x, y, z):

        """Returns the coordinates for the object node"""

        self.x = x
        self.y = y
        self.z = z
