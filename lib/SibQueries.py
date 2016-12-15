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

# The following query is used to retrieve alle the instances
q_instances = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#> 
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT DISTINCT ?instance
WHERE {
  ?instance rdf:type ?something
}"""

q_instances_of_class = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#> 
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT ?instance
WHERE {
  ?instance rdf:type <%s>
}"""

# The following query is used to retrieve the list
# of all the data properties defined in the ontology
q_dproperties = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#> 
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT DISTINCT ?property ?domain ?range
WHERE {
  { ?property rdf:type owl:DatatypeProperty .
    OPTIONAL { ?property rdfs:range ?range } .
    OPTIONAL { ?property rdfs:domain ?domain }
   }
  UNION 
  { ?property rdf:type rdfs:Datatype .
    OPTIONAL { ?property rdfs:range ?range } .
    OPTIONAL { ?property rdfs:domain ?domain }
  }
}"""

# The following query is used to retrieve the list
# of all the object properties defined in the ontology
q_oproperties = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#> 
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT DISTINCT ?property ?domain ?range
WHERE {
  { ?property rdf:type owl:ObjectProperty .
    OPTIONAL { ?property rdfs:range ?range } .
    OPTIONAL { ?property rdfs:domain ?domain }
   }
  UNION 
  { ?property rdf:type rdfs:Datatype .
    OPTIONAL { ?property rdfs:range ?range } .
    OPTIONAL { ?property rdfs:domain ?domain }
  }
}"""

# Count all the triples
q_counttriples = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT (COUNT(*) AS ?no) { ?s ?p ?o  }
"""
