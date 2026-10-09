import os
import json
def total(values):
    result=0
    for v in values :
        result = result+v
    return result
def report(orders, region = None):
    if region == None:
        return total([o["value"] for o in orders])
    return total([o["value"] for o in orders if o["region"]==region])
