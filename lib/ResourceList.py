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

        
    # find by layer
    def get_layers_list(self, layerHeight = 100):

        """Method to retrieve all the resources on a plane"""
        
        layers_list = {}

        for r in self.list.keys():
            ll_key = str(int(self.list[r].z) / layerHeight)
            if layers_list.has_key(ll_key):
                layers_list[ll_key].append(r)
            else:
                layers_list[ll_key] = []
                layers_list[ll_key].append(r)

        return layers_list
