#!/usr/bin/python

# global requirements
import pdb
import rdflib
# from pymantic import sparql
from smart_m3.m3_kp_api import *

# local requirements
from SibQueries import *
import SEPA_kp_api 

# the KP
class SibInteractor:

    """This class constitutes the KP"""
    
    def __init__(self, host, port, owl_files, n3_files, blazehost):

        """Constructor for the SibInteractor"""

        # setting class attributes
        self.host = host
        try:
            self.port = int(port)
        except:
            self.port = None
        self.owl_files = owl_files    
        self.n3_files = n3_files
        self.local_storage = None
        self.blazehost = blazehost

        # initialize a local graph
        self.local_storage = rdflib.Graph()


    def load_owl(self):

        """Load an OWL file"""
                
        for owl_file in self.owl_files.split(":"):

            # parse the owl file
            g = rdflib.Graph()
            try:
                g.parse(owl_file, format='xml')
            except Exception as e:
                raise rdflib.OWLException("Parsing failed!")
        
            # add data to the local storage
            self.local_storage += g


    def load_n3(self):

        """Load an n3 file"""
                
        for n3_file in self.n3_files.split(":"):
        
            # parse the owl file
            g = rdflib.Graph()
            try:
                g.parse(n3_file, format='n3')
            except Exception as e:
                raise rdflib.OWLException("Parsing failed!")

            # add data to the local storage
            self.local_storage += g


    def get_classes(self):

        """Method that returns the list of the rdf/owl/implicit classes"""

        # retrieve data
        classes = self.local_storage.query(q_classes)

        # return data
        return classes


    def get_statements(self):

        """Method that returns the list of the rdf/owl/implicit classes"""

        # retrieve data
        statements = self.local_storage.query(q_statements)

        # return data
        return statements


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


    def get_everything_blaze(self):

        """Method used to retrieve all the knowledge base
        from a blazegraph dataset"""

        # initialize and fill the local storage
        self.local_storage = rdflib.Graph()
        
        #server = sparql.SPARQLServer(self.blazehost)
        #results = server.query(q_everything_sparql)

        server = SepaKP(self.blazehost)
        results = server.consume(q_everything_sparql)        
        
        for res in results["results"]["bindings"]:        

            # analyze the subject  
            s = res["s"]["value"]
            if res["s"]["type"] == "uri":
                ss = rdflib.URIRef(str(s))
            else:
                ss = rdflib.BNode(str(s))

            # predicate
            pp = rdflib.URIRef(str(res["p"]["value"]))

            # analyze the object        
            o = res["o"]["value"]
            if res["o"]["type"] == "uri":
                oo = rdflib.URIRef(str(o))
            else:
                oo = rdflib.Literal(str(o))

            print res
            try:
                self.local_storage.add((ss, pp, oo))
            except:
                pdb.set_trace()
                                

    def get_everything(self):

        """Method to retrieve the entire knowledge base"""

        # join SIB
        self.kp = m3_kp_api(False, self.host, self.port)

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


    def custom_multilevel_query(self, q):

        """Method to perform a custom query and return a multiple list of URIs"""

        uri_list = []
        self.kp.load_query_sparql(q)

        # iterate over the bindings
        for binding in self.kp.result_sparql_query:

            # iterate over the fields of each binding
            for variable in binding:

                # get index
                ind = binding.index(variable)

                # see if the uri_list already contains
                # a list for that level
                try:

                    if not(str(variable[2]) in uri_list[ind]):
                        uri_list[ind].append(str(variable[2]))

                except IndexError:

                    uri_list.append([])
                    if not(str(variable[2]) in uri_list[ind]):
                        uri_list[ind].append(str(variable[2]))

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

    
    def get_statement_els(self, statement):

        """Retrieves fields of a statement"""

        res = self.local_storage.query(q_statement_fields % (statement, statement, statement, statement))
        for r in res:
            s,p,o = r
            break
        return s,p,o
        

    def get_all_comments(self):

        """Retrieves all the comments"""
        
        comments = []
        res = self.local_storage.query(q_comments)
        for r in res:
            comments.append([r[0], r[1]])
        return comments
        

    def get_all_labels(self):

        """Retrieves all the labels"""
        
        labels = []
        res = self.local_storage.query(q_labels)
        for r in res:
            labels.append([r[0], r[1]])
        return labels
