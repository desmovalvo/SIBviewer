#!/usr/bin/python

# global requirements
from smart_m3.m3_kp_api import *

# local requirements
from SibQueries import *


# the KP
class SibInteractor:

    """This class constitutes the KP"""
    
    def __init__(self, host, port):

        """Constructor for the SibInteractor"""

        # setting class attributes
        self.host = host
        self.port = int(port)
        self.kp = m3_kp_api(False, self.host, self.port)


    def get_classes(self):

        """Method that returns the list of the rdf/owl/implicit classes"""

        # retrieve data
        classes = []
        self.kp.load_query_sparql(q_classes)
        for binding in self.kp.result_sparql_query:
            classes.append(binding[0][2])

        # return data
        return classes


    def get_everything(self):

        """Method to retrieve the entire knowledge base"""

        # retrieve data
        self.kp.load_query_rdf(q_everything)

        # return data
        return self.kp.result_rdf_query
