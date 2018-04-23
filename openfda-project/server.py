from flask import Flask
from flask import jsonify
from flask import request
import socketserver
import http.client
import json
import http.server
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=11", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
repos = json.loads(repos_raw)
a=len(repos["results"])
todos=[]
for x in range(a):
    resultados=repos["results"][x]
    if resultados["openfda"]:
        todos.append(resultados["openfda"]["manufacturer_name"][0])
print(todos)
app = Flask(__name__)
x="XXXXXXXXXXXXXXXXXXXXXXXXXXx"


@app.route('/empdb',methods=['GET'])
def getAllEmp():
    return (x)
@app.route('/empdb/<empId>',methods=['GET'])
def getEmp(empId):
    usr = [ emp for emp in empDB if (emp['id'] == empId) ]
    return jsonify({'emp':usr})
app.run(host='0.0.0.0',port=1234)