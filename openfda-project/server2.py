import http.client
import json

headers = {'User-Agent': 'http-client'}
name=input("Ingrediente activo")

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?search=active_ingredient=<name>?limit=11", None, headers)

r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

print(name)
company_name=input("Nombre de la compañia")
conn.request("GET", "/drug/label.json?search=manufacturer_name=<company_name>?limit=11", None, headers)
print(company_name)
a=len(repos["results"])
listDrugs=[]
############
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)
ID=repos["results"][0]["id"]
purpose=repos["results"][0]["purpose"][0]
manufacturer=repos["results"][0]["openfda"]["manufacturer_name"][0]#cada variable impresa es el valor asignado a la clave correspondiente.
print("ID:",ID)
print("purpose:",purpose)
print("manufacturer:",manufacturer)
