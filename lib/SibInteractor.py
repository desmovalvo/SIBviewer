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


    def get_instances(self):
        
        """Method to retrieve all the instances"""
        
        # retrieve data
        qres = self.local_storage.query(q_instances)
        return qres 
        

    def get_instances_of(self, classname):
        
        """Method to retrieve all the instances
        of the given class"""
        
        # retrieve data
        qres = self.local_storage.query(q_instances_of_class % classname)
        return qres


    def get_instances_with_dp(self, dp):
        
        """Method to retrieve all the instances
        with a given datatype property"""

        # retrieve data
        qres = self.local_storage.query(q_instances_with_dp % dp)
        return qres


    def get_instances_with_op(self, op):
        
        """Method to retrieve all the instances
        with a given object property"""

        # retrieve data
        qres = self.local_storage.query(q_instances_with_dp % op)
        return qres


    def get_everything(self):

        """Method to retrieve the entire knowledge base"""

        # initialize and fill the local storage
        self.local_storage = rdflib.Graph()

        # retrieve data
        self.kp.load_query_rdf(q_everything)

        # fill the local storage
        for sib_triple in self.kp.result_rdf_query:

            # get the fields
            s, p, o = sib_triple
            
            # analyze the subject
            # NOTE: currently we suppose that all the subjects are URIs
            # NOTE: this must be generalized to admit BNodes.
            ss = rdflib.URIRef(str(s))

            # analyze the predicate
            pp = rdflib.URIRef(str(p))

            # analyze the object            
            if isinstance(o, URI):
                oo = rdflib.URIRef(str(o))
            else:
                oo = rdflib.Literal(str(o))

            # add the new triple to the local storage
            self.local_storage.add((ss, pp, oo))

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


    def get_data_properties(self):

        """Method used to retrieve alle the data
         properties defined in the ontology"""

        qres = self.local_storage.query(q_dproperties)
        return qres
        
    def get_object_properties(self):

        """Method used to retrieve alle the data
         properties defined in the ontology"""
        
        qres = self.local_storage.query(q_oproperties)
        return qres

        
    def get_stats(self):

        """Stats of the triples"""
        
        ct = None
        for res in self.local_storage.query(q_counttriples):
            ct = res[0]
            
        out_string = "KB Stats:\n- Triples: %s" % ct
        print out_string

        return out_string
