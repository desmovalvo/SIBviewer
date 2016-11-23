#!/usr/bin/python


# local requirements
from lib.Drawer import *
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
from traits.api import HasTraits, Range, Str, Instance, on_trait_change, Enum, Button, List
from traitsui.api import View, Item, VGroup, HGroup
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene


# constants
SIB_HOST = "localhost"
SIB_PORT = 10111
VALUES = ["Male", "Female"]

class Visualization(HasTraits):

    # UI definition    
    scene      = Instance(MlabSceneModel, ())
    query      = Str
    possible_classes = List([])
    classes    = Enum(0, values="possible_classes")
    refresh    = Button()
    view = View(HGroup(Item('scene', editor=SceneEditor(scene_class=MayaviScene), height=640, width=800, show_label=False),
                       VGroup('_', 'query', 'classes', Item('refresh', show_label=False))))
   

    def __init__(self, kp):

        # super class initializer
        HasTraits.__init__(self)

        # store the kp
        self.kp = kp
        self.drawer = Drawer(self.scene)
        
        # fill the list of classes
        classes = self.kp.get_classes()
        for c in classes:
            self.possible_classes.append(c)
        
        # plot 
        self.sib_artist()

        
    @on_trait_change('query')
    def update_plot(self):
        pass
        

    def _refresh_fired(self):
        
        """This method is executed when the refresh button is pressed"""

        # clean and redraw
        self.scene.mlab.clf()
        self.sib_artist()
        
        
    def sib_artist(self):
    
        # retrieve data
        results = self.kp.get_everything()
    
        # initialize dictionaries
        resources = {}
    
        # draw the plane
        self.drawer.draw_plane(0)
            
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
                op = ObjectProperty(pred, sub_res, ob_res)
                sub_res.add_object_property(op)
    
            else:
    
                # new data property found
                dp = DataProperty(pred, sub_res, str(ob))
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
            res_list.list[resource].set_coordinates(x,y,z)
            
            # draw the resource
            self.drawer.draw_resource(r)
    
            # draw the data properties
            num_prop = len(r.data_properties)
            try:
                dangle = 360 / num_prop
                diteration = 0
                for dp in r.data_properties:
                    
                    dmultiplier = 7
                    dp.x = dmultiplier * math.cos(math.radians(diteration * dangle)) + r.get_coordinates()[0]
                    dp.y = dmultiplier * math.sin(math.radians(diteration * dangle)) + r.get_coordinates()[1]
                    dp.z = r.get_coordinates()[2]
                    
                    # draw the property                
                    self.drawer.draw_data_property(dp)
                    
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
            for op in res_list.list[resource].object_properties:

                # draw the edge
                self.drawer.draw_object_property(op)

                
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
