#!/usr/bin/python

# global requirements
import rdflib
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
        self.local_storage = None


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

        # # fill the local storage
        # self.local_storage = rdflib.Graph()
        # for t in self.kp.result_rdf_query:
        #     self.local_storage.add(self.uri_to_uriref_triple(t))
        # print len(self.local_storage)

        # return data
        return self.kp.result_rdf_query

    
    def custom_query(self, q):

        """Method to perform a custom query and return a list of URIs"""

        uri_list = []
        self.kp.load_query_sparql(q)
        for binding in self.kp.result_sparql_query:
            for variable in binding:
                if not(str(variable[2]) in uri_list):
                    uri_list.append(str(variable[2]))

        return uri_list

    
    def uri_to_uriref_triple(self, triple):
        return map(self.uri_to_uriref_node, triple)


    def uri_to_uriref_node(self, node):
        
        print "analyzing: " + str(node)
        if isinstance(node, URI):
            node = rdflib.URIRef(str(node))
        return node

        
            
