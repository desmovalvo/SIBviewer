#!/usr/bin/python

# global requirements
from smart_m3.m3_kp_api import *

# The following queries are used to retrieve
# the whole content of the SIB or blazegraph
q_everything = Triple(None, None, None)
q_everything_sparql = """SELECT ?s ?p ?o WHERE { ?s ?p ?o }"""

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

# The following query is used to retrieve all the instances
q_instances = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#> 
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT DISTINCT ?instance
WHERE {
  ?instance rdf:type ?something
}"""

# The following query is used to retrieve all the instances
# of the specified class
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
SELECT DISTINCT ?property ?domain ?range ?comment ?label
WHERE {
  { ?property rdf:type owl:DatatypeProperty .
    OPTIONAL { ?property rdfs:range ?range } .
    OPTIONAL { ?property rdfs:domain ?domain } .
    OPTIONAL { ?property rdfs:label ?label} . 
    OPTIONAL { ?property rdfs:comment ?comment}
  }
  UNION 
  { ?property rdf:type rdfs:Datatype .
    OPTIONAL { ?property rdfs:range ?range } .
    OPTIONAL { ?property rdfs:domain ?domain } .
    OPTIONAL { ?property rdfs:label ?label} . 
    OPTIONAL { ?property rdfs:comment ?comment}
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
    OPTIONAL { ?property rdfs:domain ?domain } .
    OPTIONAL { ?property rdfs:label ?label} . 
    OPTIONAL { ?property rdfs:comment ?comment}
   }
  UNION 
  { ?property rdf:type rdfs:Datatype .
    OPTIONAL { ?property rdfs:range ?range } .
    OPTIONAL { ?property rdfs:domain ?domain } .
    OPTIONAL { ?property rdfs:label ?label} . 
    OPTIONAL { ?property rdfs:comment ?comment}
  }
}"""

# Count all the triples
q_counttriples = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT (COUNT(*) AS ?no) { ?s ?p ?o  }
"""

# The following query is used to get all the subjects with a
# given datatype property
q_instances_with_dp = """PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl:<http://www.w3.org/2002/07/owl#> 
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT ?instance
WHERE {
  ?instance <%s> ?object
}"""

# The following query is for reification
q_reification = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?o ?p ?s
WHERE {
  ?t rdf:type rdf:Statement .
  ?t rdf:subject ?s .
  ?t rdf:predicate ?p .
  ?t rdf:object ?o 
}"""

# The following query retrieves all the statements
q_statements = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?st
WHERE {
  ?st rdf:type rdf:Statement 
}"""

# The following query is for reification
q_statement_fields = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?s ?p ?o
WHERE {
  <%s> rdf:type rdf:Statement .
  <%s> rdf:subject ?s .
  <%s> rdf:predicate ?p .
  <%s> rdf:object ?o 
}"""

# get all the comments
q_comments = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT ?r ?c
WHERE {
  ?r rdfs:comment ?c
}"""

# get all the labels
q_labels = """PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#> 
SELECT ?r ?l
WHERE {
  ?r rdfs:label ?l
}"""
