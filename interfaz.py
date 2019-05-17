import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import textos as text
import tester
import re
import math
import ming
import textos
from bson.objectid import ObjectId


class Aplicacion(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # Definimos como componente raíz para su recuperación desde cualquier componente hijo, nieto, etc.
        self.root = self

        # Definir título
        self.title("Categorías Test")

        # Incluir menú de anotaciones
        self.menu_principal = MenuPrincipal(self)
        self.config(menu=self.menu_principal)

        # Escala para visualizar la ventana
        self.wm_minsize(300, 100)

        # Variable ejecución de control
        self.ejecucion = None

        # Frames de la aplicación
        self.frame_tests = None
        self.frame_palabras = None
        self.frame_estado = None
        self.frame_control = None


    def display_ejecucion(self, ejecucion):
        self.ejecucion = ejecucion
        self.display_tests()
        self.display_palabras()
        self.display_estado()
        self.display_control()

    def display_tests(self):
        if self.frame_tests is not None:
            self.frame_tests.destroy()
        self.frame_tests = FrameTests(self)
        self.frame_tests.grid(row=0, column=0, sticky=tk.N+tk.S)

    def display_palabras(self):
        if self.frame_palabras is not None:
            self.frame_palabras.destroy()
        print("display palabras")
        self.frame_palabras = FramePalabras(self)
        self.frame_palabras.grid(row=0, column=1, sticky=tk.N+tk.W)

    def display_estado(self):
        self.frame_estado = FrameEstado(self)
        self.frame_estado.grid(row=0, column=2, sticky=tk.N+tk.E)
        print("display estado")

    def display_control(self):
        if self.frame_control is not None:
            self.frame_control.destroy()
        self.frame_control = FrameControl(self)
        self.frame_control.grid(row=1, column=0, sticky=tk.E+tk.W, columnspan=3)

    def display_edicion(self, palabra):
        self.edicion = VentanaEdicionPalabra(self, palabra)
        print(palabra.__dict__)
        self.wait_window(self.edicion)

class MenuPrincipal(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        # Definimos el componente padre
        self.parent = parent
        self.root = parent.root

        # Opciones del menú:

        # Opción 1 - Botón Menú
        self.anotar_menu = tk.Menu(self, tearoff=0)
        self.anotar_menu.add_command(label="Iniciar anotaciones", command=self.mostrar_inicio)
        self.anotar_menu.add_command(label="Recuperar anotaciones")
        self.add_cascade(label="Menú", menu=self.anotar_menu)

        # Opción 2 - Botón Información
        self.add_command(label="Información", command=self.mostrar_info)

    def mostrar_info(self):
        texto = text.TextoInformacion()
        messagebox.showinfo(title=texto.titulo, message=texto.descripcion)

    def mostrar_inicio(self):
        ventana_inicio = VentanaIniciarAnotaciones(self)
        # La ventana de incio aparece sin bloquear la ventana principal (por defecto)
        # Del sigiente modo, se espera a que el diálogo se cierre
        self.wait_window(ventana_inicio)


class VentanaIniciarAnotaciones(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)

        # Definimos atributos de configuracion
        self.configuracion = Configuracion()

        # Definimos el componente padre
        self.parent = parent
        self.root = parent.root

        # No permitimos que se interactúe con la ventana padre
        self.grab_set()

        # Definimos la etiqueta de la ventana
        self.title("Configuración de inicio de anotaciones")

        # Campos:
        # Frame 1
        frame_rutas = tk.LabelFrame(self, text="Parámetros de configuración de anotaciones")
        frame_rutas.grid(column=0, row=0, padx=20, pady=10)

        # Frame 1 - Campo 1 - Ruta del fichero de tests
        label_fichero = tk.Label(frame_rutas, text="Ruta del fichero de texto:")
        label_fichero.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        input_fichero = tk.Entry(frame_rutas, width=50, textvariable=self.configuracion.fichero)
        input_fichero.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        boton_fichero = tk.Button(frame_rutas, text="Seleccionar...",
                                  command=lambda: self.seleccionar_fichero(input_fichero))
        boton_fichero.grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)

        # Frame 1 - Campo 2 - Ruta del controlador de mongoDB
        label_controlador = tk.Label(frame_rutas, text="Ruta del controlador de MongoDB:")
        label_controlador.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        input_controlador = tk.Entry(frame_rutas, width=50, textvariable=self.configuracion.controlador)
        input_controlador.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Frame 1 - Campo 3 - Ruta para la base de datos a crear
        label_bd = tk.Label(frame_rutas, text="Ruta de la Base de Datos a crear:")
        label_bd.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

        input_bd = tk.Entry(frame_rutas, width=50, textvariable=self.configuracion.bd)
        input_bd.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        boton_bd = tk.Button(frame_rutas, text="Seleccionar...", command=lambda: self.seleccionar_carpeta(input_bd))
        boton_bd.grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)

        # Frame 2 - Campo 4 - Categoría de tests seleccionada
        frame_categorias = tk.LabelFrame(self, text="Categoría de las anotaciones")
        frame_categorias.grid(column=0, row=1, padx=20, pady=10, sticky=tk.W+tk.E)

        radio_animales = tk.Radiobutton(frame_categorias, text="Animales", variable=self.configuracion.categoria,
                                        value=0)
        radio_animales.grid(row=0, column=0, sticky=tk.E+tk.W)

        radio_plantas = tk.Radiobutton(frame_categorias, text="Plantas", variable=self.configuracion.categoria, value=1)
        radio_plantas.grid(row=0, column=1, sticky=tk.E+tk.W)

        radio_ropa = tk.Radiobutton(frame_categorias, text="Ropa", variable=self.configuracion.categoria, value=2)
        radio_ropa.grid(row=0, column=2, sticky=tk.E+tk.W)

        radio_vehiculos = tk.Radiobutton(frame_categorias, text="Vehículos", variable=self.configuracion.categoria,
                                         value=3)
        radio_vehiculos.grid(row=0, column=3, sticky=tk.E+tk.W)

        # Botones de acción
        # Frame 3
        frame_acciones = tk.Frame(self)
        frame_acciones.grid(column=0, row=2, pady=20)

        boton_aceptar = tk.Button(frame_acciones, text="Iniciar Test", command=self.iniciar_test)
        boton_aceptar.grid(row=0, column=0, padx=15, sticky=tk.W+tk.E)

        boton_cancelar = tk.Button(frame_acciones, text="Cancelar", command=self.cancelar)
        boton_cancelar.grid(row=0, column=1, padx=15, sticky=tk.W+tk.E)

    def seleccionar_fichero(self, input_field):
        fichero = filedialog.askopenfile(initialdir="/", title="Seleccionar fichero",
                                           filetypes=(("text files", "*.txt"),))
        if fichero:
            input_field.insert(0, fichero.name)
            # print(self.configuracion.fichero.get())

    def seleccionar_carpeta(self, input_field):
        n_carpeta = filedialog.askdirectory(initialdir="/", title="Seleccionar directorio")
        if n_carpeta:
            input_field.insert(0, n_carpeta)
            # print(self.configuracion.bd.get())

    def cancelar(self):
        # Volvemos a la ventana padre
        self.parent.focus_set()
        # Destruimos la ventana actual
        self.destroy()

    def iniciar_test(self):
        # Validar campos
        if self.configuracion.validar():
            print("Se puede iniciar la anotación")
            # Crear los datos del experimento
            ejecucion = tester.EjecucionAnotacion(self.configuracion)
            # Cerrar la ventana de configuración
            self.destroy()
            # Crear los widgets de ejecución en la ventana principal
            # self.parent.parent.display_ejecucion(ejecucion)
            self.root.display_ejecucion(ejecucion)

        else:
            print("No se puede iniciar la anotación")


class Configuracion:
    def __init__(self):
        self.fichero = tk.StringVar()
        self.controlador = tk.StringVar()
        self.bd = tk.StringVar()
        self.categoria = tk.IntVar()

    def validar(self):
        assert self.fichero is not None
        assert self.controlador is not None
        assert self.categoria is not None
        assert self.bd is not None
        return True


class FrameTests(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=800)
        # Definimos el componente padre
        self.parent = parent
        self.root = parent.root

        # Definición de la etiqueta de tests
        # self.label_tests = tk.Label(self, text="Lista de tests: ")
        # self.label_tests.grid(row=0, column=0, sticky=tk.W)

        # Definición del listado de tests
        # Creo una listbox dentro del frame
        self.lista_tests = tk.Listbox(self, selectmode=tk.SINGLE)
        # Creo un widget scroll dentro de la listbox con display vertical
        self.scroll_tests = tk.Scrollbar(self, orient=tk.VERTICAL)
        # Indico a mi lista que cuando se haga scroll en dirección Y, se llame al método set del scroll
        self.lista_tests.config(yscrollcommand=self.scroll_tests.set)
        # Indico a mi scroll que el comando a usar cuando se mueva el scroll sea en la dirección Y
        self.scroll_tests.config(command=self.lista_tests.yview)

        # Inserto los ids de los tests en la lista
        for i, test in enumerate(self.parent.ejecucion.tests):
            self.lista_tests.insert(i, str(i) + " : " + test.id)

        # Display del listado de tests
        self.lista_tests.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.scroll_tests.grid(row=0, column=1, sticky=tk.N+tk.S)


        # Incluyo evento de selección de test para que se lance la función cada vez que haya una selección
        self.lista_tests.bind("<<ListboxSelect>>", self.seleccion_test)

    def seleccion_test(self, event):
        print(event)
        id_test = self.lista_tests.get(self.lista_tests.curselection())
        print(id_test, "CHECK")
        self.parent.ejecucion.test_seleccionado = int(re.split(" : ", id_test)[0])
        self.parent.display_palabras()


class FramePalabras(tk.LabelFrame):
    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text="Palabras del test")
        # Definimos el componente padre
        self.parent = parent
        self.root = parent.root

        # Definición del área de palabras
        seleccion = self.parent.ejecucion.test_seleccionado
        if seleccion != None:
            for i, palabra in enumerate(self.parent.ejecucion.tests[seleccion].palabras):
                # Defino un recuadro para hacer display de una palabra
                frame_palabra = FramePalabra(self, palabra)
                frame_palabra.grid(row=math.floor(i/5), column=i % 5, sticky=tk.N+tk.W+tk.E+tk.S)


class FramePalabra(tk.Frame):
    def __init__(self, parent, palabra):
        tk.Frame.__init__(self, parent)
        # Definimos el componente padre
        self.parent = parent
        self.palabra = palabra
        self.root = parent.root

        # Definición del área de texto
        self.label = tk.Label(self, text=palabra.texto)

        # Definición del área de color o estado
        self.estado = tk.Frame(self, width=5)

        # Definicón de la posición de la palabra
        self.pos = tk.Label(self, text=str(palabra.posicion))

        # Definición del botón de edición
        self.boton = tk.Button(self, text="Edit", command=self.seleccion_palabra)

        # Grids de cada parte de la palbra
        self.estado.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N+tk.S)
        self.label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.E+tk.W)
        self.boton.grid(row=1, column=2, pady=5, sticky=tk.E)
        self.pos.grid(row=0, column=0, sticky=tk.E+tk.W, padx=5, pady=5, columnspan=3)

        # Configuración de colores y posibilidad de edición
        if self.palabra.estado == 0:
            self.estado.config(bg="black")
            self.boton.config(state=tk.DISABLED)
        elif self.palabra.estado == 1:
            self.estado.config(bg="yellow")
        elif self.palabra.estado == 2:
            self.estado.config(bg="green")
        elif self.palabra.estado == 3:
            self.estado.config(bg="red")

    def seleccion_palabra(self):
        print("Selección de :" + self.palabra.texto)
        self.parent.parent.display_edicion(self.palabra)


class FrameEstado(tk.LabelFrame):
    def __init__(self, parent):
        tk.LabelFrame.__init__(self, parent, text="Información del progreso")
        # Definimos el componente padre
        self.parent = parent
        self.root = parent.root

        self.label1 = tk.Label(self, text="Tests completos : " + str(self.parent.ejecucion.tests_completos))
        self.label2 = tk.Label(self, text="Tests incompletos : " + str(self.parent.ejecucion.tests_incompletos))
        self.label3 = tk.Label(self, text="Palabras totales : " + str(self.parent.ejecucion.palabras_inicial))
        self.label4 = tk.Label(self, text="Palabras encontradas : " + str(self.parent.ejecucion.palabras_encontradas))
        self.label5 = tk.Label(self, text="Palabras confirmadas : " + str(self.parent.ejecucion.palabras_confirmadas))
        self.label6 = tk.Label(self,
                               text="Palabras no encontradas : " + str(self.parent.ejecucion.palabras_no_encontradas))
        self.label7 = tk.Label(self,
                               text="Palabras procesadas : " + str(self.parent.ejecucion.palabras_procesadas))

        self.label1.grid(row=0, column=0)
        self.label2.grid(row=1, column=0)
        self.label3.grid(row=2, column=0)
        self.label7.grid(row=3, column=0)
        self.label4.grid(row=4, column=0)
        self.label5.grid(row=5, column=0)
        self.label6.grid(row=6, column=0)


class FrameControl(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        # Definimos el componente padre
        self.parent = parent
        self.root = parent.root

        # Definición del botón de Iniciar/Pausar
        self.boton = tk.Button(self, text="Iniciar", command=self.iniciar)
        self.boton.grid(row=0, column=0)

        # Definición de la barra de progreso
        self.progreso = ttk.Progressbar(self, orient="horizontal", length=self.parent.ejecucion.palabras_totales,
                                        mode="determinate", maximum=self.parent.ejecucion.palabras_totales)
        self.progreso.grid(row=0, column=1)

        # Definición del botón step
        self.stepper = tk.Button(self, text="Step!", command=self.step)
        self.stepper.grid(row=0, column=2)

    def iniciar(self):
        # Cambio el botón
        self.boton.configure(text="Pausar", command=self.pausar)
        # self.progreso.step(1)

    def pausar(self):
        # Cambio el botón
        self.boton.configure(text="Iniciar", command=self.iniciar)
        # self.progreso.step(1)

    def step(self):
        self.parent.ejecucion.procesar_palabra()
        self.progreso.step(1)
        self.parent.display_estado()
        self.parent.display_palabras()


class VentanaEdicionPalabra(tk.Toplevel):
    def __init__(self, parent, palabra):
        tk.Toplevel.__init__(self, parent)
        # Definición del componente padre
        self.parent = parent
        self.root = parent.root

        # No permitimos que se interactúe con la ventana padre
        self.grab_set()

        # Guardamos la palabra actual
        self.palabra = palabra

        # Definición del frame formulario
        # self.parent.ejecucion.
        self.formulario = FormularioPalabra(self, self.palabra)
        self.formulario.grid(row=0, column=0, columnspan=3)

        # Definición del los botones de acción
        # Botón de edición
        self.editar = tk.Button(self, text="Editar", command=self.habilitar_edicion)
        self.editar.grid(row=1, column=0, pady=10, sticky=tk.E, padx=5)
        # Botón de cancelar
        self.cancelar = tk.Button(self, text="Cancelar", command=self.cancelar_edicion)
        self.cancelar.grid(row=1, column=1, pady=10, padx=5)
        # Botón de confirmar
        self.confirmar = tk.Button(self, text="Confirmar", command=lambda: self.confirmar_datos())
        self.confirmar.grid(row=1, column=2, pady=10, padx=5, sticky=tk.W)

    def habilitar_edicion(self):
        print("Habilitar edición")
        for campo in list(self.formulario.campos.values())[1:]:
            if campo.__class__.__name__=="RadioIO":
                for radio in campo.radios:
                    radio.configure(state=tk.NORMAL)
            else:
                campo.configure(state=tk.NORMAL)

    def cancelar_edicion(self):
        print("Cancelar edición")
        self.destroy()

    def confirmar_datos(self):
        print("Confirmar datos")
        # Recopilar los datos de los inputs
        diccionario_objeto = self.formulario.generar_objeto()
        print(diccionario_objeto, "DICT OBJETO")

        print(diccionario_objeto["_id"], "DICT OBJETO 2")

        # Guardar el objeto en la BD
        # self.parent.ejecucion.session.update(self.parent.ejecucion.mapper.mapped_class(), {"_id": diccionario_objeto["_id"]}, {"$set": objeto}, upsert=False)

        # obj = self.parent.ejecucion.mapper.mapped_class.query.find({"_id": schema.ObjectId(diccionario_objeto["_id"])}).first()

        doc = self.parent.ejecucion.mapper.mapped_class.query.get(_id=ObjectId(diccionario_objeto["_id"]))
        print(doc)

        self.parent.ejecucion.mapper.mapped_class.query.update({"_id": doc._id},{'$set': diccionario_objeto})
        doc = self.parent.ejecucion.session.refresh(doc)

        print(doc)

        # for k, v in diccionario_objeto.items():
        #     if k != "_id":
        #         obj[k] = v

        self.parent.ejecucion.session.flush()

        # Actualizar estado de la palabra en test
        self.parent.ejecucion.tests[self.palabra.test_index].palabras[self.palabra.posicion-1].estado = 2
        self.parent.ejecucion.tests[self.palabra.test_index].palabras[self.palabra.posicion-1].objeto = doc

        # Actualizar los frames de palabras, estado, control y tests
        self.parent.display_palabras()
        self.parent.display_estado()
        self.parent.display_control()

        # Cerrar ventana
        self.destroy()


class FormularioPalabra(tk.Frame):
    def __init__(self, parent, palabra):
        tk.Frame.__init__(self, parent)
        # Definimos el componente padre
        self.parent = parent
        self.root = parent.root

        self.labels = []
        self.campos = {}
        self.diccionario_propiedades = self.parent.parent.ejecucion.mapper.mapped_class.__dict__

        # El objeto mapper contiene -> mapped_class, collecion y session
        # Determinamos el modelo de datos que hay que cargar
        if palabra.estado == 0:
            print("No se puede editar aún")

        elif palabra.estado == 1:
            print("Mostrar datos recopilados, sin habilitar edición")
            self.mostrar_formulario(habilitar=False, objeto=palabra.objeto)

        elif palabra.estado == 2:
            print("Mostrar datos de la base de datos, sin habilitar edición")
            self.mostrar_formulario(habilitar=False, objeto=palabra.objeto)

        elif palabra.estado == 3:
            print("Mostrar formulario vacío y habilitado")
            self.mostrar_formulario(habilitar=True, objeto=palabra.objeto)

    def mostrar_formulario(self, habilitar, objeto):
        fila = 0
        # Por cada atributo y su tipo
        for key, value in self.diccionario_propiedades.items():
            # Por cada atributo del tipo propiedad
            if type(value)== ming.odm.property.FieldProperty:

                # Obtengo el nombre del campo correspondiente al atributo
                nombre_campo = textos.campos[self.parent.parent.ejecucion.entity].get(key)

                # Defino el label con el nombre del campo
                label = tk.Label(self, text=nombre_campo)
                label.grid(row=fila, column=0, sticky=tk.W, padx=5, pady=5)

                # Defino el componente de entrada/salida correspondiente con el valor del atributo
                clase_campo = textos.displays.get(self.parent.parent.ejecucion.entity).get(key)

                valor = None

                print("Mostrar formulario para objeto : ", objeto)

                if objeto:
                    valor = objeto[key]
                campo = clase_campo(parent=self, valor=valor, key=key)
                campo.grid(row=fila, column=1, sticky=tk.E, padx=5, pady=5)

                # Habilitar o no la edición por defecto
                if campo.__class__.__name__ == "RadioIO":
                    for radio in campo.radios:
                        if habilitar and key != "_id":
                            radio.configure(state=tk.NORMAL)
                        else:
                            radio.configure(state=tk.DISABLED)
                else:
                    if habilitar and key != "_id":
                        campo.configure(state=tk.NORMAL)
                    else:
                        campo.configure(state=tk.DISABLED)


                # Añadimos los objetos visuales por si necesitamos acceder a ellos
                self.campos.update({key: campo})
                self.labels.append(label)

                # Aumentar la fila del formulario
                fila += 1

    def generar_objeto(self):
        datos = {}
        for key, value in self.diccionario_propiedades.items():
            # Por cada atributo del tipo propiedad
            if type(value) == ming.odm.property.FieldProperty:

                # La clave es el nombre del atributo
                dato = self.campos[key].generar()
                print(dato)
                if dato:
                    datos.update(dato)

        print(datos)
        return datos

class EntryIO(tk.Entry):
    """Tipo de clase entry con método de input/output para una etiqueta"""
    def __init__(self, parent, valor, key):
        tk.Entry.__init__(self, parent)
        # Definición del componente padre
        self.parent = parent
        self.root = parent.root

        # Recuperamos el valor (objeto) y la clave del atributo
        self.valor = valor
        self.key = key

        self.mostrar()

    def mostrar(self):
        if self.valor:
            self.insert(tk.END, self.valor)

    def generar(self):
        return {self.key: self.get()}


class TextIO(tk.Text):
    """Tipo de clase text con método input/output para campos con más de una etiqueta"""
    def __init__(self, parent, valor, key):
        tk.Text.__init__(self, parent, height=5, width=60, wrap=tk.WORD)
        # Definición del componente padre
        self.parent = parent
        self.root = parent.root

        # Recuperamos el valor y la clave
        self.valor = valor  # Es un array de strings
        self.key = key

        self.mostrar()

    def mostrar(self):
        if self.valor:
            self.insert(tk.END, ",".join(self.valor))

    def generar(self):
        texto = self.get("1.0", tk.END)
        etiquetas = texto.split(",")
        return {self.key: etiquetas}


class RadioIO(tk.Frame):
    """Clase con I/O para representar un radio-button"""
    def __init__(self, parent, valor, key):
        tk.Frame.__init__(self, parent)
        # Definición del componente padre
        self.parent = parent
        self.root = parent.root

        # Recuperamos el diccionario y la clave que le dió acceso
        self.valor = valor  # {etiqueta: e1, uri: u1}
        self.key = key

        print(self.valor)

        # variable que alberga la selección
        self.radiovar = tk.StringVar()

        # Un array con los botones
        self.radios = []

        # Mostramos inicialmente
        self.mostrar()

    def mostrar(self):
        # El diccionario contiene dos claves: etiqueta y uri
        # Pero debemos conocer las posibles opciones (pares etiqueta - uri)
        i = 0

        # Establecemos el diccionario de opciones de formulario
        self.opciones = textos.opciones[self.parent.parent.parent.ejecucion.entity][self.key]

        # Establecemos un mapeo de uris
        mapeo = None
        if self.key in textos.mapeos[self.parent.parent.parent.ejecucion.entity].keys():
            mapeo = textos.mapeos[self.parent.parent.parent.ejecucion.entity][self.key]

        # Indicamos cúal es la uri mapeada
        uri_seleccionada = None
        if self.valor:
            if self.valor["uri"] in self.opciones.keys():
                uri_seleccionada = self.valor["uri"]
            elif mapeo:
                if self.valor["uri"] in mapeo.keys():
                    uri_seleccionada = mapeo.get(self.valor)

        for key, value in self.opciones.items():
            # Las opciones vienen en pares {uri1:label1, u2:l2, ...}
            radio = tk.Radiobutton(self, text=value, value=key, variable=self.radiovar)
            radio.grid(row=math.floor(i/5), column=i % 5, sticky=tk.W)
            i = i + 1
            # if uri_seleccionada == key:
            #     print("SELECT")
            #     radio.select()
            # else:
            #     print("DESELECT")
            #     radio.deselect()

            self.radios.append(radio)

        if uri_seleccionada:
            self.radiovar.set(uri_seleccionada)
        else:
            self.radiovar.set("UNK")

    def generar(self):
        return {self.key: {"uri": self.radiovar.get(), "etiqueta": self.opciones.get(self.radiovar.get())}}


class SingleTreeIO(tk.Entry):
    def __init__(self, parent, valor, key):
        tk.Entry.__init__(self, parent)
        self.var = 0

        self.parent = parent
        self.root = parent.root

        self.key = key
        self.valor = valor

    def mostrar(self):
        print(0)

    def generar(self):
        return{self.key: {"etiqueta": "", "uri": ""}}


class MultipleTreeIO(tk.Entry):
    def __init__(self, parent, valor, key):
        tk.Entry.__init__(self, parent)
        self.parent = parent
        self.root = parent.root

        self.var = 0

        self.key = key
        self.valor = valor

    def mostrar(self):
        print(0)

    def generar(self):
        return {self.key: [{"etiqueta": "", "uri": ""}]}


# MAIN
if __name__ == "__main__":
    aplicacion = Aplicacion()
    aplicacion.mainloop()
