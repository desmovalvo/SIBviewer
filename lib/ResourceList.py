#!/usr/bin/python

class ResourceList:

    # initializer
    def __init__(self):

        """Initializer of the ResourceList class"""

        # create an empty dictionary
        self.list = {}


    # add resource
    def add_resource(self, resource):

        """Method to add a resource to the list"""
        
        self.list[resource.name] = resource
        
        
        
    # find by name
    def find_by_name(self, name):

        """Method to retrieve a resource given the name"""
        
        if self.list.has_key(name):
            return self.list[name]
        else:
            return None
