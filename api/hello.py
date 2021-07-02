# Imports

## Flask Management
from flask import Flask, request
from flask_compress import Compress
from flask_cors import CORS

## Initialization
app = Flask(__name__) # Flask
Compress(app) # Compressing the responses
CORS(app) # Enabling CORS globally

## Other Imports
from time import time
from traceback import print_exc
from constants import makeResponse

## Variable Initialization
LOCAL_CACHE = {} # store variable
CACHE_DURATION = 3 # in sec.

# Route Defining
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello(path):
    try:
        ## if the name of the file is in the following schema: [parameter].py
        # parameter = path[path.rfind("/") + 1:]

        # Cache Management

        ## Cache Key Defining
        _values_dict = request.values.to_dict()
        _values_dict.pop("_invalidate_cache", None)
        cache_key = str(_values_dict) + str(request.method)

        ## Cache Invalidation Management
        if "_invalidate_cache" in request.values:
            LOCAL_CACHE.pop(cache_key, None)
            return "Ok"
        
        ## Cache Lookup
        try:
            if cache_key in LOCAL_CACHE:
                cache_duration = time() - LOCAL_CACHE[cache_key]["timestamp"]
                if cache_duration > CACHE_DURATION:
                    LOCAL_CACHE.pop(cache_key, None)
                else:
                    return makeResponse(data=LOCAL_CACHE[cache_key]["data"], cache_hit=True)
        except:
            print_exc()
            print("[CACHE] An error occured while sending back the cached data")
            print("[FAILURE_RECOVERING] Processing the request as if nothing was cached")




        # Processing and Computation
        result = None # the result should in this variable




        # Caching and Response
        LOCAL_CACHE[cache_key] = {"timestamp": time(), "data": result}
        return makeResponse(result, cache_hit=False)
    except:
        print_exc()
        print("[ERROR] An unknown error occured on the server and nothing could handle it. Sending back SERVER_ERROR (Status Code: 500)")
        return makeResponse({"message": "An error occured on the server"}, error="SERVER_ERROR", code=500)
