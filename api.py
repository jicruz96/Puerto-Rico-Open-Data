#!/usr/bin/python3

from requests import get
from urllib.parse import urlencode
from json import dump
import csv

# Shit for automating the query
# See https://dev.socrata.com/docs/queries/ for more on queries

# api_url = "https://data.pr.gov/resource/{resource}?{params}"
# resource = "gb92-58gc.json"
# param_dict = {
#     "$select": "*",
#     "$where": None,
#     "$order": None,
#     "$group": None,
#     "$having": None,
#     "$limit": 50000,
#     "$offset": 0,
#     "$q": None,
#     "$query": None,
#     "$$bom": None
# }

# param_dict = {x: param_dict[x] for x in param_dict if param_dict[x] != None}
# params = urlencode(param_dict, safe='$')
# url = api_url.format(resource=resource, params=params)

url = "http://api.us.socrata.com/api/catalog/v1?domains=data.pr.gov&limit=9999"
results = get(url).json().get('results')
results = {result['resource']['name']: result['resource']['id']
           for result in results}


with open('failures.csv', 'w') as failfile:

    for name, id in results.items():
        try:
            url = "https://data.pr.gov/resource/{}.csv".format(id)
            name = name.replace(" ", "_").lower()
            response = get(url).text
            with open('{}.csv'.format(name), 'w') as file:
                file.write(response)
        except:
            failfile.write(name + ", " + id)
            print(name + " FAILED")


# response = get(url).json()
# """
# response is a dictionary with three entries:
#     - 'timings' : dictionary with response runtime info
#     - 'resultSetSize' : size of result set
#     - 'results' : result set
# """
# results = response['results']
# """
# Each result in the results set contains the following attributes:

#     - owner: dictionary with owner info
#     - classification: dictionary with classification info
#     - permalink: permalink
#     - metadata: metadata dictionary
#     - link: link
#     - resource: resource dictionary
# """


#     for key, value in result.items():
#         print(key + ': ', end='')
#         if isinstance(value, str):
#             print('"' + value + '"')
#         elif key == "resource":
#             print()
#             for rkey, rval in value.items():
#                 print("\t" + rkey + ": " + str(rval))
#             print()
#         else:
#             print(type(value))
#     print()

# Write CSV
# with open('test.csv', 'w', newline='') as csv_file:

#     fields = list(results[0]['resource'].keys()) + list(results[0].keys())
#     writer = csv.DictWriter(csv_file, fieldnames=fields, quoting=csv.QUOTE_ALL)
#     writer.writeheader()
#     final = []
#     for result in results:
#         new_stuff = {}
#         for key, value in result.items():
#             new_stuff[key] = value
#         result['resource'].update(new_stuff)
#     results = [result['resource'] for result in results]
#     writer.writerows(results)
