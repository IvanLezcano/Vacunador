from flask import Flask, render_template, request
from flask import request
import json
import pickle
import csv
import pandas as pd 
import openpyxl
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sqlite3

app = Flask(__name__)

miConexion=sqlite3.connect("PrimeraBase.db")
miCursor= miConexion.cursor()

#miCursor.execute("DROP TABLE PRODUCTOS")
#miCursor.execute("CREATE TABLE PACIENTES (NOMBRE_PACIENTE VARCHAR(50),DNI INTEGER, PRIORIDAD VARCHAR(20))")




#----------------------------------------------------------------------------------------------------------------------
#Listas

pacientes={}
lista_para_excel=[]
vdatos={}
pacientes={}
archivo={}

#----------------------------------------------------------------------------------------------------------------------
#centros
hospital_gandulfo=[]
hospital_piromano=[]
hospital_fernandez=[]
hospital_ninos=[]
hospital_general_paz=[]

centros=[hospital_gandulfo,hospital_piromano,hospital_fernandez,hospital_ninos,hospital_general_paz]
def guardar_centros():
    j = open("centros.txt", "w")

    j.write(str(centros))
    j.close()
#----------------------------------------------------------------------------------------------------------------------
#vacunas disponibles

lista_vacunas=[]

def guardar_vacunas():
    j = open("centros.txt", "w")

    j.write(centros)
    j.close()






#----------------------------------------------------------------------------------------------------------------------
#Objeto Vacunador







class Vacunador():
    def __init__(self, centros=[],hospital_gandulfo=[],hospital_fernandez=[],
hospital_ninos=[],
hospital_general_paz=[],
hospital_piromano=[],lista_vacunas=[],lista_personas=[]):
        self.cantidad=0
        self.centros=[hospital_gandulfo,hospital_piromano,hospital_fernandez,hospital_ninos,hospital_general_paz]
        
    def agregar_vacunas(self,cantidad):
        for i in range(1,int(cantidad)+1):
            vacunas="vacuna "+ str(i)
            lista_vacunas.append(vacunas)
        print(lista_vacunas)
    def distribuir_vacunas(self):
        while len(lista_vacunas)>0:        
            for centro in centros:            
                centro.append(lista_vacunas[0])
                lista_vacunas.pop(0)
                if len(lista_vacunas)<=0:
                    break
        

repartidor=Vacunador()
#----------------------------------------------------------------------------------------------------------------------
#Rutas


#ruta por defecto
@app.route("/")
def index():
    return render_template("zaraza.html")



@app.route("/formulario_de_vacunacion")
def saluda():
    return render_template("formulario_carga.html")

@app.route("/")
def retorno():
    return render_template("zaraza.html")


@app.route("/configuracion_centros_de_vacunacion",methods=["GET","POST"])
def prueba():
    return render_template("formulario_vacunas.html")
    


@app.route("/guardado",methods=["GET","POST"])
def configuracion_centros_de_vacunacion():
    cantidad_vacunas=request.form.get("caplicaciones")
    repartidor.agregar_vacunas(cantidad_vacunas)
    repartidor.distribuir_vacunas()
    print(hospital_ninos)

    return index()
 


@app.route("/calcular_asignacion_de_turnos")
def calcular_asignacion_de_turnos():
    return render_template("construccion.html")


@app.route("/listar_los_turnos_asignados")
def listar_los_turnos_asignados(methods=['GET', 'POST']):
    try:
        f = open( "personas.bin", "rb" )
        jjason = pickle.load( f )
    except:
        pass


    tabla = '<table style = "width:100%">'

    titulos = "<tr> <th> Nro. Documento </th> <th> Centro de Vacunación </th>  <th> Enfermedades </th> <th> Edad </th><th> Prioridad </th>"



    tabla2 = ''
    for e in jjason:
        try:
            tabla2 +='<tr> <td> ' + e + '</td> <td> ' + jjason[e][0] + '</td> <td> ' + ', '.join(jjason[e][1]) + '</td> <td> ' + str(jjason[e][2]) + '</td> </tr>'
        except:
            pass

    tabla3 = '</table>'
    tabla4 = tabla + titulos + tabla2 + tabla3
    return tabla4


@app.route("/listado")
def lista():
    l=open("Nombres.txt","r")
    lista=l.read()
    print(hospital_gandulfo)
    return lista

@app.route("/pagina_en_construccion")
def construccion():
    return render_template("construccion.html")
    

def guardar_archivo(n1,n2,n3,n4,n5,n6,n7,n8,n9):

    f = open("datos.txt", "a")

    f.write("Nombre :"+ n1 + "\n")
    f.write("Direccion :"+ n2 + "\n")
    f.write("Dni :"+ n3 + "\n")
    f.write("Fecha de naciomiento :"+ n4 + "\n")
    f.write("Sexo :"+ n5 + "\n")
    f.write("Cormobilidad :"+ n6 + "\n")
    f.write("Centro de atencion :"+ n7 + "\n")
    f.write("Email: "+n8 + "\n")
    f.write("Edad: "+str(n9)+ "\n" )

    f.close()
def guardar_nombres(d1):
    d= open("Nombres.txt","a")

    d.write("Nombre :"+ d1 + "<br>")

    d.close()

def guardar_txt_personal(n1,n2,n3,n4,n5,n6,n7,n8):
    c= open("%s.txt" %n1, "a")

    c.write("Nombre :"+ n1 + "\n")
    c.write("Direccion :"+ n2 + "\n")
    c.write("Dni :"+ n3 + "\n")
    c.write("Fecha de naciomiento :"+ n4 + "\n")
    c.write("Sexo :"+ n5 + "\n")
    c.write("Cormobilidad :"+ n6 + "\n")
    c.write("Centro de atencion :"+ n7 + "\n")
    c.write("Email: "+ n8 + "\n")


    c.close()


def salida_a_excel(Nuestro_Data_Frame):
    Nuestro_Data_Frame.to_excel(r"Salida_Excel.xlsx",
    sheet_name="Hoja_Datos", index=False)


def retorno_prioridad(n1,n2):
    pacientes[n2]={n1}



    


@app.route("/guardar_info", methods=['GET', 'POST'])
def guardar():


    nombre= request.form.get("nombre")
    dni = request.form.get("dni")
    direccion = request.form.get("direccion")
    fecha=request.form.get("fecha_de_nacimiento")
    sexo= request.form.get("sexo")
    cormobilidad= request.form.get("cormobilidad")
    centro=request.form.get("centro")
    email=request.form.get("email")
    edad=request.form.get("edad")
    prioridad=int(edad)+len(cormobilidad.split(","))

    diccionario_para_excel={"nombre":nombre,"dni":dni,
    "cormobilidad":cormobilidad,"prioridad":prioridad}
    lista_para_excel.append(diccionario_para_excel)
    lo_que_tengo = pd.DataFrame(lista_para_excel)
    lista_para_excel.pop()
    try:
        lo_que_leo= pd.read_excel("Salida_Excel.xlsx")
        print("lo que leo")
        print(lo_que_leo)
        print("lo que tengo del formulario")
        print(lo_que_tengo)
        el_total = lo_que_tengo.append(lo_que_leo)
        print("esto es el append de todo")
        print(el_total)
        os.remove("Salida_Excel.xlsx")
        salida_a_excel(el_total)
                
        
    except:
        salida_a_excel(lo_que_tengo)

    
    guardar_archivo(nombre,dni,direccion,fecha,sexo,cormobilidad,centro,email,edad)
    guardar_nombres(nombre)
    guardar_txt_personal(nombre,direccion,dni,fecha,sexo,cormobilidad,centro,email)

    retorno_prioridad(nombre,prioridad)
    
    

    return index()










if __name__=="__main__":
    app.run(debug=True,port=8000)
