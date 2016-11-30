#!/usr/bin/python


# local requirements
from constants import *


# global requirements
import numpy


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
        r = self.scene.mlab.points3d(resource.x, resource.y, resource.z, color=purple, colormap="copper", scale_factor=5, resolution=32)
        t = self.scene.mlab.text(resource.x, resource.y, resource.name, z=resource.z, width=0.13)
        return r, t
        

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
        d = self.scene.mlab.plot3d(u, v, w, color=op.color, tube_radius=.2)
        t = self.scene.mlab.text(pred_x, pred_y, op.oproperty.split("#")[1], z=pred_z, width=0.13)
        return d, t


    # data property drawer
    def draw_data_property(self, dp):

        """Used to draw a data property"""

        # draw the data property
        o = self.scene.mlab.points3d(dp.x, dp.y, dp.z, color=green, colormap="copper", scale_factor=2, resolution=32)
        ol = self.scene.mlab.text(dp.x, dp.y, dp.get_value(), z=dp.z, width=0.13)

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
        p = self.scene.mlab.plot3d(u, v, w, color=green, tube_radius=.2)

        # write the name of the predicate
        pl = self.scene.mlab.text(pred_x, pred_y, str(dp.dproperty).split("#")[1], z=dp.z, width=0.13)

        return p, pl, o, ol

        
    # plane drawer
    def draw_plane(self, plane_number):

        """Used to draw a plane"""

        # draw the plane
        print "Drawing a plane"
        s = numpy.random.random((100, 100))
        i = self.scene.mlab.imshow(s, colormap="gray", opacity=0.5)
        i.actor.position = [0,0,plane_number*100-4]
