#!/usr/bin/python

# local requirements
from lib.UI import *
from lib.Drawer import *
from lib.Resource import *
from lib.constants import *
from lib.ResourceList import *
from lib.DataProperty import *
from lib.SibInteractor import *
from lib.ObjectProperty import *

# global requirements
import math
import numpy
import logging
from traits.api import HasTraits, Range, Str, Instance, on_trait_change, Enum, Button, List
from traitsui.api import View, Item, VGroup, HGroup
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene

# UI
class Visualization(HasTraits):

    # UI definition    
    resources = Str
    scene      = Instance(MlabSceneModel, ())

    # classes widgets
    possible_classes = List([])
    classes = Enum(0, values="possible_classes", style="simple")
    classes_w = Item('classes', show_label=True, label="Classes")
    classes_rl = Button(label="Raise/Lower")
    classes_rl_w = Item('classes_rl', show_label=False)

    # resources widgets
    possible_resources = List([])
    resources = Enum(0, values="possible_resources", style="simple")
    resources_w = Item('resources', show_label=True, label="Resources")
    resources_rl = Button(label="Raise/Lower")
    resources_rl_w = Item('resources_rl', show_label=False)

    # properties widgets
    possible_properties = List([])
    properties = Enum(0, values="possible_properties", style="simple")
    properties_w = Item('properties', show_label=True, label="Properties")
    properties_rl = Button(label="Raise/Lower")
    properties_rl_w = Item('properties_rl', show_label=False)

    # query widgets
    query = Str
    query_w = Item('query')
    query_rl = Button(label="Query") 
    query_rl_w = Item('query_rl', show_label=False)

    # refresh widgets
    refresh = Button(label="Refresh")
    refresh_w = Item('refresh', show_label=False)

    # widgets
    view = View(HGroup(VGroup(classes_w, 
                              classes_rl_w, 
                              resources_w, 
                              resources_rl_w, 
                              properties_w, 
                              properties_rl_w,
                              query_w,
                              query_rl_w,
                              refresh_w), 
                       Item('scene', editor=SceneEditor(scene_class=MayaviScene), height=640, width=800, show_label=False)))
   
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

        # initialize data structures
        self.res_list = ResourceList()

        # get and analyze knowledge
        p0, p1 = self.data_classifier()
        self.calculate_placement()
        self.draw_plane0()

     
    def _query_rl_fired(self):

        """This method is executed when the query button is pressed"""    

        # debug print
        logging.debug("QUERY button pressed")

        # retrieve URI related to the query
        # execute the sparql query
        uri_list = []
        if len(self.query) > 0:
             uri_list = self.kp.custom_query(self.query)

        # raise nodes
        for resource in self.res_list.list.keys():
            r = self.res_list.list[resource]      
            if r.name in uri_list:

                # remove the old object
                r.gitem.remove() 
                r.gitem_label.remove()

                # design the new object on a different plane
                r.z = 100
                gitem, gitem_label = self.drawer.draw_resource(r)
                r.gitem = gitem
                r.gitem_label = gitem_label

                # also raise the dp
                for dp in r.data_properties:
                    
                    # delete the old property
                    dp.gitem_object.remove()
                    dp.gitem_objectlabel.remove()
                    dp.gitem_predicate.remove()
                    dp.gitem_predicatelabel.remove()
                                        
                    # update the coordinate
                    dp.z = 100
                    
                    # draw the property                 
                    a1, a2, a3, a4 = self.drawer.draw_data_property(dp)
                    dp.gitem_object = a1
                    dp.gitem_objectlabel = a2
                    dp.gitem_predicate = a3
                    dp.gitem_predicatelabel = a4
                
        # also redraw the object properties
        for resource in self.res_list.list.keys():
            r = self.res_list.list[resource]      
            for op in r.object_properties:
                
                # delete the old object property
                op.gitem.remove()
                op.gitem_label.remove()
                    
                # draw the edge
                item, itemlabel = self.drawer.draw_object_property(op)       
                op.gitem = item
                op.gitem_label = itemlabel
        

    def _classes_rl_fired(self):
        
        # debug print
        logging.debug("CLASSES RAISE/LOWER button pressed")


    def _resources_rl_fired(self):
        
        # debug print
        logging.debug("RESOURCES RAISE/LOWER button pressed")


    def _properties_rl_fired(self):
        
        # debug print
        logging.debug("PROPERTIES RAISE/LOWER button pressed")
                

    def _refresh_fired(self):
        
        """This method is executed when the refresh button is pressed"""
        
        # debug
        logging.debug("REFRESH button pressed")

        # clean and redraw
        self.scene.mlab.clf()
        p0, p1 = self.data_classifier()
        self.sib_artist(p0, p1)


    def data_classifier(self, sparql_query=None):

        # re-init res_list
        self.res_list = ResourceList()
        
        # planes
        plane0 = []
        plane1 = []
        
        # retrieve data
        results = self.kp.get_everything()

        # execute the sparql query
        uri_list = []
        if sparql_query:
            uri_list = self.kp.custom_query(sparql_query)

        # data analyzer
        for triple in results:
    
            sub, pred, ob = triple
            
            # analyze the subject
            sub_res = self.res_list.find_by_name(str(sub))
            if not sub_res:
                sub_res = Resource(sub)
                self.res_list.add_resource(sub_res)
                
                # determine the plane for the subject
                if str(sub) in uri_list:
                    plane1.append(sub_res)
                else:
                    plane0.append(sub_res)
    
            # analyze the object
            if isinstance(ob, URI):
                ob_res = self.res_list.find_by_name(str(ob))
                if not ob_res:
                    ob_res = Resource(ob)
                    self.res_list.add_resource(ob_res)

                    # determine the plane for the object
                    if str(ob) in uri_list:
                        plane1.append(ob_res)
                    else:
                        plane0.append(ob_res)
                    
            # analyze the predicate (looking at the object)
            if isinstance(ob, URI):
    
                # new object property found
                op = ObjectProperty(pred, sub_res, ob_res)
                sub_res.add_object_property(op)
    
            else:
    
                # new data property found
                dp = DataProperty(pred, sub_res, str(ob))
                sub_res.add_data_property(dp)        

        # return
        return plane0, plane1

                
    def calculate_placement(self):

        """This method is used to calculate the best
        placement for nodes on the plane 0"""

        # resource coordinates generator
        num_points = len(self.res_list.list)
        
        # divide 360 by the number of points to get the base angle
        if num_points > 0:
            multiplier = 20
            angle = 360 / num_points
            iteration = 0 
            for resource in self.res_list.list.keys():
        
                r = self.res_list.list[resource]        
                x = multiplier * math.cos(math.radians(iteration * angle))
                y = multiplier * math.sin(math.radians(iteration * angle))
                self.res_list.list[resource].set_coordinates(x,y,0)
        
                # calculate coordinates for datatype properties
                num_prop = len(r.data_properties)
                try:
                    dangle = 360 / num_prop
                    diteration = 0
                    for dp in r.data_properties:
                        
                        dmultiplier = 7
                        dp.x = dmultiplier * math.cos(math.radians(diteration * dangle)) + r.get_coordinates()[0]
                        dp.y = dmultiplier * math.sin(math.radians(diteration * dangle)) + r.get_coordinates()[1]
                        dp.z = r.get_coordinates()[2]                                                
                        diteration += 1
                except:
                    pass                
                iteration += 1   
        

    def draw_plane0(self):

        # draw plane
        self.drawer.draw_plane(0)

        # draw resources
        for resource in self.res_list.list.keys():
            r = self.res_list.list[resource]        
            gitem, gitem_label = self.drawer.draw_resource(r)
            r.gitem = gitem
            r.gitem_label = gitem_label

            # draw data properties
            for dp in r.data_properties:
                
                # draw the property                
                a1, a2, a3, a4 = self.drawer.draw_data_property(dp)
                dp.gitem_object = a1
                dp.gitem_objectlabel = a2
                dp.gitem_predicate = a3
                dp.gitem_predicatelabel = a4

        # draw object properties
        for resource in self.res_list.list.keys():                
            for op in self.res_list.list[resource].object_properties:

                # draw the edge
                item, itemlabel = self.drawer.draw_object_property(op)       
                op.gitem = item
                op.gitem_label = itemlabel

        
    def sib_artist(self, plane0, plane1):

        # draw the planes
        self.drawer.draw_plane(0)
        if len(plane1) > 0:
            self.drawer.draw_plane(1)                    
        
        ##################################################
        #
        # draw resources and data properties
        #
        ##################################################
        
        # resource coordinates generator
        num_points = len(self.res_list.list)
        
        # divide 360 by the number of points to get the base angle
        if num_points > 0:
            multiplier = 20
            angle = 360 / num_points
            iteration = 0 
            for resource in self.res_list.list.keys():
        
                r = self.res_list.list[resource]        
                x = multiplier * math.cos(math.radians(iteration * angle))
                y = multiplier * math.sin(math.radians(iteration * angle))
    
                if r in plane0:
                    z = 0
                else:
                    z = 100
                self.res_list.list[resource].set_coordinates(x,y,z)
                
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
    
        for resource in self.res_list.list.keys():                
            for op in self.res_list.list[resource].object_properties:

                # draw the edge
                self.drawer.draw_object_property(op)
