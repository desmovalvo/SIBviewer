#!/usr/bin/python


# local requirements
from lib.Resource import *
from lib.constants import *
from lib.ResourceList import *
from lib.DataProperty import *
from lib.SibInteractor import *
from lib.ObjectProperty import *

# global requirements
import sys
import math
import numpy
import getopt
from uuid import uuid4
from mayavi import mlab
from random import randint
from smart_m3.m3_kp_api import *
from traits.api import HasTraits, Range, Str, Instance, on_trait_change, Enum, Button
from traitsui.api import View, Item, HGroup
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene


# constants
SIB_HOST = "localhost"
SIB_PORT = 10111


class Visualization(HasTraits):

    # UI definition    
    scene      = Instance(MlabSceneModel, ())
    query      = Str
    classes    = Enum('female', 'Male')
    refresh    = Button()
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene), height=640, width=800, show_label=False),
                HGroup('_', 'query', 'classes', Item('refresh', show_label=False)))
    
    
    def __init__(self, kp):

        # super class initializer
        HasTraits.__init__(self)

        # plot 
        #x, y, z, t = curve(self.meridional, self.transverse)
        #self.plot = self.scene.mlab.plot3d(x, y, z, t, colormap='Spectral')
        self.sib_artist()

        
    @on_trait_change('query')
    def update_plot(self):
        self.classes = "Male"
        sib_artist()
        

    def _refresh_fired(self):
        
        """This method is executed when the refresh button is pressed"""

        # clean and redraw
        self.scene.mlab.clf()
        self.sib_artist()
        
        
    def sib_artist(self):
    
        # retrieve data
        results = kp.get_everything()
    
        # initialize dictionaries
        resources = {}
    
        # draw the plane
        s = numpy.random.random((100, 100))
        i = self.scene.mlab.imshow(s, colormap="gray", opacity=0.5)
        i.actor.position = [0,0,-1]
            
        # create a Resource List
        res_list = ResourceList()
        
        # data analyzer
        for triple in results:
    
            sub, pred, ob = triple
            
            # analyze the subject
            sub_res = res_list.find_by_name(str(sub))
            if not sub_res:
                sub_res = Resource(sub)
                res_list.add_resource(sub_res)
    
            # analyze the object
            if isinstance(ob, URI):
                ob_res = res_list.find_by_name(str(ob))
                if not ob_res:
                    ob_res = Resource(ob)
                    res_list.add_resource(ob_res)
                    
            # analyze the predicate (looking at the object)
            if isinstance(ob, URI):
    
                # new object property found
                op = ObjectProperty(pred, ob_res)
                sub_res.add_object_property(op)
    
            else:
    
                # new data property found
                dp = DataProperty(pred, str(ob))
                sub_res.add_data_property(dp)
    
    
        ##################################################
        #
        # draw resources and data properties
        #
        ##################################################
        
        # resource coordinates generator
        num_points = len(res_list.list)
        
        # divide 360 by the number of points to get the base angle
        multiplier = 20
        angle = 360 / num_points
        iteration = 0 
        for resource in res_list.list.keys():
    
            r = res_list.list[resource]        
            x = multiplier * math.cos(math.radians(iteration * angle))
            y = multiplier * math.sin(math.radians(iteration * angle))
            z = 0
            res_list.list[resource].set_coordinates(x,y)
            
            # draw the resource
            self.scene.mlab.points3d(x, y, z, color=purple, colormap="copper", scale_factor=5)
            self.scene.mlab.text(x, y, r.name, z=0, width=0.13)
    
            # draw the data properties
            num_prop = len(r.data_properties)
            try:
                dangle = 360 / num_prop
                diteration = 0
                for dp in r.data_properties:
                    
                    dmultiplier = 7
                    dx = dmultiplier * math.cos(math.radians(diteration * dangle)) + r.get_coordinates()[0]
                    dy = dmultiplier * math.sin(math.radians(diteration * dangle)) + r.get_coordinates()[1]
                    dz = 0
                    
                    # draw the property
                    u = numpy.linspace(x, dx, 10)
                    v = numpy.linspace(y, dy, 10)
                    w = numpy.linspace(0,0,10)
                    self.scene.mlab.points3d(dx, dy, dz, color=green, colormap="copper", scale_factor=2)
                    self.scene.mlab.text(dx, dy, dp.get_value(), z=0, width=0.13)
    
                    # draw the edge
                    self.scene.mlab.plot3d(u, v, w, color=green, tube_radius=.2)
                    pred_x = numpy.mean(u)
                    pred_y = numpy.mean(v)
                    pred_z = numpy.mean(w)
                    self.scene.mlab.text(pred_x, pred_y, str(dp.dproperty).split("#")[1], z=0, width=0.13)
                    
                    diteration += 1
            except:
                pass
            
            iteration += 1
    
    
        ##################################################
        #
        # draw object properties
        #
        ##################################################
    
        for resource in res_list.list.keys():
    
            sres = res_list.list[resource]
            sx, sy = sres.get_coordinates()
    
            for op in sres.object_properties:
    
                ores = op.get_value()
                ox, oy = ores.get_coordinates()
    
                # draw the edge
                u = numpy.linspace(sx, ox, 10)
                v = numpy.linspace(sy, oy, 10)
                w = numpy.linspace(0,0,10)
                self.scene.mlab.plot3d(u, v, w, color=op.color, tube_radius=.2)
                pred_x = numpy.mean(u)
                pred_y = numpy.mean(v)
                pred_z = numpy.mean(w)
                self.scene.mlab.text(pred_x, pred_y, op.oproperty.split("#")[1], z=0, width=0.13)

                
###############################################################
#
# main
#
###############################################################
if __name__ == "__main__":

    
    ###############################################################
    #
    # read command line options
    #
    ###############################################################
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:", ["sib="])
    except getopt.GetoptError as err:
        sys.exit(2)

    sib_host = None
    sib_port = None
    
    for o, a in opts:
        if o in ("-s", "--sib"):
            sib_host, sib_port = a.split(":")
        else:
            assert False, "unhandled option"


    ###############################################################
    #
    # instantiate the KP
    #
    ###############################################################
    kp = SibInteractor(sib_host, sib_port)

    
    ###############################################################
    #
    # instantiate the viewer
    #
    ###############################################################            
    ui = Visualization(kp)
    ui.configure_traits()
