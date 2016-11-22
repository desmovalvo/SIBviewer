#!/usr/bin/python

# global requirements
from smart_m3.m3_kp_api import *

# the class Resource
class Resource:

    # initializer
    def __init__(self, resource, ns_list=None):

        """Initializes the Resource class"""
        
        # store the resource name
        self.name = str(resource)

        # split in prefix and qname
        try:
            self.prefix, self.qname = self.resource.split("#")
            if ns_list:
                if ns_list.has_key(self.prefix):
                    self.ns = ns_list[self.prefix]
        except:
            self.prefix = None
            self.qname = None
            self.ns = None

        # initialize properties
        self.data_properties = []
        self.object_properties = []
        
        # define coordinates
        self.x = None
        self.y = None


    # set coords
    def set_coordinates(self, x, y):

        """Stores the coordinates of the resource"""
        
        self.x = int(x)
        self.y = int(y)

        
    # get coords
    def get_coordinates(self):

        """Returns the coordinates"""
        
        return self.x, self.y


    # add data property
    def add_data_property(self, dproperty):

        """Adds a new data property to the list"""

        self.data_properties.append(dproperty)


    # add object property
    def add_object_property(self, oproperty):

        """Adds a new object property to the list"""

        self.object_properties.append(oproperty)
        
