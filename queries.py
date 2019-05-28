# Categoría de plantas y animales
query_ask = 'ASK WHERE{ <#SPECIE#> wdt:P171* #ENTITY#. }'
query_subclass = 'ASK WHERE{ <#SPECIE#> wdt:P279* #ENTITY#}'
query_product = 'SELECT ?taxon WHERE{<#ENTITY#> wdt:P1582 ?taxon.}'
query_labels_species = 'SELECT DISTINCT ?specie ?label WHERE{ ' \
               'VALUES ?prop {rdfs:label skos:altLabel skos:prefLabel schema:name wdt:P1843 wdt:P225} ' \
               '?specie ?prop "#QUERY#"@es.}'
query_labels = 'SELECT DISTINCT ?item ?label WHERE{ ' \
               'VALUES ?prop {rdfs:label skos:altLabel skos:prefLabel schema:name schema:description} ' \
               '?item ?prop "#QUERY#"@es.}'
query_eol_identifier = "SELECT ?id WHERE { <#SPECIE#> wdt:P830 ?id. } LIMIT 10"
query_animal_use = "ASK WHERE { <#SPECIE#> ?pred ?tipo. ?tipo wdt:P171* ?parent. ?parent wdt:P279* ?clase. " \
                   "?clase ?predicate #ENTITY#. VALUES ?pred {wdt:P31 wdt:P279}}"
query_ask_common = 'ASK WHERE{ <#SPECIE#> wdt:P31 wd:Q55983715. }'
query_parent_classes_taxon = 'SELECT DISTINCT ?taxon WHERE { <#SPECIE#> wdt:P279* ?taxon. ?taxon wdt:P31 wd:Q16521. }'

# Subcategorías de plantas
query_tipo_planta_1 = "ASK WHERE{ <#ENTITY#> ?instancia_o_subclase #TYPE#. VALUES ?instancia_o_subclase " \
                      "{wdt:P31 wdt:P279} }"
query_tipo_planta_2 = "ASK WHERE{ <#ENTITY#> wdt:P171* ?taxon. ?taxon ?instancia_o_subclase #TYPE#. " \
                      "VALUES ?instancia_o_subclase {wdt:P31 wdt:P279} }"
query_tipo_planta_3 = "ASK WHERE{ <#ENTITY#> wdt:P1582 ?taxon. ?taxon wdt:P171* ?taxon_padre. " \
                      "?taxon_padre ?instancia_o_subclase #TYPE#. VALUES ?instancia_o_subclase {wdt:P31 wdt:P279} }"
query_tipo_planta_4 = "ASK WHERE{ <#ENTITY> wdt:P279* #TYPE# }"

query_ask_planta_1 = "ASK WHERE{ <#ENTITY#> wdt:P171* #TYPE#} "
query_ask_planta_2 = "ASK WHERE{ <#ENTITY#> wdt:P1582 ?taxon. ?taxon wdt:P171* #TYPE#}"
query_ask_planta_3 = "ASk WHERE{ <#ENTITY#> wdt:P279* #TYPE#}"
query_ask_planta_4 = "ASK WHERE { <#ENTITY#> wdt:P171* ?tipo. ?tipo wdt:P279* #TYPE#}"
query_ask_planta_5 = "ASK WHERE { <#ENTITY#> wdt:P1582 ?taxon. ?taxon wdt:P171* ?tipo. ?tipo wdt:P279* #TYPE#}"

# Categoría de vehículos
query_ask_transport_1 = "ASK WHERE {<#VEHICLE#> wdt:P31 ?clase. ?clase wdt:P279* wd:Q334166.}"
query_ask_transport_2 = "ASK WHERE {<#VEHICLE#> wdt:P31 wd:Q334166.}"
query_ask_transport_3 = "ASK WHERE {<#VEHICLE#> wdt:P279* wd:Q334166.}"
query_ask_transport_4 = "ASK WHERE {<#VEHICLE#> wdt:P279* ?instancia. ?instancia wdt:P31 wd:Q334166.}"
query_ask_vehicle_1 = "ASK WHERE {<#VEHICLE#> wdt:P31 ?clase. ?clase wdt:P279* wd:Q42889.}"
query_ask_vehicle_2 = "ASK WHERE {<#VEHICLE#> wdt:P31 wd:Q42889}"
query_ask_vehicle_3 = "ASK WHERE {<#VEHICLE#> wdt:P279* wd:Q42889}"
query_ask_vehicle_4 = "ASK WHERE {<#VEHICLE#> wdt:P279* ?instancia. ?instancia wdt:P31 wd:Q42889.}"

query_tipo_vehiculo_1 = "ASK WHERE{<#ENTITY#> wdt:P279* #TYPE#}"
query_tipo_vehiculo_2 = "ASK WHERE{<#ENTITY#> wdt:P31 #TYPE#}"
query_tipo_vehiculo_3 = "ASK WHERE{?clase wdt:P279* #TYPE#. <#ENTITY#> wdt:P31 ?clase}"

# Categoría de ropa
query_clothing_1 = "ASK WHERE {<#CLOTHING#> wdt:P31 ?clase. ?clase wdt:P279* wd:Q11460.}"
query_clothing_2 = "ASK WHERE {<#CLOTHING#> wdt:P31 wd:Q11460.}"
query_clothing_3 = "ASK WHERE {<#CLOTHING#> wdt:P279* wd:Q11460.}"
query_clothing_4 = "ASK WHERE {<#CLOTHING#> wdt:P279* ?instancia. ?instancia wdt:P31 wd:Q11460.}"

query_tipo_ropa_1 = "ASK WHERE{<#ENTITY#> wdt:P279* #TYPE#}"
query_tipo_ropa_2 = "ASK WHERE{<#ENTITY#> wdt:P31 #TYPE#}"
query_tipo_ropa_3 = "ASK WHERE{?clase wdt:P279* #TYPE#. <#ENTITY#> wdt:P31 ?clase}"

# Categoría genérica
query_retrieve_labels = "SELECT ?label WHERE{ <#ENTITY#> ?prop_label ?label. " \
                        "VALUES ?prop_label {rdfs:label skos:altLabel skos:prefLabel schema:name wdt:P1843} " \
                        "FILTER(lang(?label)='es') }"
query_retrieve_description = "SELECT ?description WHERE{ <#ENTITY#> schema:description ?description. " \
                             "FILTER(lang(?description)='es') }"
