import http.client
import json
puerto=8001
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)
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

##class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
##  def do_GET(self):
##      self.send_response(200)
##      self.send_header("content-type","text/html")
##      self.end_headers()
##      cuerpo="<html><body>"
##      for fabri in todos:
##          cuerpo+=fabricante+"<br>"
##          cuerpo+="</body></html>"
##          self.wfile.write(bytes(cuerpo,"utf8"))
##          return


##handler=testHTTPRequestHandler
##HTTPD= socketserver.TCPserver(("",puerto),handler)
##try:
##  print("servidor activado...")
##  HTTPD.serve_forever()
## except KeyboardInterrupt:
##  print("servidor cerrado")
##  HTTPD.server_close()