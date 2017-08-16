#!/usr/bin/python

# requirements
import requests
import json


class SepaKP:

    def __init__(self, queryURI):

        # store attributes
        self.queryURI = queryURI


    def consume(self, queryText):

        # do the request
        headers = {"Content-Type":"application/sparql-query", "Accept":"application/json"}
        r = requests.post(self.queryURI, headers = headers, data = queryText)
        r.connection.close()
        results = r.text

        # parse results
        jresults = json.loads(results)
        return jresults
