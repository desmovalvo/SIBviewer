#!/usr/bin/python

# global requirements
import socket
from uuid import uuid4
from rdflib import URIRef, Literal
from xml.etree.ElementTree import fromstring, Element, SubElement, Comment, tostring

# KPI
class KP:

    def __init__(self, host, port):

        """Constructor for the KP class"""

        # setting class attributes
        self.host = host
        self.port = int(port)
        self.node_id = str(uuid4())
        self.space_id = "X"
        self.transaction_id = 0


    def join(self):
        
        """Method to join the smart space"""                

        # build a message
        ssap_message = Element("SSAP_message")
        node_id = SubElement(ssap_message, "node_id")
        node_id.text = self.node_id
        space_id = SubElement(ssap_message, "space_id")
        space_id.text = self.space_id
        transaction_id = SubElement(ssap_message, "transaction_id")
        transaction_id.text = self.transaction_id
        message_type = SubElement(ssap_message, "message_type")
        message_type.text = "REQUEST"
        transaction_type = SubElement(ssap_message, "transaction_type")
        transaction_type.text = "JOIN"
        credentials = SubElement(ssap_message, 'parameter', {'name':'credentials'})
        credentials.text = "XXYYZZ"

        # send a message
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.host, self.port))
        s.send(tostring(ssap_message))    
        
        # wait for the reply
        reply = ""
        while 1:
            data = s.recv(4096)
            if not data:
                break
            else:
                reply = reply + data
        s.close()

        # parse the reply
        root = fromstring(reply)
        for child in root:
            tag = child.tag
            attrib = child.attrib
            text = child.text
            if attrib == {"name" : "status"}:
                if text.lower() == "m3:success":
                    return True
        return False


    def sparql_query(self, query):

        """Method to perform a SPARQL query"""

        # build a message
        ssap_message = Element("SSAP_message")
        node_id = SubElement(ssap_message, "node_id")
        node_id.text = self.node_id
        space_id = SubElement(ssap_message, "space_id")
        space_id.text = self.space_id
        transaction_id = SubElement(ssap_message, "transaction_id")
        transaction_id.text = self.transaction_id
        message_type = SubElement(ssap_message, "message_type")
        message_type.text = "REQUEST"
        transaction_type = SubElement(ssap_message, "transaction_type")
        transaction_type.text = "QUERY"
        querytype = SubElement(ssap_message, "parameter", {'name':'query'})
        querytype.text = "sparql"
        queryfield = SubElement(ssap_message, "parameter", {'name':'query'})
        queryfield.text = sanitized_query


# <SSAP_message>
# 	<node_id>d88e372f-fedd-47cc-a1a2-026ac4cac670-0d39999c-2bbd-4f77-b0b2-ea1c57bfb09a</node_id>
# 	<space_id>X</space_id>
# 	<transaction_type>QUERY</transaction_type>
# 	<message_type>REQUEST</message_type>
# 	<transaction_id>6</transaction_id>

# 	<parameter name = "type">sparql</parameter>
# 	<parameter name = "query">
# 		PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns#&gt;
# 		PREFIX owl: &lt;http://www.w3.org/2002/07/owl#&gt;
# 		PREFIX xsd: &lt;http://www.w3.org/2001/XMLSchema#&gt;
# 		PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema#&gt;
# 		PREFIX ns: &lt;http://smartM3Lab/Ontology.owl#&gt;
# 		SELECT ?s ?p ?o
# 		    WHERE { ?s ?p ?o }
# 	</parameter>
# </SSAP_message>

        # build a message
        # send a message
        # wait for the reply
        # parse the reply
        pass

if __name__ == "__main__":
    kp = KP("localhost", 10111)
    print kp.join()
