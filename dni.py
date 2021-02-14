import requests
from lxml import html
import pandas as pd
import re
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--nombre", required=False,help="Nombre de la persona")
ap.add_argument("-p", "--paterno", required=False,help="Apellido Paterno de la persona")
ap.add_argument("-m", "--materno", required=False,help="Apellido Materno de la persona")
args = vars(ap.parse_args())

nom = args["nombre"]; apep = args["paterno"]; apem = args["materno"]

if nom == None:
    nom = "%%"

url = 'https://eldni.com/pe/buscar-por-nombres'
headers = {
    "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 13310.93.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.133 Safari/537.36"
}

session = requests.session()
front = session.get(url)
csrf_token = re.findall(r'<input type="hidden" name="_token" value="(.*)"', front.text)[0]
cookies = session.cookies

data = {
    "nombres": nom, "apellido_p": apep, "apellido_m": apem, '_token': csrf_token
}
response = requests.post(url=url, data=data, headers=headers, cookies=cookies)
lista = []

if not(nom == "%%" and apep == None and apem == None):
    if response.status_code == 200:
        doc = html.fromstring(response.content)
        resultados = doc.xpath('//table[@class="table table-striped table-scroll"]')
        try:
            cont = int(doc.xpath('//h4/mark/text()')[0])
        except:
            cont = 30
            print("Se encontraron mas de 30 resultados")

        if cont>0:
            for resultado in resultados:
                dni = resultado.xpath('.//tbody/tr/th[not(@colspan)]/text()')
                nombre = resultado.xpath('.//tbody/tr/td[1]/text()')
                apellido_p = resultado.xpath('.//tbody/tr/td[2]/text()')
                apellido_m = resultado.xpath('.//tbody/tr/td[3]/text()')

            for i in range(cont):
                lista.append({
                    "dni": dni[i],
                    "nombre": nombre[i],
                    "apellido_p": apellido_p[i],
                    "apellido_m": apellido_m[i]
                })

            df = pd.DataFrame(lista)
            print(df)
        else:
            print("No se encontraron resultados")

else:
    ap.print_help()
