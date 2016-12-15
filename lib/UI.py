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
import pdb
import math
import numpy
import logging
from traits.api import HasTraits, Range, Str, Instance, on_trait_change, Enum, Button, List
from traitsui.api import View, Item, Group, VGroup, HGroup, ListEditor, ListStrEditor, TableEditor, TextEditor
from traitsui.table_column import ObjectColumn, ExpressionColumn
from traitsui.table_filter import EvalFilterTemplate, MenuFilterTemplate, RuleFilterTemplate, EvalTableFilter
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene


############################################################
#
# The following classes are used to draw tables on the
# User Interface
#
############################################################

class TraitResource(HasTraits):
    resource_name = Str

class TraitObjectProperty(HasTraits):
    obprop_name = Str
    obprop_range = Str
    obprop_domain = Str

class TraitDataProperty(HasTraits):
    dprop_name = Str
    dprop_range = Str
    dprop_domain = Str

class TraitClass(HasTraits):
    class_name = Str


# UI
class Visualization(HasTraits):

    # UI definition    
    scene      = Instance(MlabSceneModel, ())

    #################################################
    #
    # Widget for Log messages
    #
    #################################################

    lastlog_string = Str
    lastlog_widget = Item('lastlog_string', show_label = False, style = 'readonly')

    #################################################
    #
    # Widget for handling Resources
    #
    #################################################

    # resource table_editor
    selected_resource = Instance(TraitResource)
    resources_table_editor = TableEditor(
        columns = [ObjectColumn(name = 'resource_name', width = 1)],
        deletable = False,
        editable = False,
        sort_model  = True,
        auto_size   = False,
        orientation = 'vertical',
        selected = 'selected_resource',
        row_factory = TraitResource)

    # Resources list
    resources_list = List(TraitResource, selection_mode = "rows")
    resources_list_widget = Item('resources_list', show_label = False, editor = resources_table_editor, padding = 10),

    # Raise/Lower Button
    resources_button = Button(label="Raise/Lower Resource")      
    resources_button_widget = Item('resources_button', show_label=False)

    #################################################
    #
    # Widget for handling Classes
    #
    #################################################

    # class table_editor
    classes_table_editor = TableEditor(
        columns = [ObjectColumn(name='class_name', width = 1)],
        deletable = False,
        editable = False,
        sort_model = True,
        auto_size = False,
        orientation = 'vertical',
        row_factory = TraitClass)

    # new classes widget
    classes_list = List(TraitClass)
    classes_list_widget = Item('classes_list', show_label = False, editor = classes_table_editor, padding = 10),

    # classes button
    classes_button = Button(label="Raise/Lower Class")
    classes_button_widget = Item('classes_button', show_label=False)

    #################################################
    #
    # Widget for handling DataProperties
    #
    #################################################

    # dataproperty table_editor
    dataproperty_table_editor = TableEditor(
        columns = [ObjectColumn(name = 'dp_name', width = 1, label = "DataProperty"), 
                   ObjectColumn(name = 'dp_domain', width = 1, label = "Domain"), 
                   ObjectColumn(name = 'dp_range', width = 1, label = "Range")],
        deletable = False,
        editable = False,
        sort_model  = True,
        auto_size   = False,
        orientation = 'vertical',
        row_factory = TraitDataProperty)

    # new dataproperties widget
    dataproperties_list = List(TraitDataProperty)
    dataproperties_list_widget = Item('dataproperties_list', show_label = False, editor = dataproperty_table_editor, padding = 10),

    #################################################
    #
    # Widget for handling Objectproperties
    #
    #################################################

    # objectproperty table_editor
    objectproperty_table_editor = TableEditor(
        columns = [ObjectColumn(name = 'op_name', width = 1, label = "Objectproperty"), 
                   ObjectColumn(name = 'op_domain', width = 1, label = "Domain"), 
                   ObjectColumn(name = 'op_range', width = 1, label = "Range")],
        deletable = False,
        editable = False,
        sort_model  = True,
        auto_size   = False,
        orientation = 'vertical',
        row_factory = TraitObjectProperty)

    # new objectproperties widget
    objectproperties_list = List(TraitObjectProperty)
    objectproperties_list_widget = Item('objectproperties_list', show_label = False, editor = objectproperty_table_editor, padding = 10),

    #################################################
    #
    # Widget for handling custom queries
    #
    #################################################

    # query widgets
    query_string = Str
    query_entry_widget = Item('query_string', show_label=False)
    query_button = Button(label="SPARQL Query") 
    query_button_widget = Item('query_button', show_label=False)

    #################################################
    #
    # Widget for the stats
    #
    #################################################

    stats_string = Str
    stats_entry_widget = Item('stats_string', show_label=False, style="readonly")    

    #################################################
    #
    # Widget for refreshing the view
    #
    #################################################

    # refresh widgets
    refresh = Button(label="Refresh")
    refresh_w = Item('refresh', show_label=False)
   
    # widgets
    view = View(VGroup(HGroup(VGroup(resources_list_widget, resources_button_widget, # resources fields
                                     classes_list_widget, classes_button_widget, # classes fields
                                     dataproperties_list_widget, # dp fields
                                     objectproperties_list_widget, # op fields
                                     query_entry_widget, query_button_widget, # query fields
                                     stats_entry_widget,
                                     refresh_w), 
                              Item('scene', editor=SceneEditor(scene_class=MayaviScene), height=640, width=800, show_label=False))), lastlog_widget)
   
    def stampa(self):
        print "ASDFAF"

    # constructor
    def __init__(self, kp):

        """Initializer of the UI class"""

        ###################################################
        #
        # Initialize the scene
        #
        ###################################################

        # super class initializer
        HasTraits.__init__(self)

        # Drawer instance
        self.drawer = Drawer(self.scene)

        ###################################################
        #
        # Retrieve Data
        #
        ###################################################

        # store the kp
        self.kp = kp
        self.kp.get_everything()
        
        ###################################################
        #
        # Fill the side lists
        #
        ###################################################
        
        # get data properties
        dps = self.kp.get_data_properties()
        for dp in dps:
            self.dataproperties_list.append(TraitDataProperty(dp_name = str(dp[0]), dp_domain = str(dp[1]), dp_range = str(dp[2])))

        # get object properties
        ops = self.kp.get_object_properties()    
        for op in ops:
            self.objectproperties_list.append(TraitObjectProperty(op_name = str(op[0]), op_domain = str(op[1]), op_range = str(op[2])))

        # get instances
        for res in self.kp.get_instances():
            self.resources_list.append(TraitResource(resource_name = str(res[0])))

        # TODO: get classes

        # get stats
        self.stats_string = self.kp.get_stats()

        ###################################################
        #
        # Draw
        #
        ###################################################

        # fill the list of classes
        classes = self.kp.get_classes()
        for c in classes:
            self.classes_list.append(TraitClass(class_name = c))

        # initialize data structures
        self.res_list = ResourceList()

        # get and analyze knowledge
        p0, p1 = self.data_classifier()
        self.calculate_placement()
        self.draw_plane0()


    def _query_button_fired(self):

        """This method is executed when the query button is pressed"""    

        # debug print
        logging.debug("QUERY button pressed")
        self.lastlog_string = "QUERY button pressed"

        # retrieve URI related to the query
        # execute the sparql query
        uri_list = []
        if len(self.query_string) > 0:
             uri_list = self.kp.custom_query(self.query_string)

        self.redraw(uri_list)


    def redraw(self, uri_list):

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
        

    def _classes_button_fired(self):
        
        # debug print
        logging.debug("CLASS RAISE/LOWER button pressed")
        self.lastlog = "CLASSES RAISE/LOWER button pressed"
        print self.classes_list


    def _resources_button_fired(self):
        
        # getting selected resource
        r = self.selected_resource.resource_name

        # debug print
        logging.debug("Raising resource %s" % r)
        self.lastlog = "Raising resource %s" % r
        
        # raise
        self.redraw([r])


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
