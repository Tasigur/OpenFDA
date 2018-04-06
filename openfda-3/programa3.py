import socketserver
import http.client
import json
import http.server
puerto=1801
headers = {'User-Agent': 'http-client'}
conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=11", None, headers)
r1 = conn.getresponse()
print(r1.status, r1.reason)
repos_raw = r1.read().decode("utf-8")
conn.close()
repos = json.loads(repos_raw)
a=len(repos["results"])#a es un número igual a la longitud del diccionario
todos=[]#lista vacía
for x in range(a):# para los valores númericos hasta a; llamamos resultados a los cosos en la posición correspondiente a x en "results"
    resultados=repos["results"][x]
    if resultados["openfda"]:#si existe un valor para resultados con clave "openfda" añadimos el valor con clave "manufacturer_name" a la lista originalmente vacía todos.
        todos.append(resultados["openfda"]["manufacturer_name"][0])
print(todos)#imrpimimos esa lista
print("A")
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type","text/html")
        self.end_headers()
        cuerpo="<html><body>"#creamos cuerpo (vacío) en html.
        for fabricante in todos:#para cada valor de la lista todos lo añadimos,pasándolo antes a html,a cuerpo.
            cuerpo+=fabricante+"<br>"
        cuerpo+="</body></html>"
        self.wfile.write(bytes(cuerpo,"utf8"))
        return


handler=testHTTPRequestHandler
HTTPD= socketserver.TCPServer(("",puerto),handler)
try:
    print("servidor abierto")
    HTTPD.serve_forever()
except KeyboardInterrupt:
    print("servidor cerrado")
    HTTPD.server_close()