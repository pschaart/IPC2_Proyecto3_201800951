import os
import re
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask_restful import Resource, Api
import xml.etree.ElementTree as ET

class Evento():
    def __init__(self):
        self.Fecha = []
        self.Usuario = None
        self.Afectado = []
        self.Error = None

class Estadistica():
    def __init__(self):
        self.Fecha = []
        self.Usuario = []
        self.Afectado = []
        self.Error = []
        self.CantMens = 0
class Usuario():
    def __init__(self,Correo):
        self.Correo = Correo
        self.CantMens = 0
class Error():
    def __init__(self,Codigo,Detalles):
        self.Codigo = Codigo
        self.Detalle = Detalles
        self.CantMens = 0

def leerArchivo(arch):
    Eventos = []
    t = open(arch)
    temp = []
    for linea in t.readlines():
        if '<EVENTOS>'in linea or '</EVENTOs>' in linea:
            continue
        elif '<EVENTO>' in linea:
            temp.append(Evento())
        elif 'Guatemala' in linea:
            lineadiv = linea.split('Guatemala')
            cons = re.search('[0-9]{2}\/[0-9]{2}\/[0-9]{4}', lineadiv[1])
            if cons:
                temp[0].Fecha.append(cons.string)
            else:
                temp.pop()
        elif 'Reportado por:' in linea:
            if temp != []:
                lineadiv = linea.split('Reportado por:')
                cons = re.search('[^ ]{1,}\@ing\.usac\.edu\.gt', lineadiv[1])
                if cons:
                    temp[0].Usuario = Usuario(cons)
                else:
                    temp.pop()
        elif 'Usuarios afectados:' in linea:
            if temp != []:
                lineadiv = linea.split('Usuarios afectados:')
                lineadiv[0] = lineadiv[1].split(',')
                for i in lineadiv[0]:
                    cons = re.search('[^ ]{1,}\@ing\.usac\.edu\.gt', i)
                    if cons:
                        temp[0].Afectado.append(cons.string)
                    else:
                        temp.pop()
        elif 'Error:' in linea:
            if temp != []:
                lineadiv = linea.split('Error:')
                lineadiv[1] = lineadiv[1].split('-')
                cons = re.search('[0-9]+', lineadiv[1][0])
                if cons:
                    temp[0].Error.Codigo(cons.string)
                    temp[0].Error.Detalle(lineadiv[1][1])
        elif '</EVENTO>' in linea:
            if temp != []:
                if temp[0].Fecha != [] and temp[0].Usuario != [] and temp[0].Afectado != [] and temp[0].Error != []:
                    Eventos.append(temp[0])
                    temp.pop()
            else:
                continue
    print('leido con exito')
    print('ordenando')
    Estadisticas = []
    for i in Eventos:
        if Estadisticas == []:
            est = Estadistica()
            est.Fecha.append(i.Fecha)
            est.Error.append(i.Error)
            est.Usuario.append(i.Usuario)
            for h in i.Afectado:
                est.Afectado.append(h)
            est.CantMens += 1
            Estadisticas.append(est)
        elif Estadisticas != []:
            eventoanal = False
            for s in Estadisticas:
                if i.Fecha == s.Fecha:
                    erroren = False
                    usuarioen = False
                    for l in s.Error:
                        if i.Error.Codigo == l.Error.Codigo:
                            l.CantMens += 1
                            s.CantMens += 1
                            erroren = True
                            break
                    if erroren == False:
                        s.Error.append(i.Error)
                    for k in s.Usuario:
                        if k.Correo == i.Usuario.Correo:
                            k.CantMens += 1
                            s.CantMens += 1
                            usuarioen = True
                            break
                    if usuarioen == False:
                        s.Usuario.append(i.Usuario)
                    for h in i.Afectado:
                        est.Afectado.append(h)
                    eventoanal = True
                    break
            if eventoanal == False:
                est = Estadistica()
                est.Fecha.append(i.Fecha)
                est.Error.append(i.Error)
                est.Usuario.append(i.Usuario)
                for h in i.Afectado:
                    est.Afectado.append(h)
                est.CantMens += 1
                Estadisticas.append(est)

    root = ET.Element("ESTADISTICAS")
    for g in Estadisticas:
        Estadisticah = ET.SubElement(root,'ESTADISTICA')
        ET.SubElement(Estadisticah,'Fecha').text = str(g.Fecha)
        ET.SubElement(Estadisticah,'CANTIDAD_MENSAJES').text = str(g.CantMens)
        reportadox = ET.SubElement(Estadisticah,'REPORTADO POR')
        for n in g.Usuario:
            usuarix = ET.SubElement(reportadox,'USUARIO')
            ET.SubElement(usuarix,'EMAIL').text = str(n.Correo)
            ET.SubElement(usuarix, 'CANTIDAD_MENSAJES').text = str(n.CantMens)
        Afectadosx = ET.SubElement(Estadisticah,'AFECTADOS')
        for n in g.Afectado:
            ET.SubElement(Afectadosx,'AFECTADO').text = str(n)
        erroresx = ET.SubElement(Estadisticah, 'ERRORES')
        for n in g.Error:
            errorx = ET.SubElement(erroresx,'ERROR')
            ET.SubElement(errorx, 'CODIGO').text = str(n.Codigo)
            ET.SubElement(errorx, 'CANTIDAD_MENSAJES').text = str(n.CantMens)

    arbol = ET.ElementTree(root)
    arbol.write("Estadistica.xml")




UPLOAD_FOLDER = 'Archivos Recibidos'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            leerArchivo(UPLOAD_FOLDER+'/'+ file.filename)
            return 'Cargado con exito'
    return

if __name__ == '__main__':
    app.run(debug=True)