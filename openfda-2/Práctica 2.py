print("Parte 1:")
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=active_ingredient:acetylsalicylic", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
a=len(repos["results"])
try:
    for x in range(a):
        print(repos["results"][x]["openfda"]["manufacturer_name"][0])
except KeyError:
    print("Not found")

print("Parte 2:")
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=substance_name:aspirin&limit=100", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
b=len(repos["results"])
try:
    for x in range(b):
        print(repos["results"][x]["openfda"]["manufacturer_name"][0])
except KeyError:
    print("Not found")