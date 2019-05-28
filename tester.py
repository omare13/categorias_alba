import modelo_datos
import wikidata
import entities
import io
import re
from ming import create_datastore, collection
from ming.odm import ODMSession
from ming.odm import Mapper


class EjecucionAnotacion:
    def __init__(self, configuracion):
        self.configuracion = configuracion
        self.fichero = Fichero(self.configuracion.fichero.get())
        self.tests = self.extraer_tests()
        self.current_test = 0
        self.current_palabra = 0
        self.test_seleccionado = None
        self.palabra_seleccionada = None
        self.tests_completos = None
        self.tests_incompletos = None
        self.palabras_inicial = None
        self.palabras_encontradas = None
        self.palabras_confirmadas = None
        self.palabras_no_encontradas = None
        self.palabras_totales = None
        self.palabras_procesadas = None
        self.session = None
        self.collection = None
        self.mapper = None
        self.entity = None
        self.estadistica_ejecucion()
        self.conectar_db()

    def estadistica_ejecucion(self):
        n_tests_completos = 0
        n_tests_incompletos = 0

        dist_pal = []
        dist_pal_inicial = []
        dist_pal_encontrada = []
        dist_pal_confirmada = []
        dist_pal_no_encontrada = []
        dist_pal_procesadas = []

        for test in self.tests:
            print(test)
            incompleto = False
            for palabra in test.palabras:
                if palabra.texto not in dist_pal:
                    dist_pal.append(palabra.texto)
                if (palabra.estado == 0) or (palabra.estado is None):
                    incompleto = True
                    if palabra.texto not in dist_pal_inicial:
                        dist_pal_inicial.append(palabra.texto)
                elif palabra.estado == 1:
                    incompleto = True
                    if palabra.texto not in dist_pal_encontrada:
                        dist_pal_encontrada.append(palabra.texto)
                    if palabra.texto not in dist_pal_procesadas:
                        dist_pal_procesadas.append(palabra.texto)
                elif palabra.estado == 2:
                    if palabra.texto not in dist_pal_confirmada:
                        dist_pal_confirmada.append(palabra.texto)
                    if palabra.texto not in dist_pal_procesadas:
                        dist_pal_procesadas.append(palabra.texto)
                elif palabra.estado == 3:
                    incompleto = True
                    if palabra.texto not in dist_pal_no_encontrada:
                        dist_pal_no_encontrada.append(palabra.texto)
                    if palabra.texto not in dist_pal_procesadas:
                        dist_pal_procesadas.append(palabra.texto)

            if incompleto:
                n_tests_incompletos += 1
            else:
                n_tests_completos += 1

        self.tests_completos = n_tests_completos
        self.tests_incompletos = n_tests_incompletos
        self.palabras_inicial = len(dist_pal_inicial)
        self.palabras_encontradas = len(dist_pal_encontrada)
        self.palabras_confirmadas = len(dist_pal_confirmada)
        self.palabras_no_encontradas = len(dist_pal_no_encontrada)
        self.palabras_totales = len(dist_pal)
        self.palabras_procesadas = len(dist_pal_procesadas)

    def extraer_tests(self):
        tests = []
        fichero = io.open(self.configuracion.fichero.get(), "r", encoding="UTF-8")
        for i, linea in enumerate(fichero.readlines()):
            # print(linea)
            tests.append(Test(linea, self.configuracion.categoria.get(), i))
        fichero.close()
        return tests

    def conectar_db(self):
        mongodb_url = self.configuracion.bd.get()
        if len(mongodb_url) == 0:
            # print("Conectando con mongoDB por defecto (mongodb://localhost:27017/db)")
            self.session = ODMSession(bind=create_datastore("mongodb://localhost:27017/db"))
        else:
            # print("Conectando con mongoDB para la dirección: " + mongodb_url)
            self.session = ODMSession(bind=create_datastore(mongodb_url))

        if self.configuracion.categoria.get() == 0:
            self.collection = collection("animales", self.session)
            self.mapper = Mapper(modelo_datos.Animal, self.collection, self.session)
            self.entity = entities.entity_animal
        elif self.configuracion.categoria.get() == 1:
            self.collection = collection("plantas", self.session)
            self.mapper = Mapper(modelo_datos.Planta, self.collection, self.session)
            self.entity = entities.entity_plant
        elif self.configuracion.categoria.get() == 2:
            self.collection = collection("vehiculos", self.session)
            self.mapper = Mapper(modelo_datos.Vehiculo, self.collection, self.session)
            self.entity = entities.entity_vehicle
        elif self.configuracion.categoria.get() == 3:
            self.collection = collection("prendas", self.session)
            self.mapper = Mapper(modelo_datos.Prenda, self.collection, self.session)
            self.entity = entities.entity_clothing
        self.mapper.compile_all()

    def procesar_palabra(self):
        """Procesa la siguiente palabra del test actual"""
        palabra = self.tests[self.current_test].palabras[self.current_palabra]
        etiqueta = wikidata.actual_word(palabra.texto)

        # ¿Está el label en la base de datos?
        docs = self.mapper.mapped_class.query.find({"etiqueta": etiqueta}).all()

        if len(docs) == 0:
            print("La BD no contiene la etiqueta principal, buscando por etiquetas alternativas")
            docs = self.mapper.mapped_class.query.find({"etiquetas": etiqueta}).all()

        if len(docs) > 0:
            if len(docs) > 1:
                print("La BD contiene más de un documento con este label")
            if len(docs) == 1:
                print("La BD contiene una entrada con este label")
                self.tests[self.current_test].palabras[self.current_palabra].estado = 2
                self.tests[self.current_test].palabras[self.current_palabra].objeto = docs[0]
        else:
            print("la BD no contiene la etiqueta")
            resultados = wikidata.search_wikidata(palabra.texto, self.entity)
            if resultados:
                objeto = None
                for label, entity_uri in resultados.items():
                    descripcion = wikidata.get_description(entity_uri)
                    # print(descripcion)
                    labels = wikidata.get_labels(entity_uri)
                    # print(labels)
                    objeto = self.crear_objeto(etiqueta=etiqueta, etiquetas=labels, descripcion=descripcion,
                                          categoria=self.entity, uri=entity_uri)
                    subcategorias = wikidata.get_subcategories(entity_uri, self.entity)
                    print(subcategorias)
                    # TODO - Incluir procesado de subcategorías --> Se deberían pasar los objetos según modelo datos?
                self.tests[self.current_test].palabras[self.current_palabra].objeto = objeto
                self.tests[self.current_test].palabras[self.current_palabra].estado = 1
            else:
                self.tests[self.current_test].palabras[self.current_palabra].estado = 3

        self.estadistica_ejecucion()

        print(self.current_palabra, "CURRENT")
        if len(self.tests[self.current_test].palabras) > self.current_palabra + 1:
            self.current_palabra += 1
        else:
            self.current_test += 1
            self.current_palabra = 0
        print(self.current_palabra, "CURRENT NEXT")

    def crear_objeto(self, etiqueta, etiquetas, descripcion, uri, categoria):
        obj = None

        if categoria == entities.entity_animal:
            obj = modelo_datos.Animal()
        if categoria == entities.entity_clothing:
            obj = modelo_datos.Prenda()
        if categoria == entities.entity_plant:
            obj = modelo_datos.Planta()
        if categoria == entities.entity_vehicle:
            obj = modelo_datos.Vehiculo()

        print(obj)

        obj.uri = uri
        obj.etiquetas = etiquetas
        obj.etiqueta = etiqueta
        obj.descipcion = descripcion
        return obj

    def actualizar_palabras(self, etiqueta, estado, objeto):
        for test in self.tests:
            for palabra in test.palabras:
                if palabra.texto == etiqueta:
                    palabra.estado = estado
                    palabra.objeto = objeto

    def actualizar_tests(self):
        for test in self.tests:
            inicial = True
            intermedio = False
            for palabra in test.palabras:
                if palabra.estado != 0:
                    inicial = False
                if (palabra.estado == 1) or (palabra.estado == 3):
                    intermedio = True
            if inicial:
                test.estado = 0
            elif intermedio:
                test.estado = 1
            else:
                test.estado = 3

class Test:
    def __init__(self, linea, categoria, test_index, estado=None):
        palabras = []
        campos = linea.split(",")
        if re.match(r"[0-9][0-9][0-9]Ev[0-9]", campos[0]):
            test = campos[0]
            pos = 0
            for palabra in campos[1:]:
                pos = pos + 1
                if palabra.startswith("*"):
                    palabras.append(Palabra(test, palabra[1:], pos, test_index, tipo="rechazada"))
                if palabra.startswith("(") and palabra.endswith(")"):
                    palabras.append(Palabra(test, palabra[1:-1], pos, test_index, tipo="rechazada"))
                elif "?" in palabra:
                    palabras.append(Palabra(test, "UNK", pos, test_index, tipo="desconocida"))
                else:
                    palabras.append(Palabra(test, palabra, pos, test_index, tipo="aceptada"))

            self.palabras = palabras
            self.texto = ",".join(campos[1:])
            self.id = test
            self.estado = estado
            self.categoria = categoria
        else:
            print("N/A")
            self.estado = "N/A"


class Palabra:
    def __init__(self, test, texto, posicion, test_index, tipo=None, estado=0, objeto=None):
        self.test = test
        self.texto = texto
        self.posicion = posicion
        self.tipo = tipo
        self.estado = estado
        self.test_index = test_index
        self.objeto = objeto


class Fichero:
    def __init__(self, ruta_fichero):
        self.nombre_fichero = ruta_fichero
        self.n_lineas = None
        self.tokens_distintos = None
        self.tokens_rechazados = None
        self.lineas_invalidas = None
        self.n_tokens = None
        self.n_tokens_desconocidos = None
        self.estadisticas_fichero()

    def estadisticas_fichero(self):
        # Leer el fichero y comprobar que cumple formato
        fichero = io.open(self.nombre_fichero, "r", encoding="UTF-8")
        dist_tokens = []
        dist_tokens_rechazados = []
        lineas_invalidas = []
        n_tokens = 0
        n_dist_tokens = 0
        n_tokens_rechazados = 0
        n_dist_tokens_rechazados = 0
        n_tokens_desconocidos = 0
        n_linea = 0
        for linea in fichero.readlines():
            n_linea += 1
            campos = linea.split(",")
            if re.match(r"[0-9][0-9][0-9]Ev[0-9]]", campos[0]):
                for palabra in campos[1:]:
                    if palabra.startswith("*"):
                        n_tokens_rechazados += 1
                        if palabra[1:] not in dist_tokens_rechazados:
                            dist_tokens_rechazados.append([palabra[1:]])
                            n_dist_tokens_rechazados += 1
                    if palabra.startswith("(") and palabra.endswith(")"):
                        n_tokens_rechazados += 1
                        if palabra[1:-1] not in dist_tokens_rechazados:
                            dist_tokens_rechazados.append([palabra[1:-1]])
                            n_dist_tokens_rechazados += 1
                    elif "?" in palabra:
                        n_tokens_desconocidos += 1
                    else:
                        n_tokens += 1
                        if palabra not in dist_tokens:
                            dist_tokens.append(palabra)
                            n_dist_tokens += 1
            else:
                lineas_invalidas.append(n_linea)

        self.n_lineas = n_linea
        self.tokens_distintos = dist_tokens
        self.tokens_rechazados = dist_tokens_rechazados
        self.lineas_invalidas = lineas_invalidas
        self.n_tokens = n_tokens
        self.n_tokens_desconocidos = n_tokens_desconocidos
        fichero.close()
