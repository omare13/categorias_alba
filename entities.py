import io
from rdflib import Graph, RDFS, URIRef, Namespace
import rdflib.plugins.sparql

entity_animal = "wd:Q729"
entity_plant = "wd:Q756"
entity_clothing = "wd:Q11460"
entity_vehicle = "wd:Q334166"

environmental_condition = "http://purl.obolibrary.org/obo/ENVO_01000203"
biome = "http://purl.obolibrary.org/obo/ENVO_00000428"

entity_to_category_name = {"wd:Q729": "animal", "wd:Q756": "planta", "wd:Q11460": "prenda", "wd:Q334166": "transporte"}

trophic_levels_wikidata = {}  # pares del tipo label,uri_wikidata
trophic_levels_mapping = {}  # pares del tipo uri_externa,uri_wikidata
habitat_mapping = {}  # pares del tipo uri_externa,uri_envo
environmental_envo = []  # un árbol del tipo [{label:"environmental_condition", ...
# ... uri="http://uri.org/envcond", hijos:[uri1, uri2, ...]},{}]


taxons = {"http://www.wikidata.org/entity/Q5113": "bird",
          "http://www.wikidata.org/entity/Q22724": "ovis",
          "http://www.wikidata.org/entity/Q25324": "canidae",
          "http://www.wikidata.org/entity/Q23390": "cervidae",
          "http://www.wikidata.org/entity/Q25265": "felidae",
          "http://www.wikidata.org/entity/Q152": "fish",
          "http://www.wikidata.org/entity/Q1390": "insect",
          "http://www.wikidata.org/entity/Q7380": "primate",
          "http://www.wikidata.org/entity/Q25900": "leporidae",
          "http://www.wikidata.org/entity/Q10811": "reptilia",
          "http://www.wikidata.org/entity/Q10908": "amphibia",
          "http://www.wikidata.org/entity/Q10850": "rodentia",
          "http://www.wikidata.org/entity/Q28521": "mustela"
          }

uso_animal = {"http://www.wikidata.org/entity/Q1797813": "productive",
              "http://www.wikidata.org/entity/Q228534": "working",
              "http://www.wikidata.org/entity/Q622377": "pack",
              "http://www.wikidata.org/entity/Q11637629": "draft",
              "http://www.wikidata.org/entity/Q622852": "domesticated",
              "http://www.wikidata.org/entity/Q39201": "mascota"}


def get_trophic_levels(path_to_file):
    """El archivo de nivel trófico es un CSV con las columnas: label, uri preferida, uri sinónima"""
    file = io.open(path_to_file, "r", encoding="utf-8")
    for linea in file.readlines():
        campos = linea.split(",")
        if campos[1] not in trophic_levels_wikidata.values():
            trophic_levels_wikidata.update({campos[1]: campos[0]})
        if campos[2] not in trophic_levels_mapping.keys():
            trophic_levels_mapping.update({campos[1]: campos[2]})
    file.close()
    return


def get_habitat_mappings(path_to_file):
    """El archivo de sinónimos de hábitat es un CSV con las columnas: uri_envo,uri_envo_desfasada o uri_externa"""
    file = io.open(path_to_file, "r", encoding="utf-8")
    for linea in file.readlines():
        campos = linea.split(",")
        if campos[1] not in habitat_mapping.keys():
            habitat_mapping.update({campos[1]: campos[0]})
    file.close()
    return


def get_habitats(path_to_onto):
    """Este método extrae los hábitats de la ontología ENVO, cuya ruta se le pasa por parámetro"""
    grafo = file_to_rdf(path_to_onto)
    taxon = taxon_from_node(grafo, biome)
    return taxon


def file_to_rdf(path_to_file):
    """Devuelve una representacion rdflib de un grafo almacenado en el fichero indicado por el parámetro"""
    g = Graph()
    g.parse(path_to_file)
    return g


def taxon_from_node(grafo, nodo_base):
    taxon = []
    query_label = rdflib.plugins.sparql.prepareQuery(
        "SELECT ?label WHERE {?subject rdfs:label ?label.}",
        initNs={"rdfs": RDFS}
    )
    query_sons = rdflib.plugins.sparql.prepareQuery(
        "SELECT ?subject WHERE {?subject rdfs:subClassOf ?object.}",
        initNs={"rdfs": RDFS}
    )
    query_parent = rdflib.plugins.sparql.prepareQuery(
        "SELECT ?object WHERE {?subject rdfs:subClassOf ?object.}",
        initNs={"rdfs": RDFS}
    )
    query_description = rdflib.plugins.sparql.prepareQuery(
        "SELECT ?description WHERE {?subject obo:IAO_0000115 ?description.}",
        initNs={"obo": Namespace("http://purl.obolibrary.org/obo/")}
    )

    # Obtengo el label del nodo raíz y lo añado a la taxonomía
    labels_raiz = grafo.query(query_label, initBindings={"subject": URIRef(nodo_base)})
    label_raiz = "root"
    if len(labels_raiz) > 0:
        label_raiz = sparql_result_array(labels_raiz)[0]

    descriptions_raiz = sparql_result_array(grafo.query(query_description, initBindings={"subject": URIRef(nodo_base)}))
    description_raiz = ""
    if len(description_raiz) > 0:
        description_raiz = descriptions_raiz[0]

    dict_raiz = {"parent": "", "uri": nodo_base, "label": label_raiz, "description": description_raiz}
    taxon.append(dict_raiz)

    # Obtengo las subclases y las añado a la taxonomía
    clases_visitadas = []
    clases_restantes = []

    hijos = sparql_result_array(grafo.query(query_sons, initBindings={"object": URIRef(nodo_base)}))

    clases_restantes = clases_restantes + hijos
    clases_visitadas.append(URIRef(nodo_base))

    while len(clases_visitadas) < len(clases_restantes):
        for clase in clases_restantes:
            if clase not in clases_visitadas:
                description = ""
                parent = ""
                label = ""
                uri = str(clase)

                descriptions = sparql_result_array(grafo.query(query_description, initBindings={"subject": clase}))
                if len(descriptions) > 0:
                    description = str(descriptions[0])

                parents = sparql_result_array(grafo.query(query_parent, initBindings={"subject": clase}))
                if len(parents) > 0:
                    for element_result in parents:
                        if (type(element_result) == URIRef) and (element_result in clases_visitadas):
                            parent = element_result

                labels = sparql_result_array(grafo.query(query_label, initBindings={"subject": clase}))
                if len(labels) > 0:
                    label = str(labels[0])

                sons = sparql_result_array(grafo.query(query_sons, initBindings={"object": clase}))

                clases_visitadas.append(clase)
                clases_restantes = clases_restantes + sons
                taxon.append({"parent": parent, "uri": uri, "label": label, "description": description})

    return taxon

def sparql_result_array(sparqlresult):
    results = []
    for row in sparqlresult:
        results.append(row[0])
    return results

# Main
print("Obteniendo datos sobre nivel trófico")
get_trophic_levels("trophic_levels.csv")
print(trophic_levels_mapping, "MAPPING_TROPHIC")
print(trophic_levels_wikidata, "WIKI")
print("Obteniendo datos sobre hábitats")
get_habitat_mappings("habitat_synonyms.csv")
print(habitat_mapping, "MAPPING_HABITAT")
# print(habitat_mapping, "HABITATS")
print("Obteniendo taxonomía de hábitats ENVO")
habitats_envo = get_habitats("envo.owl")  # un árbol del tipo [{label:"biome", uri="http://uri.org/biom", hijos:[uri1, uri2, ...]},{}]
print(habitats_envo, "TAXON!!")
