#!/usr/bin/python3

from __future__ import print_function

import os
import sys
import requests
import json
import pprint

# def jprint(obj):
#     # create a formatted string of the Python JSON object
#     text = json.dumps(obj, sort_keys=True, indent=4)
#     print(text)

#jprint(response.json())
#jobject(response.json())
class PartClass():
    def __init__(self, partname, qty):
        self.partname = partname
        self.qty = qty

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def ReadFile():
    array_parts = []
    f = open("mouser_items_to_add.txt", "r")
    for x in f:
        _part = x.strip("\n").split(" ")
        part = PartClass("","")
        part.partname = _part[0]
        part.qty = int(_part[1])
        array_parts.append(part)
    return array_parts
    f.close()

def SearchPart(part):
    API_KEY = "97463f63-1d87-497e-8067-1524f6cc016b"


    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    params = (
        ('apiKey', API_KEY),
    )


    data = '{ "SearchByPartRequest": { "mouserPartNumber": "%s", "partSearchOptions": "string" }}' % str(part)


    response = requests.post('https://api.mouser.com/api/v1/search/partnumber', headers=headers, params=params, data=data)

    binary = response.content

    output = json.loads(binary)

    return output


#print(output['Errors'])

#pprint.pprint(SearchPart(part))


array_parts = ReadFile()

for i in array_parts:
    results = SearchPart(i.partname)
    results = results['SearchResults']
    results = results['Parts'][0]
    price_breaks = results['PriceBreaks']


    for k in range(len(price_breaks)):

        if k < len(price_breaks)-1:
            this = price_breaks[k]
            next = price_breaks[k+1]

            if (i.qty >= this['Quantity']) and (i.qty < next['Quantity']):
                print('part: {} qty: {} qtybreak: {} price: {}'.format(
                    i.partname, i.qty, this['Quantity'], this['Price']))
            if (i.qty >= next['Quantity']) and (i.qty < next['Quantity']):
                print('part: {} qty: {} qtybreak: {} price: {}'.format(
                    i.partname, i.qty, next['Quantity'], next['Price']))
        else:
            pass

        if len(price_breaks) == 1:
            this = price_breaks[k]
            print('part: {} qty: {} qtybreak: {} price: {}'.format(
                i.partname, i.qty, this['Quantity'], this['Price']))
        else:
            pass
