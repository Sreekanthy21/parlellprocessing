#!/usr/bin/env python
"""
API Testing.

@Author : Sreekanth Yekabathula

Contact : sreekanthy21@gmail.com
"""

import datetime
import urllib2
import json
import sys


def request(url, params):
    """
        Method to perform http call and return response back.
    """
    handler = urllib2.HTTPHandler()

    opener = urllib2.build_opener(handler)

    request = urllib2.Request(url, data=params )

    request.add_header("Content-Type",'application/json')

    request.get_method = lambda: "POST"

    # try it; catch the result
    try:
        connection = opener.open(request)
    except urllib2.HTTPError,e:
        connection = e

    #Response Status Check.
    if connection.code == 200:

        #If the response is already in json format, 
        #we can exclude this conversion
        result = json.loads(connection.read())

        return {"status": "success", "Error": 0, "result": result,
                "message": ""}

    else:
        return {"status": "error", "Error": connection.code,
                "message": connection.msg, "result": ""}


#===================================================================#
#               Main Method Starts Here                             #
#===================================================================#

def main():

    #I've used current timestamp here, we can change as required.
    params, url = {}, ""

    #Assigning parameters manually, we can also make this as dynamic
    params = {"sample": "sample"}
    if not url:
        print "Empty URL given, Try again by modifying url, parameters..."
        sys.exit(1)

    result = request(url, params)


if __name__ == "__main__":
    main()
