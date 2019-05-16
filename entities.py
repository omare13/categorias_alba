import io
from rdflib import Graph, RDFS, URIRef
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
habitats_envo = []  # un árbol del tipo [{label:"biome", uri="http://uri.org/biom", hijos:[uri1, uri2, ...]},{}]
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
    dicctionario = taxon_from_node(grafo, biome)


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
    diccionario_base = {}
    labels = grafo.query(query_label, initBindings={"subject": URIRef(nodo_base)})
    hijos = grafo.query(query_sons, initBindings={"object": URIRef(nodo_base)})

    diccionario_base = {"uri": nodo_base, "label": labels[0], "hijos": hijos}


def recursive_sons(nodo):
    query_sons = rdflib.plugins.sparql.prepareQuery(
        "SELECT ?subject WHERE {?subject rdfs:subClassOf ?object.}",
        initNs={"rdfs": RDFS}
    )

# Main
print("Obteniendo datos sobre nivel trófico")
get_trophic_levels("trophic_levels.csv")
print(trophic_levels_mapping, "MAPPING_TROPHIC")
print(trophic_levels_wikidata, "WIKI")
print("Obteniendo datos sobre hábitats")
get_habitat_mappings("habitat_synonyms.csv")
print(habitat_mapping, "MAPPING_HABITAT")
print("Obteniendo datos sobre taxones")
# get_habitats("envo.owl")
# # print(habitat_mapping, "HABITATS")
# Comentario final
