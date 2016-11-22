#!/usr/bin/python


# local requirements
from lib.Resource import *
from lib.ResourceList import *
from lib.DataProperty import *
from lib.ObjectProperty import *

# global requirements
import math
import numpy
from uuid import uuid4
from mayavi import mlab
from random import randint
from smart_m3.m3_kp_api import *

# constants
SIB_HOST = "localhost"
SIB_PORT = 10111

# namespaces
rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
ns = "http://ns#"

# colors
red = (1,0,0)
green = (0,1,0)
blue = (0,0,1)
brown = (0.8,0.25,0)
purple = (0.7,0,1)
orange = (1,0.7,0)

# main
if __name__ == "__main__":

    # create a figure
    fig = mlab.figure(bgcolor=(0,0,0))

    # connect to the sib
    kp = m3_kp_api(False, SIB_HOST, SIB_PORT)
    
    # retrieve data
    kp.load_query_rdf(Triple(None, None, None))
    results = kp.result_rdf_query

    # initialize dictionaries
    resources = {}

    # draw the plane
    s = numpy.random.random((100, 100))
    i = mlab.imshow(s, colormap="gray", opacity=0.5)
    i.actor.position = [0,0,-1]
    
    #x, y = numpy.mgrid[0:100:0,0:100:0]
    #s = mlab.surf(x, y, numpy.asarray(x*0.1, 'd'))
    #mlab.surf(numpy.ones((100,100)), color=(1,1,1))

    # mlab.imshow(numpy.ones((100,100)), extent=[-10,10,-10,10,0,0])


    # create a Resource List
    res_list = ResourceList()
    
    # data analyzer
    for triple in results:

        sub = triple[0]
        pred = triple[1]
        ob = triple[2]
        
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
    print num_points
            
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
        mlab.points3d(x, y, z, color=purple, colormap="copper", scale_factor=5)
        mlab.text(x, y, r.name, z=0, width=0.13)

        # draw the data properties
        num_prop = len(r.data_properties)
        print num_prop
        print r.data_properties
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
                mlab.points3d(dx, dy, dz, color=green, colormap="copper", scale_factor=2)
                mlab.text(dx, dy, dp.get_value(), z=0, width=0.13)

                # draw the edge
                mlab.plot3d(u, v, w, color=green, tube_radius=.2)
                pred_x = numpy.mean(u)
                pred_y = numpy.mean(v)
                pred_z = numpy.mean(w)
                mlab.text(pred_x, pred_y, str(dp.dproperty).split("#")[1], z=0, width=0.13)
                
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
            mlab.plot3d(u, v, w, color=op.color, tube_radius=.2)
            pred_x = numpy.mean(u)
            pred_y = numpy.mean(v)
            pred_z = numpy.mean(w)
            mlab.text(pred_x, pred_y, op.oproperty.split("#")[1], z=0, width=0.13)

        

    # show
    mlab.show()
