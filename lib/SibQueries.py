#!/usr/bin/python

# global requirements
from smart_m3.m3_kp_api import *

# The following query is used to retrieve
# the whole content of the SIB
q_everything = Triple(None, None, None)

# The following query is used to retrieve
# the list of the classes defined into the SIB
q_classes = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#> 
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT DISTINCT ?class
WHERE {
  { ?resource rdf:type ?class }
  UNION 
  { ?class rdf:type owl:Class }
  UNION 
  { ?class rdf:type rdfs:Class }
}"""


# The following query is used to retrieve the list
# of all the data properties defined in the ontology
q_dproperties = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#> 
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT DISTINCT ?property
WHERE {
  { ?property rdf:type owl:DatatypeProperty }
  UNION 
  { ?property rdf:type rdfs:Datatype }
}"""

# The following query is used to retrieve the list
# of all the object properties defined in the ontology
q_oproperties = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#> 
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT DISTINCT ?property
WHERE {
  { ?property rdf:type owl:ObjectProperty }
  UNION 
  { ?property rdf:type rdfs:Datatype }
}"""

# Count all the triples
q_counttriples = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT (COUNT(*) AS ?no) { ?s ?p ?o  }
"""

# Count all instances of classes
q_countinstances = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT  ?class (COUNT(?s) AS ?count ) { ?s a ?class } GROUP BY ?class ORDER BY ?count"""
