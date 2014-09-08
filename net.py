import crypt
import json
import requests
from util import *


def action(action_id, body, encode_key):
    data = json.dumps({
        REQ_HEADER_TAG: {REQ_ID: action_id},
        REQ_BODY_TAG: {REQ_BODY: crypt.encode(body, encode_key)}
    }, separators=(',', ':'))

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'en',
        'User-Agent': 'android',
        'Content-Length': len(data),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Expect': '100-continue'
    }

    r = requests.post('http://iosv2.bravefrontier.gumi.sg/bf/gme/action.php',
                      headers=headers,
                      data=data)

    if r.status_code == 200:
        try:
            return crypt.decode(r.json()[REQ_BODY_TAG][REQ_BODY], encode_key)
        except:
            pass

    return None
