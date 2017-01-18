#!/usr/bin/python

# global requirements
from smart_m3.m3_kp_api import *

# the class Resource
class Resource:

    # initializer
    def __init__(self, resource, isClass, ns_list=None):

        """Initializes the Resource class"""
        
        # store the resource name
        self.name = str(resource)        
        self.isClass = isClass

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
        self.isStatement = False

        # initialize the graphic element
        self.gitem = None
        
        # define coordinates
        self.x = None
        self.y = None
        self.z = None

        # initialize label and comment
        self.label = None
        self.comment = None
        

    # set coords
    def set_coordinates(self, x, y, z):

        """Stores the coordinates of the resource"""
        
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

        
    # get coords
    def get_coordinates(self):

        """Returns the coordinates"""
        
        return self.x, self.y, self.z


    # add data property
    def add_data_property(self, dproperty):

        """Adds a new data property to the list"""

        self.data_properties.append(dproperty)


    # add object property
    def add_object_property(self, oproperty):

        """Adds a new object property to the list"""

        self.object_properties.append(oproperty)
        

    # info_dp
    def get_info_dp(self):

        """Returns a string containing the list
        of the datatype properties"""

        # init output string
        out_string = ""

        # cycle over the datatype properties
        for dp in self.data_properties:
            out_string += "%s -> %s" % (dp.dproperty, dp.value)
        
        # return 
        return out_string


    # info_op
    def get_info_op(self):

        """Returns a string containing the list
        of the datatype properties"""

        # init output string
        out_string = ""

        # cycle over the datatype properties
        for op in self.object_properties:
            out_string += "%s, %s, %s" % (op.s, op.oproperty, op.o)
        
        # return 
        return out_string


    # info
    def get_info(self):

        """This method is used to retrieve a string
        that will be put in the left panel to describe
        the resource"""

        info = """Resource: %s

Datatype properties: 
%s

Object properties: 
%s

""" % (self.name, self.get_info_dp(), self.get_info_op())

        # return
        return info
