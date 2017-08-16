#!/usr/bin/python

from smart_m3.m3_kp_api import *

# constants
SIB_HOST = "localhost"
SIB_PORT = 7701

# namespaces
rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
ns = "http://ns#"

# connect to the sib
kp = m3_kp_api(False, SIB_HOST, SIB_PORT)

# clean it
kp.load_rdf_remove(Triple(None, None, None))

# generate triple list
triple_list = []
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(rdf + "type"), URI(ns + "Person")))
triple_list.append(Triple(URI(ns + "Person2_URI"), URI(rdf + "type"), URI(ns + "Person")))
triple_list.append(Triple(URI(ns + "Person3_URI"), URI(rdf + "type"), URI(ns + "Person")))
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(ns + "hasName"), Literal("Fabio")))
triple_list.append(Triple(URI(ns + "Person2_URI"), URI(ns + "hasName"), Literal("Alfredo")))
triple_list.append(Triple(URI(ns + "Person3_URI"), URI(ns + "hasName"), Literal("Tullio")))
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(ns + "hasAge"), Literal("30")))
triple_list.append(Triple(URI(ns + "Person2_URI"), URI(ns + "hasAge"), Literal("35")))
triple_list.append(Triple(URI(ns + "Person3_URI"), URI(ns + "hasAge"), Literal("66")))
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(ns + "hasFriend"), URI(ns + "Person2_URI")))
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(ns + "hasFriend"), URI(ns + "Person3_URI")))
triple_list.append(Triple(URI(ns + "Person2_URI"), URI(ns + "hasFriend"), URI(ns + "Person1_URI")))
triple_list.append(Triple(URI(ns + "Person3_URI"), URI(ns + "hasFriend"), URI(ns + "Person1_URI")))
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(ns + "hasChief"), URI(ns + "Person3_URI")))
triple_list.append(Triple(URI(ns + "Person2_URI"), URI(ns + "hasChief"), URI(ns + "Person3_URI")))
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(ns + "hasGender"), Literal("Male")))
triple_list.append(Triple(URI(ns + "Person2_URI"), URI(ns + "hasGender"), Literal("Male")))
triple_list.append(Triple(URI(ns + "Person3_URI"), URI(ns + "hasGender"), Literal("Male")))
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(ns + "hasNickname"), Literal("desmovalvo")))
triple_list.append(Triple(URI(ns + "Person2_URI"), URI(ns + "hasNickname"), Literal("elfo81")))
triple_list.append(Triple(URI(ns + "Person3_URI"), URI(ns + "hasNickname"), Literal("tullios")))
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(ns + "hasFullname"), Literal("Fabio Viola")))
triple_list.append(Triple(URI(ns + "Person2_URI"), URI(ns + "hasFullname"), Literal("Alfredo D'Elia")))
triple_list.append(Triple(URI(ns + "Person3_URI"), URI(ns + "hasFullname"), Literal("Tullio Salmon")))
triple_list.append(Triple(URI(ns + "Interoperability_URI"), URI(rdf + "type"), URI(ns + "Course")))
triple_list.append(Triple(URI(ns + "Person1_URI"), URI(ns + "hasCourse"), URI(ns + "Person")))
triple_list.append(Triple(URI(ns + "Person2_URI"), URI(ns + "hasCourse"), URI(ns + "Person")))


# put data into the SIB
kp.load_rdf_insert(triple_list)
