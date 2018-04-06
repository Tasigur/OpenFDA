import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
for x in range(10):
    a=x+1
    print(a)
    try:
        print("ID:",repos["results"][x]["id"])
    except Exception:
        print("Not found")
    try:
        print("Fabricante:",repos["results"][x]["openfda"]["manufacturer_name"][0])
    except Exception:
        print("Not found")
    try:
        print("Propósito:",repos["results"][x]["purpose"][0])
    except Exception:
        print("Not found")
    continue
#para cada valor hasta el 10, tratamos de imprimir el valor deseado proveniente de los diccionarios a través de los cuales buscamos.