import requests
import lxml.html
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-n", "--nombre", required=False,help="Nombre de la persona")
ap.add_argument("-p", "--paterno", required=False,help="Apellido Paterno de la persona")
ap.add_argument("-m", "--materno", required=False,help="Apellido Materno de la persona")
args = vars(ap.parse_args())

nom=args["nombre"];apep=args["paterno"];apem=args["materno"]
if nom=="" :nom="%%"
if apep=="" :apep="%%"
if apem=="" :apem="%%"

if __name__ == '__main__':
    url = 'https://eldni.com/pe/buscar-por-nombres'
    args = {'nombres':nom, 'apellido_p':apep, 'apellido_m':apem}
    response=requests.get(url, args)

    if response.status_code==200:
        doc = lxml.html.fromstring(response.content)
        try:
            resultado=doc.xpath('//h4[@class="text-center"]/mark/text()')
            if len(resultado)==0:
                resultado=doc.xpath('//h4[@class="text-center"]/text()')
                if resultado[0] == "Se encontraton más de 30 personas, haz una búsqueda más exacta para encontrar lo que deseas.":
                    res=30
            else:
                res=int(resultado[0])

            datos = doc.xpath('//tbody/tr/td/text()')
            documento = doc.xpath('//tbody/tr/th/text()')
            dni=[]
            for i in documento:
                if len(i)==8:
                    dni.append(i)
            n=0;p=1;m=2
            nombres = [];apellido_p = [];apellido_m = []
            while(n<(3*res)):
                nombres.append(datos[n])
                n=n+3

            while (p < (3 * res)):
                apellido_p.append(datos[p])
                p = p + 3

            while (m < (3 * res)):
                apellido_m.append(datos[m])
                m = m + 3

            if res > 1 and res<=29 :
                print("Se encontraron ",res," resultados")
            elif res==30:
                print("Se encontraron más de 30 personas, haz una búsqueda más exacta para encontrar lo que deseas")
            else:
                print("Se encontró ", res, " resultado")
            for i in range(res):
                print(dni[i],nombres[i],apellido_p[i],apellido_m[i])
        except:
            print("No hay resultados")