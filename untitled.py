
import requests
from PyQt5 import QtCore, QtGui, QtWidgets
from bs4 import BeautifulSoup
from xml.dom import minidom
import xml.etree.ElementTree as ET

url = 'http://127.0.0.1:5000'


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget,clicked= lambda:enviar(self.plainTextEdit_2))
        self.pushButton.setGeometry(QtCore.QRect(120, 30, 101, 51))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(480, 30, 121, 51))
        self.pushButton_2.setObjectName("pushButton_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(60, 140, 301, 331))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(420, 140, 301, 331))
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 120, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(420, 120, 47, 13))
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuCargar = QtWidgets.QMenu(self.menubar)
        self.menuCargar.setObjectName("menuCargar")
        self.menuMostrar_ayuda = QtWidgets.QMenu(self.menubar)
        self.menuMostrar_ayuda.setObjectName("menuMostrar_ayuda")
        self.menuPeticiones = QtWidgets.QMenu(self.menubar)
        self.menuPeticiones.setObjectName("menuPeticiones")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionInformacion_del_estudiante = QtWidgets.QAction(MainWindow)
        self.actionInformacion_del_estudiante.setObjectName("actionInformacion_del_estudiante")
        self.actionDocumentacion = QtWidgets.QAction(MainWindow)
        self.actionDocumentacion.setObjectName("actionDocumentacion")
        self.actionConsultar_datos = QtWidgets.QAction(MainWindow)
        self.actionConsultar_datos.setObjectName("actionConsultar_datos")
        self.actionFiltrar_por_fecha_y_usuario = QtWidgets.QAction(MainWindow)
        self.actionFiltrar_por_fecha_y_usuario.setObjectName("actionFiltrar_por_fecha_y_usuario")
        self.actionFiltrar_por_fecha_y_codigo_de_error = QtWidgets.QAction(MainWindow)
        self.actionFiltrar_por_fecha_y_codigo_de_error.setObjectName("actionFiltrar_por_fecha_y_codigo_de_error")
        self.actionCargar_Archivo = QtWidgets.QAction(MainWindow)
        self.actionCargar_Archivo.setObjectName("actionCargar_Archivo")
        self.menuCargar.addAction(self.actionCargar_Archivo)
        self.menuMostrar_ayuda.addAction(self.actionInformacion_del_estudiante)
        self.menuMostrar_ayuda.addAction(self.actionDocumentacion)
        self.menuPeticiones.addAction(self.actionConsultar_datos)
        self.menuPeticiones.addAction(self.actionFiltrar_por_fecha_y_usuario)
        self.menuPeticiones.addAction(self.actionFiltrar_por_fecha_y_codigo_de_error)
        self.menubar.addAction(self.menuCargar.menuAction())
        self.menubar.addAction(self.menuPeticiones.menuAction())
        self.menubar.addAction(self.menuMostrar_ayuda.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.menuCargar.triggered.connect(lambda :CargarArchivo(self.plainTextEdit))
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Enviar"))
        self.pushButton_2.setText(_translate("MainWindow", "Reset"))
        self.label.setText(_translate("MainWindow", "Entrada"))
        self.label_2.setText(_translate("MainWindow", "Salida"))
        self.menuCargar.setTitle(_translate("MainWindow", "Cargar"))
        self.menuMostrar_ayuda.setTitle(_translate("MainWindow", "Mostrar ayuda"))
        self.menuPeticiones.setTitle(_translate("MainWindow", "Peticiones"))
        self.actionInformacion_del_estudiante.setText(_translate("MainWindow", "Informacion del estudiante"))
        self.actionDocumentacion.setText(_translate("MainWindow", "Documentacion"))
        self.actionConsultar_datos.setText(_translate("MainWindow", "Consultar datos"))
        self.actionFiltrar_por_fecha_y_usuario.setText(_translate("MainWindow", "Filtrar por fecha y usuario"))
        self.actionFiltrar_por_fecha_y_codigo_de_error.setText(_translate("MainWindow", "Filtrar por fecha y codigo de error"))
        self.actionCargar_Archivo.setText(_translate("MainWindow", "Cargar Archivo"))


#-----------Memoria--------------------
ArchivoG = None

#----------funciones-------------------
def enviar(ui):
    files = {'file': open('temp.txt','rb')}
    r = requests.post(url + '/upload',files = files )
    ui.setPlainText(r.text)
def CargarArchivo(ui):
    global ArchivoG
    ruta = QtWidgets.QFileDialog.getOpenFileName()[0]
    Archivo = open(ruta)
    ArchivoG = Archivo.read()
    f = open('temp.txt', 'w')
    f.write(ArchivoG)
    f.close()
    ui.setPlainText(ArchivoG)
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

