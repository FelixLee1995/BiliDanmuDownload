import re
import json


def loads_jsonp(_jsonp):
    try:
        return re.match(".*?({.*}).*",_jsonp,re.S).group(1)
    except:
        raise ValueError('Invalid Input')


