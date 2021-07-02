from time import time
from flask import request, Response
from json import dumps

QUERY_URL = "https://api.wolframalpha.com/v2/query?appid={appID}&input={input}&podstate=Step-by-step+solution&podstate=Step-by-step&podstate=Show+all+steps&scantimeout={timeout}"
AUTOCOMPLETE_URL = "https://www.wolframalpha.com/n/v1/api/autocomplete/?i={input}"

APPIDS = [
    '26LQEH-YT3P6T3YY9',
    'K49A6Y-4REWHGRWW6',
    'J77PG9-UY8A3WQ2PG',
    'P3WLYY-2G9GA6RQGE',
    'P7JH3K-27RHWR53JQ',
    'L349HV-29P5JV8Y7J',
    '77PP56-XLQK5GKUAA',
    '59EQ3X-HE26TY2W64',
    '8Q68TL-QA8W9GEXAA',
    'KQRKKJ-8WHPY395HA',
    'AAT4HU-Q3RETTGY93',
    '7JKH84-T648HW2UV9',
    'WYEQU3-2T55JP3WUG',
    'T2XT8W-57PJW3L433',
    '2557YT-52JEY65G9K',
]

def get_app_id():
    return APPIDS[int((time() * 1000) % len(APPIDS))]

def makeResponse(data=None, error=None, code=200, cache_hit=False):
    """
    Shapes the response
    """
    responseBody = {"success": error is None, "error": error, "data": data}

    if "minify" in request.values:
        response = Response(dumps(responseBody, ensure_ascii=False, separators=(",", ":")))
    else:
        response = Response(dumps(responseBody, ensure_ascii=False, indent=4))
    
    response.headers["Server"] = "Anise"
    response.headers["Content-Type"] = "application/json"
    if cache_hit:
        response.headers["X-ANISE-CACHE"] = "HIT"
    else:
        response.headers["X-ANISE-CACHE"] = "MISS"
    response.status_code = int(code)
    return response
