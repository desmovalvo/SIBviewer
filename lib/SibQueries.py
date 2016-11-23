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
