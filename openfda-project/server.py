import http.server
import http.client
import json
import socketserver

PORT = 8000#puerto
headers = {'User-Agent': 'http-client'}


class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def principio(self):#Definimos la página principall
        principal = """
                    <html>
                        <head>
                        Pagina Principal
                        <head>
                        <style>
                        body {
                            background-color: coral;
                        }
                        </style>
                        <body>
                            <form action="listDrugs">
                                <input type = "submit" value="listDrugs"> 
                               ("A")
                                </input>
                            </form>
                            <form action="listCompanies">
                                <input type = "submit" value="listCompanies">
                                ("B")
                                </input>
                            </form>
                            <form action="searchDrug">
                                Active ingredient:
                                <input type = "text" name="active_ingredient">
                               ("C")
                                </input>
                            </form>
                            <form action="searchCompany">
                                Manufacturer name:
                                <input type = "text" name="manufacturer_name">
                                ("D")
                                </input>
                            </form>
                            <form action="listWarnings">
                                <input type = "submit" value="listWarnings"> 
                               ("E")
                                </input>
                            

                        </body>
                    </html>
                        """
        return principal

    # Ponemos un input del tipo submit con el cuál aparecerá un "botón" con un nombre asignado.
    #Otro input del tipo text con el que tendremos un hueco en blanco donde poder escribir
    def listas(self, lista):
        list_html = """
                                <html>
                                    <style>
                                        body {
                                            background-color: purple;
                                        }
                                    </style>
                                    <body>
                                        <ul style="list-style-type:none">

                            """
        for x in lista:
            list_html += "<li>" + x + "</li>"
        list_html += """
                                        </ul style="list-style-type:none">
                                    </body>
                                </html>
                            """
        return list_html
    #En esta función definimos la estructura que tendrán las listas de más adelante.
    #El principio de la lista lo definimos en list_html con <ul. Usamos el bucle for para añadir cada miembro de la lista a la lista en html.Y por último cerramos con </ul>
    def do_GET(self):
        recurso_list = self.path.split("?")
        if len(recurso_list) > 1:
            params = recurso_list[1]
        else:
            params = ""
        limit = 10

        # Obtener los parametros
        if params:
            parse_limit = params.split("=")
            if parse_limit[0] == "limit":
                limit = int(parse_limit[1])
                print("Limit: {}".format(limit))
        else:
            print("SIN PARAMETROS")
        if self.path == '/':#si usamos "/" nos llevará a la pagina principal ya definda en def principio(self).
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            respuesta = self.principio()
            self.wfile.write(bytes(respuesta, "utf8"))
        elif 'listDrugs' in self.path:#si usamos "listDrugs" se imprimirá por pantalla la lista que creamos con los datos que sacamos de api.fda....
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            conn = http.client.HTTPSConnection("api.fda.gov")#Creamos conexión con la página fda.
            conn.request("GET", "/drug/label.json?limit=10", None, headers)#Petición tipo get
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf8")
            repos = json.loads(repos_raw)
            resultados = repos['results']
            listDrugs = []#lista vacía
            for resultado in resultados:#Para cada elemento proveniente de "results" , si este tiene un valor para la key 'generic_name' añadimos este valor a la lista.
                if 'generic_name' in resultado['openfda']:
                    listDrugs.append(resultado['openfda']['generic_name'][0])
            listaHTML = self.listas(listDrugs)#Usamos la función de las listas para pasar esta lista recién creada a HTML.
            self.wfile.write(bytes(listaHTML, "utf8"))
        elif 'listCompanies' in self.path:#Para listCompanies el procedimiento es el mismo.Pero en el bucle for si noe existe el valor correspondiente a la key, se añade "Desconocida" a la lista.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=10", None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf8")
            repos = json.loads(repos_raw)
            resultados = repos['results']
            listCompanies = []
            for resultado in resultados:
                if 'manufacturer_name' in resultado['openfda']:
                    listCompanies.append(resultado['openfda']['manufacturer_name'][0])
                else:
                    listCompanies.append("Desconocida")
            listaHTML = self.listas(listCompanies)
            self.wfile.write(bytes(listaHTML, "utf8"))
        elif "searchDrug" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            drug = self.path.split('=')[1]
            drugs = []
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=10&search=active_ingredient:" + drug)#Ahora se realiza una petición de búsqueda para active_ingredient y una "drug" concreta.
            r1 = conn.getresponse()#Recorremos la información y añadimos el "generic_name" de aquellos que active_ingredient se corresponde con drug.
            repos_raw = r1.read()
            repos = repos_raw.decode("utf8")
            completo = json.loads(repos)
            results = completo["results"]
            for z in results:
                if 'generic_name' in z['openfda']:
                    drugs.append(z['openfda']['generic_name'][0])
                else:
                    drugs.append('Desconocido')
            listaHTML = self.listas(drugs)
            self.wfile.write(bytes(listaHTML, "utf8"))
        elif 'searchCompany' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            company = self.path.split('=')[1]
            companies = []
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=10&search=openfda.manufacturer_name:" + company)
            r1 = conn.getresponse()
            repos_raw = r1.read()
            repos = repos_raw.decode("utf8")
            completo = json.loads(repos)
            results = completo["results"]
            for z in results:
                companies.append(z['openfda']['manufacturer_name'][0])
            listaHTML = self.listas(companies)
            self.wfile.write(bytes(listaHTML, "utf8"))
        elif 'listWarnings' in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            conn = http.client.HTTPSConnection("api.fda.gov")
            conn.request("GET", "/drug/label.json?limit=10", None, headers)
            r1 = conn.getresponse()
            repos_raw = r1.read().decode("utf8")
            repos = json.loads(repos_raw)
            resultados = repos['results']
            listWarnings=[]
            for resultado in resultados:
                if 'warnings' in resultado:
                    listWarnings.append(resultado['warnings'][0])
                else:
                    listWarnings.append("Desconocida")
            listaHTML = self.listas(listWarnings)
            self.wfile.write(bytes(listaHTML, "utf8"))
        elif '/redirect' in self.path:#Nos devuelve a la página principal.
            self.send_response(302)
            self.send_header('Location','http://127.0.0.1:8000')
            self.end_headers()
        elif '/secret' in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Secure Area"')
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("Prueba escribiendo bien el recurso '{}'.".format(self.path).encode())

        return
socketserver.TCPServer.allow_reuse_address = True
handler = testHTTPRequestHandler
HTTPD = socketserver.TCPServer(("", PORT), handler)
print("Activado puerto:",PORT)
HTTPD.serve_forever()
