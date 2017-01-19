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
import sys
import math
import numpy
import getopt
import logging
from uuid import uuid4
from mayavi import mlab
from random import randint
from smart_m3.m3_kp_api import *

# constants
SIB_HOST = "localhost"
SIB_PORT = 10111
                
###############################################################
#
# main
#
###############################################################
if __name__ == "__main__":

    # setting logger
    logging.basicConfig(level=logging.DEBUG)

    ###############################################################
    #
    # read command line options
    #
    ###############################################################
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:o:b:", ["sib=", "owl=", "blaze="])
    except getopt.GetoptError as err:
        sys.exit(2)

    sib_host = None
    sib_port = None
    owl_file = None
    blaze_host = None
    
    for o, a in opts:
        if o in ("-s", "--sib"):
            sib_host, sib_port = a.split(":")
        elif o in ("-o", "--owl"):
            owl_file = a
        elif o in ("-b", "--blaze"):
            blaze_host = a
        else:
            assert False, "unhandled option"


    ###############################################################
    #
    # instantiate the KP 
    #
    ###############################################################
    kp = SibInteractor(sib_host, sib_port, owl_file, blaze_host)

    
    ###############################################################
    #
    # instantiate the viewer
    #
    ###############################################################            
    ui = Visualization(kp)
    ui.configure_traits()
