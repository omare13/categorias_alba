import requests
import re
import queries
import entities
import eol


def is_good_label(palabra):
    if palabra[0] == "(" and palabra[len(palabra)-1] == ")":
        return False
    else:
        return True


def actual_word(palabra):
    palabra = palabra.strip()
    if palabra[0] == "(" and palabra[len(palabra) - 1] == ")":
        return palabra[1:-1]
    elif "*" in palabra:
        return None
    else:
        return palabra.strip()


def search_label(query, category_data):
    results = []
    for label in list(category_data.keys()):
        if query == label:
            results.append({label: category_data.get(label)})

    if len(results) >= 1:
        # print(results[0])
        return results[0]
    else:
        return None


def remove_accents(term):
    term = re.sub("á", "a", term)
    term = re.sub("é", "e", term)
    term = re.sub("í", "i", term)
    term = re.sub("ó", "o", term)
    term = re.sub("ú", "u", term)
    return term


def get_variants(term):
    variants = []
    term_con_acentos = term.lower()
    term_sin_acentos = remove_accents(term)

    # Variantes con la primera mayúscula
    term_con_upper = "".join([term_con_acentos[0].upper()+term_con_acentos[1:]])
    term_sin_upper = "".join([term_sin_acentos[0].upper()+term_sin_acentos[1:]])

    variants.append(term_con_acentos)
    variants.append(term_sin_acentos)

    if term_con_upper not in variants:
        variants.append(term_con_upper)
    if term_sin_upper not in variants:
        variants.append(term_sin_upper)
    # Get variantes búsqueda wikipedia
    return variants


def execute_sparql_query(query):

    # print(query)

    endpoint = 'https://query.wikidata.org/sparql'
    params = {
        'query': query
    }
    headers = {
        'Accept': 'application/sparql-results+json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:59.0) Gecko/20100101 Firefox/59.0'
    }

    response = requests.get(endpoint, params=params, headers=headers)
    response.raise_for_status()
    results = response.json()
    return results


def is_parent_taxon_of(entity_animal, entity_taxon):
    query = re.sub("#SPECIE#", entity_animal, queries.query_ask)
    query = re.sub("#ENTITY#", entity_taxon, query)
    # print(query)
    results = execute_sparql_query(query)
    result = results['boolean']
    return bool(result)


def is_zoological_category(entity_uri, category_uri):
    query = re.sub("#SPECIE#", entity_uri, queries.query_parent_classes_taxon)
    results = execute_sparql_query(query)
    for result in results["results"]["bindings"]:
        # print("Parent taxon zoological category: " + result["taxon"]["value"])
        entity_superclass = result["taxon"]["value"]
        if is_parent_taxon_of(entity_superclass, category_uri):
            return True
    return False


def is_category(entity_uri, category_entity):
    query = re.sub("#SPECIE#", entity_uri, queries.query_ask)
    query = re.sub("#ENTITY#", category_entity, query)
    results = execute_sparql_query(query)
    result = results['boolean']
    return bool(result)


def is_common_name_specie(entity_uri):
    query = re.sub("#SPECIE#", entity_uri, queries.query_ask_common)
    results = execute_sparql_query(query)
    result = results['boolean']
    return bool(result)


def is_product_of_category(entity_uri, category_entity):
    query = re.sub("#ENTITY#", entity_uri, queries.query_product)
    results = execute_sparql_query(query)
    if len(results["results"]["bindings"]) > 0:
        for result in results["results"]["bindings"]:
            taxon_entity = result["taxon"]["value"]
            if is_category(taxon_entity, category_entity):
                return True
    return False


def is_subclass_of_category(entity_uri, category_entity):
    query = re.sub("#SPECIE#", entity_uri, queries.query_subclass)
    query = re.sub("#ENTITY#", category_entity, query)
    results = execute_sparql_query(query)
    result = results['boolean']
    return bool(result)


def lematize_word(query, lemmas):
    if query in lemmas.keys():
        lema = lemmas.get(query)
        # print("LEMA : ", lema)
        return lema


def get_lemmas(path_to_lemmas):
    lemma_data = {}
    with open(path_to_lemmas, "r", encoding='UTF-8') as file:
        lineas = file.readlines()
        for linea in lineas:
            lemma = linea.split("\t")[0].strip()
            wordform = linea.split("\t")[1].strip()
            lemma_data.update({wordform: lemma})
    # print(lemmas)
    return lemma_data


def is_subclass_of_taxon_in_category(entity_uri, taxon_uri):
    query = re.sub("#SPECIE#", entity_uri, queries.query_parent_classes_taxon)
    results = execute_sparql_query(query)
    if len(results["results"]["bindings"]) > 0:
        for result in results["results"]["bindings"]:
            entity_uri = result["taxon"]["value"]
            if is_category(entity_uri, taxon_uri):
                return True
    return False


def is_for_human_use(entity_uri, type_of_use_id):
    query = re.sub("#SPECIE#", entity_uri, queries.query_animal_use)
    query = re.sub("#ENTITY#", type_of_use_id, query)
    results = execute_sparql_query(query)
    result = results['boolean']
    if bool(result):
        return True
    return False


def is_transport(entity_uri):
    for query_transport in [queries.query_ask_transport_1, queries.query_ask_transport_2,
                            queries.query_ask_transport_3, queries.query_ask_transport_4]:
        query = re.sub("#VEHICLE#", entity_uri, query_transport)
        results = execute_sparql_query(query)
        result = results['boolean']
        if bool(result):
            return True
    return False


def is_vehicle(entity_uri):
    for query_vehicle in [queries.query_ask_vehicle_1, queries.query_ask_vehicle_2,
                          queries.query_ask_vehicle_3, queries.query_ask_vehicle_4]:
        query = re.sub("#VEHICLE#", entity_uri, query_vehicle)
        results = execute_sparql_query(query)
        result = results['boolean']
        if bool(result):
            return True
    return False


def is_clothing(entity_uri):
    for query_clothing in [queries.query_clothing_1, queries.query_clothing_2,
                           queries.query_clothing_3, queries.query_clothing_4]:
        query = re.sub("#CLOTHING#", entity_uri, query_clothing)
        results = execute_sparql_query(query)
        result = results['boolean']
        if bool(result):
            return True
    return False


def search_wikidata_plant(term, category_entity):
    variants = get_variants(term)
    # print(variants)
    for variant in variants:
        query = re.sub("#QUERY#", variant, queries.query_labels_species)
        results = execute_sparql_query(query)
        if len(results["results"]["bindings"]) > 0:
            for result in results["results"]["bindings"]:
                entity_uri = result["specie"]["value"]
                if is_category(entity_uri, category_entity):
                    return {term: entity_uri}
                elif is_product_of_category(entity_uri, category_entity):
                    return {term: entity_uri}
                elif is_subclass_of_category(entity_uri, category_entity):
                    return {term: entity_uri}
    return None


def search_wikidata(term, category_entity):
    term = actual_word(term)
    if category_entity == entities.entity_plant:
        return search_wikidata_plant(term, category_entity)
    elif category_entity == entities.entity_animal:
        return search_wikidata_animal(term, category_entity)
    elif category_entity == entities.entity_clothing:
        return search_wikidata_clothing(term)
    elif category_entity == entities.entity_vehicle:
        return search_wikidata_vehicle(term)
    else:
        return None


def search_wikidata_vehicle(term):
    variants = get_variants(term)
    # print(variants)
    for variant in variants:
        query = re.sub("#QUERY#", variant, queries.query_labels)
        results = execute_sparql_query(query)
        if len(results["results"]["bindings"]) > 0:
            for result in results["results"]["bindings"]:
                entity_uri = result["item"]["value"]
                if is_transport(entity_uri):
                    return {term: entity_uri}
                elif is_vehicle(entity_uri):
                    return {term: entity_uri}

    return None


def search_wikidata_clothing(term):
    variants = get_variants(term)
    # print(variants)
    for variant in variants:
        query = re.sub("#QUERY#", variant, queries.query_labels)
        results = execute_sparql_query(query)
        if len(results["results"]["bindings"]) > 0:
            for result in results["results"]["bindings"]:
                entity_uri = result["item"]["value"]
                if is_clothing(entity_uri):
                    return {term: entity_uri}

    return None


def search_wikidata_animal(term, category_entity):
    variants = get_variants(term)
    # print(variants)
    for variant in variants:
        query = re.sub("#QUERY#", variant, queries.query_labels_species)
        print(query)
        results = execute_sparql_query(query)
        print(results)
        if len(results["results"]["bindings"]) > 0:
            for result in results["results"]["bindings"]:
                entity_uri = result["specie"]["value"]

                if is_category(entity_uri, category_entity):
                    return {term: entity_uri}

                elif is_common_name_specie(entity_uri):
                    return {term: entity_uri}

                elif is_subclass_of_category(entity_uri, category_entity):
                    return {term: entity_uri}

                elif is_subclass_of_taxon_in_category(entity_uri, category_entity):
                    return {term: entity_uri}

                # elif is_product_of_category(entity_uri, category_entity):
                #     return {term: entity_uri}

    return None


def get_animal_subcategories(entity_uri):
    subcategorias_taxon = zoological_categories(entity_uri)
    subcategorias_human_use = human_use_categories(entity_uri)
    subcategorias_eol = get_eol_categories(entity_uri)
    print(subcategorias_taxon)
    print(subcategorias_human_use)
    print(subcategorias_eol)


def get_eol_ids(entity_uri):
    query = re.sub("#SPECIE#", entity_uri, queries.query_eol_identifier)
    results = execute_sparql_query(query)
    eol_ids = []
    if len(results["results"]["bindings"]) > 0:
        for result in results["results"]["bindings"]:
            eol_id = result["id"]["value"]
            eol_ids.append(eol_id)

    return eol_ids


def get_eol_categories(entity_uri):
    # Cojo el(los identificador/es de la entidad en EOL
    eol_ids = get_eol_ids(entity_uri)

    # Diccionario a devolver
    entity_eol_categories = {}

    # Tengo un diccionario con las subcategorías
    eol_categories = {"http://eol.org/schema/terms/Habitat": "habitat_includes",
                      "http://rs.tdwg.org/dwc/terms/habitat": "habitat_is",
                      "http://purl.obolibrary.org/obo/GAZ_00000071": "biogeographic_realm",
                      "https://www.wikidata.org/wiki/Q295469": "ecoregion",
                      "http://www.wikidata.org/entity/Q1053008": "trophic_level_wikidata",
                      "http://eol.org/schema/terms/TrophicLevel": "trophic_level_eol"}

    for eol_id in eol_ids:
        if eol.test_identifier(eol_id):
            for cat_uri, cat_name in eol_categories.items():
                eol_objects = eol.get_eol_objects(eol_id, cat_uri)
                if len(eol_objects) > 0:
                    entity_eol_categories.update({cat_name: eol_objects})
            return entity_eol_categories

    return entity_eol_categories


def human_use_categories(entity_uri):
    """Devuelve un diccionario indicando las categorías de uso humano a las que el animal pertenece"""
    # Diccionario a devolver
    entity_human_use_cats = {}

    # Tengo un diccionario con las subcategorías
    human_use_cats = {"wd:Q1797813": "productive", "wd:Q228534": "working", "wd:Q622377": "pack",
                      "wd:Q11637629": "draft", "wd:Q622852": "domesticated", "wd:Q39201": "mascota"}

    for cat_id, cat_name in human_use_cats.items():
        if is_for_human_use(entity_uri, cat_id):
            entity_human_use_cats.update({cat_name: 1})
        else:
            entity_human_use_cats.update({cat_name: 0})

    return entity_human_use_cats


def zoological_categories(entity_uri):
    """Devuelve un diccionario indicando las superespecies a las que pertenece un animal dado por su uri"""
    # Diccionario a devolver
    entity_zool_cats = {}

    # Tengo un diccionario con las subcategorías
    zool_cats = {"wd:Q5113": "bird", "wd:Q22724": "bovine", "wd:Q25324": "canine", "wd:Q23390": "deer",
                 "wd:Q25265": "feline", "wd:Q152": "fish", "wd:Q1390": "insect", "wd:Q7380": "primate",
                 "wd:Q25900": "rabbit", "wd:Q10811": "reptile", "wd:Q10908": "amphibian", "wd:Q10850": "rodent",
                 "wd:Q28521": "weasel"}
    for cat_id, cat_name in zool_cats.items():
        if is_zoological_category(entity_uri, cat_id):
            entity_zool_cats.update({cat_name: 1})
        else:
            entity_zool_cats.update({cat_name: 0})

    return entity_zool_cats


def get_description(entity_uri):
    query = re.sub("#ENTITY#", entity_uri, queries.query_retrieve_description)
    results = execute_sparql_query(query)
    if results["results"]["bindings"]:
        return results["results"]["bindings"][0]["description"]["value"]


def get_labels(entity_uri):
    labels = []
    query = re.sub("#ENTITY#", entity_uri, queries.query_retrieve_labels)
    results = execute_sparql_query(query)
    if len(results["results"]["bindings"]) > 0:
        for result in results["results"]["bindings"]:
            label = result["label"]["value"]
            labels.append(label)
    return labels


def get_subcategories(entity_uri, category_entity):
    if category_entity == entities.entity_animal:
        return get_animal_subcategories(entity_uri)


loaded_lemmas = get_lemmas("lemmatization-es.txt")
