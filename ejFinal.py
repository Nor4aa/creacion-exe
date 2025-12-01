
import os
 
from PySide6.QtCore import Qt # type: ignore
from datetime import datetime
from PySide6.QtGui import QAction, QIcon, QKeySequence, QTextCursor, QTextDocument, QFont, QColor, QTextCharFormat # type: ignore
from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QTextEdit, QFileDialog, QMessageBox, QWidget, QLineEdit, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QColorDialog, QFontDialog, QStatusBar, QCheckBox, QGroupBox, QRadioButton

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Word")
        self.archivo_actual = None #Variable donde se guarda la ruta del archivo abierto
        self.resize(700, 500)
        self.ultima_posicion_busqueda = 0

        #zona del texto
        self.texto= QTextEdit()
        self.texto.setPlaceholderText("Escribe o pega tu texto aquí.....")

        #Panel lateral de búsqueda avanzada 
        self.panel_busqueda = self.crear_panel()

        #Layout principal
        layout_principal = QHBoxLayout()
        layout_principal.addWidget(self.texto)
        layout_principal.addWidget(self.panel_busqueda)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        #Barra de estado
        #Contador de palabras --> actualizar cada que cambia el texto
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.contador_palabras = QLabel("Palabras: 0")
        self.status_bar.addPermanentWidget(self.contador_palabras)
        self.texto.textChanged.connect(self.actualizar_contador)

        #Actualizar el contador
        self.texto.textChanged.connect(self.actualizar_contador)

        #menus
        barra_menus = self.menuBar()
        self.menu_archivo = barra_menus.addMenu("Archivo")
        self.menu_editar = barra_menus.addMenu("Editar")
        self.menu_personalizar = barra_menus.addMenu("Personalizar")
        self.menu_herramientas = barra_menus.addMenu("Herramientas") 

        #herramientas1
        barra_herramientas = QToolBar("Archivo")
        barra_herramientas.setMovable(False) #Evitar que se mueva
        barra_herramientas.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(barra_herramientas)

        #herramientas2
        barra_herramientas2 = QToolBar("Editar")
        barra_herramientas2.setMovable(False)
        barra_herramientas2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(barra_herramientas2)
        
        #herramientas3
        barra_herramientas3 = QToolBar("Adicional")
        barra_herramientas3.setMovable(False)
        barra_herramientas3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addToolBar(barra_herramientas3)
   
        #Personalizar
        accion_color = QAction("Cambiar el color del fondo",self)
        accion_color.triggered.connect(self.cambiar_color)
        self.menu_personalizar.addAction(accion_color)

        accion_fuente = QAction("Cambiar tipo de letra",self)
        accion_fuente.triggered.connect(self.cambiar_fuente)
        self.menu_personalizar.addAction(accion_fuente)

        #ACCION EXTRA
        #FECHA
        ruta_hora = os.path.join(os.path.dirname(__file__), "C:\\Users\\norit\\Downloads\\hora.png")
        accion_fecha = QAction(QIcon(ruta_hora), "Fecha y hora", self)
        accion_fecha.setShortcut(QKeySequence("Ctrl+D"))
        accion_fecha.triggered.connect(self.insertar_fecha_hora)

        barra_herramientas3.addAction(accion_fecha)
        self.menu_herramientas.addAction(accion_fecha)
        #ACCIONES EDITAR
        #accion de nuevo
        #imagen
        ruta_a_icono = os.path.join(os.path.dirname(
            __file__), "C:\\Users\\norit\\Downloads\\nuevo.png")
        accion_nuevo = QAction(QIcon(ruta_a_icono), "Nuevo", self)  
        #accion 
        accion_nuevo.setShortcut(QKeySequence.New) # = Ctrl + N
        accion_nuevo.triggered.connect(self.nuevo_archivo)
        #barra_herramientas
        barra_herramientas.addAction(accion_nuevo)
        self.menu_archivo.addAction(accion_nuevo)

        #accion abrir
        #imagen
        icono_abrir = os.path.join(os.path.dirname(
            __file__), "abrir2.png")
        accion_abrir = QAction(QIcon(icono_abrir),"Abrir",self)
        #accion
        accion_abrir.setShortcut(QKeySequence.Open)
        accion_abrir.triggered.connect(self.abrir_archivo)
        #barra_herramientas
        barra_herramientas.addAction(accion_abrir)
        self.menu_archivo.addAction(accion_abrir)

        #accion guardar
        #imagen
        accion_guardar = QAction(QIcon(os.path.join(os.path.dirname(__file__), "C:\\Users\\norit\\Downloads\\guardar.png")), "Guardar", self)
        self.menu_archivo.addAction(accion_guardar)
        #accion
        accion_guardar.setShortcut(QKeySequence.Save)
        accion_guardar.triggered.connect(self.guardar_archivo)
        #barra_herramientas
        barra_herramientas.addAction(accion_guardar)
        self.menu_archivo.addAction(accion_guardar)
  
        #accion salir
        accion_salir = QAction("Salir",self)
        accion_salir.setShortcut(QKeySequence.Quit)
        accion_salir.triggered.connect(self.salir_aplicacion)
        self.menu_archivo.addAction(accion_salir)

        #accion deshacer
        #imagen
        accion_deshacer = QAction(QIcon(os.path.join(os.path.dirname(__file__),  "C:\\Users\\norit\\Downloads\\deshacer2.png")), "Deshacer", self)
        self.menu_editar.addAction(accion_deshacer)
        #accion
        accion_deshacer.setShortcut(QKeySequence.Undo)
        accion_deshacer.triggered.connect(self.texto.undo)
        #barra_herramientas
        barra_herramientas2.addAction(accion_deshacer)
        self.menu_editar.addAction(accion_deshacer)
      
        #accion rehacer
        #imagen
        accion_rehacer = QAction(QIcon(os.path.join(os.path.dirname(__file__), "C:\\Users\\norit\\Downloads\\rehacer2.png")), "Rehacer", self)
        self.menu_editar.addSeparator()
        #accion
        accion_rehacer.setShortcut(QKeySequence.Redo)
        accion_rehacer.triggered.connect(self.texto.redo)   
        #barra_herramientas
        barra_herramientas2.addAction(accion_rehacer)
        self.menu_editar.addAction(accion_rehacer)
    
        #accion copiar
        #imagen
        accion_copiar = QAction(QIcon(os.path.join(os.path.dirname(__file__), "C:\\Users\\norit\\Downloads\\copiar2.png")), "Copiar", self)
        self.menu_editar.addAction(accion_copiar)
        #accion
        accion_copiar.setShortcut(QKeySequence.Copy)
        accion_copiar.triggered.connect(self.texto.copy)
        #barra_herramientas
        barra_herramientas2.addAction(accion_copiar)
        self.menu_editar.addAction(accion_copiar)
       
        #accion cortar
        #imagen
        accion_cortar = QAction(QIcon(os.path.join(os.path.dirname(__file__), "C:\\Users\\norit\\Downloads\\cortar.png")), "Cortar", self)
        self.menu_editar.addAction(accion_cortar)
        #accion
        accion_cortar.setShortcut(QKeySequence.Cut)
        accion_cortar.triggered.connect(self.texto.cut)
        #barra_herramientas
        barra_herramientas2.addAction(accion_cortar)
        self.menu_editar.addAction(accion_cortar)
        
        #accion pegar
        #imagen
        accion_pegar = QAction(QIcon(os.path.join(os.path.dirname(__file__), "C:\\Users\\norit\\Downloads\\pegar2.png")), "Pegar", self)
        self.menu_editar.addAction(accion_pegar)
        #accion
        accion_pegar.setShortcut(QKeySequence.Paste)
        accion_pegar.triggered.connect(self.texto.paste)
        #herramientas
        barra_herramientas2.addAction(accion_pegar)
        self.menu_editar.addAction(accion_pegar)

    def salir_aplicacion(self):
        respuesta = QMessageBox.question(self,"Salir", "¿Deseas salir?",QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            self.close()

    #FUNCIONES ARCHIVO
    def nuevo_archivo(self):
        self.texto.clear()
        self.archivo_actual = None 
        self.status_bar.showMessage("Nuevo documento creado",3000)

    def abrir_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self,"Abrir archivo","","Texto (*.txt);;Todos(*.*)")
        if archivo:
            with open(archivo,"r",encoding="utf-8") as f:
                self.texto.setPlainText(f.read())
            self.archivo_actual=archivo
            self.status_bar.showMessage(f"Archivo {archivo} abierto", 3000)
    
    def guardar_archivo(self):
        if not self.archivo_actual:
            archivo, _ = QFileDialog.getSaveFileName(self,"Guardar archivo", "", "Textos (*.txt);;Todos (*.*)")
            if not archivo:
                return
            self.archivo_actual = archivo
        
        with open(self.archivo_actual,"w", encoding="utf-8") as f:
            f.write(self.texto.toPlainText())

        QMessageBox.information(self,"Guardar", "Archivo guardado correctamente.")
        self.status_bar.showMessage("Archivo guardado correctamente.", 3000)

    #APARTADO PERSONALIZACION
    def cambiar_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.texto.setStyleSheet(f"background-color: {color.name()};")
            self.status_bar.showMessage(f"Color de fondo cambiado a {color.name()}",3000)

    def cambiar_fuente(self):
        fuente, a = QFontDialog.getFont()
        if a:
            self.texto.setFont(a)
            self.status_bar.showMessage("Fuente cambiada")
 
    #APARTADO CONTADOR
    def actualizar_contador(self):
        texto = self.texto.toPlainText()
        palabras = len(texto.split()) #Divide por espacios y cuenta
        self.contador_palabras.setText(f"Palabras: {palabras}")

    #BUSQUEDA/REMPLAZO AVANZADO
    def limpiar_resaltado(self):
        cursor = self.texto.textCursor()
        cursor.select(QTextCursor.Document)
        formato = QTextCharFormat()
        formato.setBackground(Qt.transparent)
        cursor.mergeCharFormat(formato)
        self.texto.setTextCursor(cursor)


    def resaltar_todas(self, texto_a_buscar):
        self.limpiar_resaltado()
        if not texto_a_buscar:
            return
        
        cursor = self.texto.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.texto.setTextCursor(cursor)

        formato = QTextCharFormat()
        formato.setBackground(QColor("#FFF59D"))  # Amarillo claro

        encontrado = False
        cursor = self.texto.document().find(texto_a_buscar)
        while not cursor.isNull():
            cursor.mergeCharFormat(formato)
            encontrado = True
            cursor = self.texto.document().find(texto_a_buscar, cursor)

        if not encontrado:
            QMessageBox.information(self, "No encontrado", "El texto no ha sido encontrado")
        else:
            self.status_bar.showMessage("Coincidencias resaltadas")

    def buscar_texto(self):
        texto_a_buscar = self.buscar_input.text().strip()
        if not texto_a_buscar:
            QMessageBox.warning(self,"Buscar", "Por favor, introduce un texto a buscar.")
            return
        
        if self.radio_todos.isChecked():
            self.resaltar_todas(texto_a_buscar)
            return
        
        self.limpiar_resaltado()
        
        # Configurar opciones de búsqueda
        opciones = QTextDocument.FindFlags()
        if self.radio_atras.isChecked():
            opciones |= QTextDocument.FindBackward

        # Realizar la búsqueda
        encontrado = self.texto.find(texto_a_buscar, opciones)

        if encontrado:
            # Resaltar la coincidencia encontrada
            cursor = self.texto.textCursor()
            formato = QTextCharFormat()
            formato.setBackground(QColor("#90CAF9"))  # Azul claro
            cursor.mergeCharFormat(formato)
            self.status_bar.showMessage("Coincidencia encontrada")
        else:
            # Si no se encuentra, volver al inicio y buscar de nuevo
            cursor = self.texto.textCursor()
            if self.radio_atras.isChecked():
                cursor.movePosition(QTextCursor.End)
            else:
                cursor.movePosition(QTextCursor.Start)
            self.texto.setTextCursor(cursor)
            
            # Intentar buscar de nuevo desde el inicio/fin
            encontrado = self.texto.find(texto_a_buscar, opciones)
            if encontrado:
                cursor = self.texto.textCursor()
                formato = QTextCharFormat()
                formato.setBackground(QColor("#90CAF9"))  # Azul claro
                cursor.mergeCharFormat(formato)
                self.status_bar.showMessage("Coincidencia encontrada (búsqueda reiniciada)")
            else:
                QMessageBox.information(self, "No encontrado", "El texto no ha sido encontrado en el documento.")
                self.status_bar.showMessage("Texto no encontrado")

    def crear_panel(self):
        panel= QGroupBox("Buscar/Remplazar")
        layout = QVBoxLayout()

        self.buscar_input = QLineEdit()
        self.reemplazar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Texto a buscar...")
        self.reemplazar_input.setPlaceholderText("Texto de reemplazo....")


        self.radio_adelante = QRadioButton("Buscar hacia adelante")
        self.radio_atras = QRadioButton("Buscar hacia atrás")
        self.radio_todos = QRadioButton("Buscar todas las coincidencias")
        self.radio_adelante.setChecked(True)

        self.boton_buscar = QPushButton("Buscar")
        self.boton_reemplazar = QPushButton("Reemplazar")
        self.boton_reemplazar_todo = QPushButton("Reemplazar todas")

        layout.addWidget(QLabel("Buscar:"))
        layout.addWidget(self.buscar_input)
        layout.addWidget(QLabel("Reemplazar con :"))
        layout.addWidget(self.reemplazar_input)
        layout.addWidget(self.radio_adelante)
        layout.addWidget(self.radio_atras)
        layout.addWidget(self.radio_todos)
        layout.addWidget(self.boton_buscar)
        layout.addWidget(self.boton_reemplazar)
        layout.addWidget(self.boton_reemplazar_todo)
        layout.addStretch()

        panel.setLayout(layout)

        #CONEXIONES
        self.boton_buscar.clicked.connect(self.buscar_texto)
        self.boton_reemplazar.clicked.connect(self.reemplazar_texto)
        self.boton_reemplazar_todo.clicked.connect(self.reemplazar_todo)

        return panel

    def reemplazar_texto(self):
        texto_a_buscar = self.buscar_input.text().strip()
        texto_reemplazo = self.reemplazar_input.text()

        if not texto_a_buscar:
            QMessageBox.warning(self, "Reemplazar", "Introduce un texto a buscar")
            return
        
        # Si estamos en modo "buscar todas", primero buscar sin reemplazar
        if self.radio_todos.isChecked():
            self.buscar_texto()
            return
        
        # Guardar la posición actual del cursor
        cursor_original = self.texto.textCursor()
        
        # Buscar la siguiente ocurrencia
        opciones = QTextDocument.FindFlags()
        if self.radio_atras.isChecked():
            opciones |= QTextDocument.FindBackward
            
        encontrado = self.texto.find(texto_a_buscar, opciones)
        
        if encontrado:
            # Reemplazar el texto encontrado
            cursor = self.texto.textCursor()
            cursor.insertText(texto_reemplazo)
            
            # Resaltar brevemente el texto reemplazado
            cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, len(texto_reemplazo))
            formato = QTextCharFormat()
            formato.setBackground(QColor("#A5D6A7"))  # Verde claro para reemplazo
            cursor.mergeCharFormat(formato)
            
            self.status_bar.showMessage("Texto reemplazado")
        else:
            # Si no se encuentra, volver a la posición original y mostrar mensaje
            self.texto.setTextCursor(cursor_original)
            
            # Intentar buscar desde el inicio/fin
            cursor = self.texto.textCursor()
            if self.radio_atras.isChecked():
                cursor.movePosition(QTextCursor.End)
            else:
                cursor.movePosition(QTextCursor.Start)
            self.texto.setTextCursor(cursor)
            
            encontrado = self.texto.find(texto_a_buscar, opciones)
            if encontrado:
                cursor = self.texto.textCursor()
                cursor.insertText(texto_reemplazo)
                
                # Resaltar brevemente el texto reemplazado
                cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, len(texto_reemplazo))
                formato = QTextCharFormat()
                formato.setBackground(QColor("#A5D6A7"))  # Verde claro para reemplazo
                cursor.mergeCharFormat(formato)
                
                self.status_bar.showMessage("Texto reemplazado (búsqueda reiniciada)")
            else:
                QMessageBox.information(self, "No encontrado", "No se encontró más texto para reemplazar")
                self.status_bar.showMessage("Texto no encontrado")

    def reemplazar_todo(self):
        texto_a_buscar = self.buscar_input.text().strip()
        texto_reemplazo = self.reemplazar_input.text()
        
        if not texto_a_buscar:
            QMessageBox.warning(self, "Reemplazar todo", "Introduce un texto a buscar.")
            return
        
        self.limpiar_resaltado()
        
        # Ir al inicio del documento
        cursor = self.texto.textCursor()
        cursor.movePosition(QTextCursor.Start)
        self.texto.setTextCursor(cursor)
        
        contador = 0
        encontrado = True
        
        # Reemplazar todas las ocurrencias
        while encontrado:
            encontrado = self.texto.find(texto_a_buscar)
            if encontrado:
                cursor = self.texto.textCursor()
                cursor.insertText(texto_reemplazo)
                contador += 1
        
        if contador > 0:
            self.status_bar.showMessage(f"Reemplazadas {contador} coincidencias.")
            QMessageBox.information(self, "Reemplazar todo", f"Se reemplazaron {contador} ocurrencias.")
        else:
            self.status_bar.showMessage("No se encontraron coincidencias para reemplazar.")
            QMessageBox.information(self, "Reemplazar todo", "No se encontraron coincidencias.")

#   ACCION EXTRA
    def insertar_fecha_hora(self):
        fecha_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.texto.textCursor().insertText(fecha_hora)
        self.status_bar.showMessage("Fecha y hora insertadas", 3000)

if __name__ == "__main__":
    app = QApplication([])
    ventana1 = VentanaPrincipal()
    ventana1.show()
    app.exec()