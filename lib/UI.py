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
from traits.api import HasTraits, Range, Str, Instance, on_trait_change, Enum, Button, List, Int
from traitsui.api import View, Item, Group, VGroup, HGroup, ListEditor, ListStrEditor, TableEditor, TextEditor, Tabbed
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
    scene = Instance(MlabSceneModel, ())

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
    resources_button = Button(label="Raise/Lower resource to level:")      
    resources_button_widget = Item('resources_button', show_label=False)

    # Raise/Lower level selector
    resources_level_int = Int
    resources_level_int_widget = Item('resources_level_int', show_label=False)

    # Raise/Lower group
    resources_raiselower_hgroup = HGroup(resources_button_widget, resources_level_int_widget)

    # Group for all the data properties widget
    rpg = VGroup(resources_list_widget, resources_raiselower_hgroup, label="Resources:", show_border=True)

    #################################################
    #
    # Widget for handling Classes
    #
    #################################################

    # class table_editor
    selected_class = Instance(TraitClass)
    classes_table_editor = TableEditor(
        columns = [ObjectColumn(name='class_name', width = 1)],
        deletable = False,
        editable = False,
        sort_model = True,
        auto_size = False,
        orientation = 'vertical',
        selected = 'selected_class',
        row_factory = TraitClass)

    # new classes widget
    classes_list = List(TraitClass)
    classes_list_widget = Item('classes_list', show_label = False, editor = classes_table_editor, padding = 10),

    # classes button
    classes_button = Button(label="Raise/Lower class to level:")
    classes_button_widget = Item('classes_button', show_label=False)

    # Raise/Lower level selector
    classes_level_int = Int
    classes_level_int_widget = Item('classes_level_int', show_label=False)

    # Raise/Lower group
    classes_raiselower_hgroup = HGroup(classes_button_widget, classes_level_int_widget)

    # Group for all the data properties widget
    cpg = VGroup(classes_list_widget, classes_raiselower_hgroup, label="Classes:", show_border=True)

    #################################################
    #
    # Widget for handling DataProperties
    #
    #################################################

    # dataproperty table_editor
    selected_dp = Instance(TraitDataProperty)
    dataproperty_table_editor = TableEditor(
        columns = [ObjectColumn(name = 'dp_name', width = 1, label = "DataProperty"), 
                   ObjectColumn(name = 'dp_domain', width = 1, label = "Domain"), 
                   ObjectColumn(name = 'dp_range', width = 1, label = "Range")],
        deletable = False,
        editable = False,
        sort_model  = True,
        auto_size   = False,
        orientation = 'vertical',
        selected = 'selected_dp',
        row_factory = TraitDataProperty)

    # new dataproperties widget
    dataproperties_list = List(TraitDataProperty)
    dataproperties_list_widget = Item('dataproperties_list', show_label = False, editor = dataproperty_table_editor, padding = 10),

    # Raise/Lower Button
    dataproperties_button = Button(label="Raise/Lower Datatype Property to level:")      
    dataproperties_button_widget = Item('dataproperties_button', show_label=False)

    # Raise/Lower level selector
    dataproperties_level_int = Int
    dataproperties_level_int_widget = Item('dataproperties_level_int', show_label=False)

    # Raise/Lower group
    dataproperties_raiselower_hgroup = HGroup(dataproperties_button_widget, dataproperties_level_int_widget)

    # Group for all the data properties widget
    dpg = VGroup(dataproperties_list_widget, dataproperties_raiselower_hgroup, label="Data Properties:", show_border=True)
    
    #################################################
    #
    # Widget for handling Objectproperties
    #
    #################################################

    # objectproperty table_editor
    selected_op = Instance(TraitObjectProperty)
    objectproperty_table_editor = TableEditor(
        columns = [ObjectColumn(name = 'op_name', width = 1, label = "Objectproperty"), 
                   ObjectColumn(name = 'op_domain', width = 1, label = "Domain"), 
                   ObjectColumn(name = 'op_range', width = 1, label = "Range")],
        deletable = False,
        editable = False,
        sort_model  = True,
        auto_size   = False,
        orientation = 'vertical',
        selected = 'selected_op',
        row_factory = TraitObjectProperty)

    # new objectproperties widget
    objectproperties_list = List(TraitObjectProperty)
    objectproperties_list_widget = Item('objectproperties_list', show_label = False, editor = objectproperty_table_editor, padding = 10),

    # Raise/Lower Button
    objectproperties_button = Button(label="Raise/Lower Object Property to level:")      
    objectproperties_button_widget = Item('objectproperties_button', show_label=False)

    # Hide Button
    objectproperties_hide_button = Button(label="Hide/Show Object Property")      
    objectproperties_hide_button_widget = Item('objectproperties_hide_button', show_label=False)

    # Raise/Lower level selector
    objectproperties_level_int = Int
    objectproperties_level_int_widget = Item('objectproperties_level_int', show_label=False)

    # Raise/Lower group
    objectproperties_raiselower_hgroup = HGroup(objectproperties_hide_button_widget, objectproperties_button_widget, objectproperties_level_int_widget)

    # Group for all the object properties widgets
    opg = VGroup(objectproperties_list_widget, objectproperties_raiselower_hgroup, label="Object Properties:", show_border=True)

    #################################################
    #
    # Widget for handling custom queries
    #
    #################################################

    # query widgets
    query_string = Str
    query_entry_widget = Item('query_string', show_label=False)

    # query button
    query_button = Button(label="SPARQL Query") 
    query_button_widget = Item('query_button', show_label=False)

    # Raise/Lower level selector
    query_level_int = Int
    query_level_int_widget = Item('query_level_int', show_label=False)

    # Raise/Lower group
    query_raiselower_hgroup = HGroup(query_button_widget, query_level_int_widget)

    # group for all the query widgets
    qpg = VGroup(query_entry_widget, query_raiselower_hgroup, label="SPARQL Query", show_border=True)

    #################################################
    #
    # Widget for handling planes
    #
    #################################################

    # query button
    plane_button = Button(label="Merge plane A on plane B") 
    plane_button_widget = Item('plane_button', show_label=False)

    # Raise/Lower level selector
    plane_level_int1 = Int
    plane_level_int1_widget = Item('plane_level_int1', show_label=False)
    plane_level_int2 = Int
    plane_level_int2_widget = Item('plane_level_int2', show_label=False)

    # Raise/Lower group
    plane_merge_hgroup = HGroup(plane_level_int1_widget, plane_button_widget, plane_level_int2_widget)

    # group for all the query widgets
    ppg = VGroup(plane_merge_hgroup, label="Planes", show_border=True)


    #################################################
    #
    # Widget for exporting png
    #
    #################################################

    # export widgets
    export_button = Button(label="Export as PNG image") 
    export_button_widget = Item('export_button', show_label=False)


    #################################################
    #
    # Widget for the stats
    #
    #################################################

    stats_string = Str
    stats_entry_widget = Item('stats_string', show_label=False, style="readonly")    

    #################################################
    #
    # Widget for resetting the planes
    #
    #################################################

    # refresh widgets
    reset = Button(label="Reset placement")
    reset_w = Item('reset', show_label=False)

    #################################################
    #
    # Widget for refreshing the view
    #
    #################################################

    # refresh widgets
    refresh = Button(label="Refresh")
    refresh_w = Item('refresh', show_label=False)
   
    # widgets
    view = View(VGroup(HGroup(VGroup(Tabbed(rpg, cpg, dpg, opg, qpg, ppg),
                                     stats_entry_widget,
                                     export_button_widget,
                                     reset_w,
                                     refresh_w), 
                              Item('scene', editor=SceneEditor(scene_class=MayaviScene), height=640, width=800, show_label=False))), 
                lastlog_widget,
                scrollable=True)
   
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

        # get classes
        cs = self.kp.get_classes()
        for c in cs:
            self.classes_list.append(TraitClass(class_name = c))

        # get stats
        self.stats_string = self.kp.get_stats()

        ###################################################
        #
        # Draw
        #
        ###################################################

        # initialize data structures
        self.res_list = ResourceList()
        self.planes = []

        # get and analyze knowledge
        p0, p1 = self.data_classifier()
        self.calculate_placement()
        self.draw()


    @on_trait_change('scene.activated')
    def scene_ready(self):

        # get the figure and bind the picker
        self.figure = self.scene.mayavi_scene
        self.figure.on_mouse_pick(self.picker_callback)


    def picker_callback(self, picker):
            
        # find the resource related to the clicked object
        # ..if any

        # NOTE: this code is absolutely raw. Needs to be
        # optimized and many tricks can be used to speed
        # up the execution even with large datasets.

        for resource in self.res_list.list.keys():

            # cycle over the resources
            r = self.res_list.list[resource]      
            if picker.actor in r.gitem.actor.actors:
                logging.debug("Received click on %s" % r.name)
                self.lastlog_string = r.name
                break

            else:                

                # cycle over the data properties
                for dp in r.data_properties:
                    if picker.actor in dp.gitem_predicate.actor.actors:
                        logging.debug("Received click on %s" % dp.dproperty)
                        self.lastlog_string = dp.dproperty
                        break
                        
                # cycle over the object properties
                for op in r.object_properties:
                    if picker.actor in op.gitem.actor.actors:
                        logging.debug("Received click on %s" % op.oproperty)
                        self.lastlog_string = op.oproperty
                        break


    def _plane_button_fired(self):

        """This method is used to merge a plane with the plane 0"""

        # debug print
        logging.debug("Merge plane function called")
        self.lastlog_string = "Merge plane function called"

        # get the plane to merge
        l1 = self.plane_level_int1    
        l2 = self.plane_level_int2   

        # get items on that plane
        uri_list = self.res_list.find_by_layer(l1)
        
        # move items on plane 0
        self.redraw(uri_list, l2)


    def _export_button_fired(self):
        
        """This method is used to export the scene to a PNG image"""
        
        # debug print
        logging.debug("Exporting the current scene to a PNG image")
        self.lastlog_string = "Exporting the current scene to a PNG image"

        # # export
        # self.scene.save("/tmp/output.png")

        self.res_list.find_by_layer(0, 100)


    def _reset_fired(self):
        
        """This method is used to reset the view to plane 0"""
        
        # debug print
        logging.debug("Resetting the view to plane 0")
        self.lastlog_string = "Resetting the view to plane 0"

        # reset
        self.redraw(None, 0)


    def _query_button_fired(self):

        """This method is executed when the query button is pressed"""    

        # debug print
        logging.debug("QUERY button pressed")
        self.lastlog_string = "QUERY button pressed"

        # read the required value
        l = self.query_level_int    
     
        # retrieve URI related to the query
        # execute the sparql query
        uri_list = []
        if len(self.query_string) > 0:
             uri_list = self.kp.custom_query(self.query_string)

        # move objects!
        self.redraw(uri_list, l)


    def redraw(self, uri_list, plane):

        """This function moves all the resources of uri_list
        to the plane indicated by the plane variable. If uri_list 
        is None and plane is 0, then everything is reset to the 
        initial position."""

        # temporarily disable rendering for faster visualization
        self.scene.disable_render = True

        # raise nodes
        for resource in self.res_list.list.keys():
            r = self.res_list.list[resource]      
            if (not(uri_list) and plane == 0) or (r.name in uri_list):
                
                # remove the old object
                r.gitem.remove() 
                r.gitem_label.remove()
                
                # design the new object on a different plane
                r.z = 100 * int(plane)
                gitem, gitem_label = self.drawer.draw_resource(r)
                r.gitem = gitem
                r.gitem_label = gitem_label
                
                # also raise the dp
                for dp in r.data_properties:
                     
                    # delete the old property
                    dp.gitem_object.remove()
                    dp.gitem_objectlabel.remove()
                    dp.gitem_predicate.remove()
                    
                    # update the coordinate
                    dp.z = 100 * int(plane)
                     
                    # draw the property                 
                    a1, a2, a3 = self.drawer.draw_data_property(dp)
                    dp.gitem_predicate = a1
                    dp.gitem_object = a2
                    dp.gitem_objectlabel = a3
                 
        # also redraw the object properties
        for resource in self.res_list.list.keys():
            r = self.res_list.list[resource]      
            for op in r.object_properties:
                 
                # delete the old object property
                op.gitem.remove()
                     
                # draw the edge
                item = self.drawer.draw_object_property(op)       
                op.gitem = item

        # remove existing planes and draw a plane where needed
        needed_planes = self.res_list.get_layers_list().keys()
        for plane in self.planes:
            plane.remove()
        self.planes = []
        for needed_plane in needed_planes:
            self.planes.append(self.drawer.draw_plane(int(needed_plane)))
    
        # enable rendering
        self.scene.disable_render = False
        

    def _classes_button_fired(self):
        
        # getting selected class
        c = self.selected_class.class_name
    
        # read the required value
        l = self.classes_level_int    

        # debug print
        logging.debug("Raising instances of class %s" % c)
        self.lastlog_string = "Raising instances of class %s" % c    

        # getting instances of classs c
        uri_list = []
        qres = self.kp.get_instances_of(c)
        for res in qres:
            uri_list.append(str(res[0]))

        # raising instances
        self.redraw(uri_list, l)        


    def _resources_button_fired(self):
        
        # getting selected resource
        r = self.selected_resource.resource_name

        # read the required value
        l = self.resources_level_int    

        # debug print
        logging.debug("Raising resource %s" % r)
        self.lastlog_string = "Raising resource %s" % r
        
        # raise
        self.redraw([r], l)


    def _dataproperties_button_fired(self):
        
        # getting selected datatype property
        dp = self.selected_dp.dp_name

        # read the required value
        l = self.dataproperties_level_int    
    
        # debug print
        logging.debug("Raising instances of class %s" % dp)
        self.lastlog_string = "Raising instances with datatype property %s" % dp

        # getting instances with dataproperty dp
        uri_list = []
        qres = self.kp.get_instances_with_dp(dp)
        for res in qres:
            uri_list.append(str(res[0]))

        # raising instances
        self.redraw(uri_list, l)


    def _objectproperties_button_fired(self):
        
        # getting selected object property
        op = self.selected_op.op_name
    
        # read the required value
        l = self.objectproperties_level_int    

        # debug print
        logging.debug("Raising instances with object property %s" % op)
        self.lastlog_string = "Raising instances with object property %s" % op

        # getting instances with object property op
        uri_list = []
        qres = self.kp.get_instances_with_op(op)
        for res in qres:
            uri_list.append(str(res[0]))

        # raising instances
        self.redraw(uri_list, l)


    def _objectproperties_hide_button_fired(self):
        
        # getting selected object property
        opname = self.selected_op.op_name
    
        # debug print
        logging.debug("Hide/show object property %s" % opname)
        self.lastlog_string = "Hide/show object property %s" % opname               

        # draw object properties
        for resource in self.res_list.list.keys():                
            for op in self.res_list.list[resource].object_properties:
                if op.oproperty == opname:
                    
                    # if item is None -> draw, else remove
                    if op.gitem:
                        op.gitem.remove()
                        op.gitem = None
                    else:
                        # draw the edge
                        item = self.drawer.draw_object_property(op)       
                        op.gitem = item


    def _refresh_fired(self):
        
        """This method is executed when the refresh button is pressed"""
        
        # debug
        logging.debug("REFRESH button pressed")

        # clean and redraw
        self.scene.mlab.clf()
        p0, p1 = self.data_classifier()
        self.sib_artist(p0, p1)


    def data_classifier_ng(self):

        # re-init res_list
        self.res_list = ResourceList()
        
        # retrieve data
        results = self.kp.get_everything()

        # data analyzer
        for triple in results:
    
            sub, pred, ob = triple
            
            # analyze the subject
            sub_res = self.res_list.find_by_name(str(sub))
            if not sub_res:
                sub_res = Resource(sub)
                self.res_list.add_resource(sub_res)

            # analyze the object
            if isinstance(ob, URI):
                ob_res = self.res_list.find_by_name(str(ob))
                if not ob_res:
                    ob_res = Resource(ob)
                    self.res_list.add_resource(ob_res)
                    
            # analyze the predicate (looking at the object)
            if isinstance(ob, URI):
    
                # new object property found
                op = ObjectProperty(pred, sub_res, ob_res)
                sub_res.add_object_property(op)
    
            else:
    
                # new data property found
                dp = DataProperty(pred, sub_res, str(ob))
                sub_res.add_data_property(dp)        


    def data_classifier(self, sparql_query=None):

        # re-init res_list
        self.res_list = ResourceList()
        
        # planes
        plane0 = []
        plane1 = []
        
        # retrieve data
        results = self.kp.get_everything()

        # retrieve classes
        cs = self.kp.get_classes()
        print cs

        # execute the sparql query
        uri_list = []
        if sparql_query:
            uri_list = self.kp.custom_query(sparql_query)

        # data analyzer
        for triple in results:
    
            sub, pred, ob = triple
            print triple
            
            # analyze the subject
            sub_res = self.res_list.find_by_name(str(sub))
            if not sub_res:
                
                if str(sub) in cs:                                        
                    sub_res = Resource(sub, True)
                else:
                    sub_res = Resource(sub, False)

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

                    if str(ob) in cs:                    
                        ob_res = Resource(ob, True)
                    else:
                        ob_res = Resource(ob, False)

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

                
    def calculate_placement_ng(self, uriplanes = None):

        """This method is used to calculate the best placement for
        nodes. uriplanes is a list of lists.  The first list specifies
        the items to be placed on plane 1 (the default is plane 0),
        the second on plane 2, and so on. If None everything is placed
        on plane 0"""

        # calculate the elements for each plane
        if uriplanes:

            # determine the number of planes
            num_planes = len(uriplanes)
            
            # create a list for every plane
            planes = []
            for p in range(num_planes):
                planes.append([])
            
            # fill the previously created lists
            for resource in self.res_list.list.keys():

                # find in which plane must be placed the resource
                plane_found = False
                r = self.res_list.list[resource]      
                plane_counter = 0
                for uriplane in uriplanes:
                    plane_counter += 1
                    if r.name in uriplane:                        
                        print "PLANE FOUND!"
                        planes[plane_counter].append(r)
                        plane_found = True
                        break
                if not plane_found:
                    planes[0].append(r)
                    
        print "PLANES ARE:"
        counter = 0
        for plane in planes:
            print "* plane %s:" % counter
            print plane
            print
            counter += 1


    def calculate_placement(self):

        """This method is used to calculate the best
        placement for nodes on the plane 0"""

        # resource coordinates generator
        num_points = len(self.res_list.list)
        
        # divide 360 by the number of points to get the base angle
        if num_points > 0:
            multiplier = 30
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
        

    def draw(self):

        """This method is called at init time or at refresh time.
        Everything is placed on plane 0. Then the selected items
        can be moved to other planes with proper functions"""

        # disable rendering
        self.scene.disable_render = True

        # create a dict for plane0
        plane0_dict = {}

        # draw plane
        plane0_dict["plane"] = self.drawer.draw_plane(0)
        plane0_dict["widgets"] = []

        # draw resources
        for resource in self.res_list.list.keys():
            r = self.res_list.list[resource]        
            gitem, gitem_label = self.drawer.draw_resource(r)
            r.gitem = gitem
            r.gitem_label = gitem_label

            # draw data properties
            for dp in r.data_properties:
                
                # draw the property                
                a1, a2, a3 = self.drawer.draw_data_property(dp)
                dp.gitem_object = a2
                dp.gitem_objectlabel = a3
                dp.gitem_predicate = a1

        # draw object properties
        for resource in self.res_list.list.keys():                
            for op in self.res_list.list[resource].object_properties:

                # draw the edge
                item = self.drawer.draw_object_property(op)       
                op.gitem = item
                # op.gitem_label = itemlabel

        # enable rendering
        self.scene.disable_render = False        

        # store the first plane
        self.planes.append(plane0_dict["plane"])
            
        
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
