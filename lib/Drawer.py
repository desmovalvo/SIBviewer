#!/usr/bin/python


# local requirements
from constants import *

# global requirements
import time
import numpy
import logging


# the Drawer
class Drawer:

    """An helper to draw the 3d graph"""

    # constructor
    def __init__(self, scene):
        
        """Constructor for the Drawer class"""

        # store the scene
        self.scene = scene


    # resource drawer
    def draw_resource(self, resource):

        """Used to draw a resource"""
        
        # draw the resource
        st = time.time()
        if resource.isClass:
            r = self.scene.mlab.points3d(resource.x, resource.y, resource.z, color=orange, colormap="copper", scale_factor=5, resolution=8)
        else:
            if resource.isStatement:
                r = self.scene.mlab.points3d(resource.x, resource.y, resource.z, color=red, colormap="copper", scale_factor=5, resolution=8)
            else:
                r = self.scene.mlab.points3d(resource.x, resource.y, resource.z, color=purple, colormap="copper", scale_factor=5, resolution=8)
        et = time.time()
        logging.debug("Sphere drawn in %s ms" % (round(et-st, 3) * 1000))

        # return
        return r
        

    # object property drawer
    def draw_object_property(self, op):

        """Used to draw an object property"""

        # get subject and object
        s = op.s
        o = op.o
        
        # calculate coordinates to draw the edge and its name
        u = numpy.linspace(s.x, o.x, 10)
        v = numpy.linspace(s.y, o.y, 10)
        w = numpy.linspace(s.z, o.z, 10)
        pred_x = numpy.mean(u)
        pred_y = numpy.mean(v)
        pred_z = numpy.mean(w)

        # draw the edge and its name
        st = time.time()        
        d = self.scene.mlab.plot3d(u, v, w, color=op.color, tube_radius=.25)
        et = time.time()
        logging.debug("Edge drawn in %s ms" % (round(et-st, 3) * 1000)) 

        # return
        return d


    # data property drawer
    def draw_data_property(self, dp):

        """Used to draw a data property"""

        # draw the data property
        o = self.scene.mlab.points3d(dp.x, dp.y, dp.z, color=green, colormap="copper", scale_factor=2, resolution=8)

        # get the subject of the property
        r = dp.resource
        
        # find coordinates for the edge and for its name
        u = numpy.linspace(r.x, dp.x, 10)
        v = numpy.linspace(r.y, dp.y, 10)
        w = numpy.linspace(r.z, dp.z,10)    
        pred_x = numpy.mean(u)
        pred_y = numpy.mean(v)    
        pred_z = numpy.mean(w)

        # draw the edge
        st = time.time()
        p = self.scene.mlab.plot3d(u, v, w, color=green, tube_radius=.25)
        et = time.time()
        logging.debug("Sphere drawn in %s ms" % (round(et-st, 3) * 1000))
        
        # return
        return p, o

        
    # plane drawer
    def draw_plane(self, plane_number):

        """Used to draw a plane"""

        # draw the plane
        # s = numpy.random.random((100, 100))
        s = numpy.zeros((100, 100))
        i = self.scene.mlab.imshow(s, colormap="gray", opacity=0.7)
        i.actor.position = [0,0,plane_number*100-4]

        # return the plane
        return i

        
    # draw text
    def draw_text(self, resource):

        """Used to put text on the resource
        and all of its data properties"""

        # init objects
        objects = []

        # what to type?
        mystring = ""
        if resource.label:
            mystring = resource.label
        else:
            mystring = resource.name
        
        # draw label for the resource
        st = time.time()        
        t = self.scene.mlab.text(resource.x, resource.y, mystring, z=resource.z, width=char_width * len(mystring))
        et = time.time()
        logging.debug("Text drawn in %s ms" % (round(et-st, 3) * 1000)) 
        objects.append(t)
                
        # draw label for all the data properties
        for dp in resource.data_properties:
            t = self.scene.mlab.text(dp.x, dp.y, dp.get_value(), z=dp.z, width=char_width * len(str(dp.get_value())))
            objects.append(t)

        # return the drawn objects
        return objects
        
