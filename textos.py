import entities
import interfaz


class TextoInformacion:
    def __init__(self):
        self.titulo = "Información Sobre la Aplicación"
        self.descripcion = "Aplicación creada para las anotaciones"


regex_fichero = r'^([a-zA-Z]\:|\\\\[^\/\\:*?"<>|]+\\[^\/\\:*?"<>|]+)(\\[^\/\\:*?"<>|]+)+(\.[^\/\\:*?"<>|]+)$'
regex_carpeta = r'^(?:\.{2})?(?:\/\.{2})*(\/[a-zA-Z0-9]+)+$'


campos = {entities.entity_animal: {
                "_id": "Identificador",
                "etiqueta": "Etiqueta Principal",
                "etiquetas": "Etiquetas Válidas",
                "descripcion": "Descripción de la entidad",
                "uri": "URI",
                "eol_id": "Identificador en EOL",
                "nivel_trofico": "Nivel Trófico",
                "habitat": "Hábitat Principal",
                "habitat_incluye": "Hábitats",
                "taxon_comun": "Taxón Común"
            }, entities.entity_plant: {
                "_id": "Identificador",
                "etiqueta": "Etiqueta Principal",
                "etiquetas": "Etiquetas Válidas",
                "descripcion": "Descripción de la entidad",
                "uri": "URI",
                "tipo": "Tipo de planta",
                "vegetal": "Tipo de vegetal"
            }, entities.entity_vehicle: {
                "_id": "Identificador",
                "etiqueta": "Etiqueta Principal",
                "etiquetas": "Etiquetas Válidas",
                "descripcion": "Descripción de la entidad",
                "uri": "URI",
                "tipo": "Tipo de transporte",
            }, entities.entity_clothing: {
                "_id": "Identificador",
                "etiqueta": "Etiqueta Principal",
                "etiquetas": "Etiquetas Válidas",
                "descripcion": "Descripción de la entidad",
                "uri": "URI",
                "tipo": "Tipo de prenda"
}}


displays = {entities.entity_animal: {
                "_id": interfaz.EntryIO,
                "etiqueta": interfaz.EntryIO,
                "etiquetas": interfaz.TextIO,
                "descripcion": interfaz.EntryIO,
                "uri": interfaz.EntryIO,
                "eol_id": interfaz.EntryIO,
                "nivel_trofico": interfaz.RadioIO,
                "habitat": interfaz.SingleTreeIO,
                "habitat_incluye": interfaz.MultipleTreeIO,
                "taxon_comun": interfaz.RadioIO,
                "tipo_uso": interfaz.MultipleOptionIO
            },
            entities.entity_plant: {
                "_id": interfaz.EntryIO,
                "etiqueta": interfaz.EntryIO,
                "etiquetas": interfaz.TextIO,
                "descripcion": interfaz.EntryIO,
                "uri": interfaz.EntryIO,
                "tipo": interfaz.RadioIO,
                "vegetal": interfaz.RadioIO
            },
            entities.entity_vehicle: {
                "_id": interfaz.EntryIO,
                "etiqueta": interfaz.EntryIO,
                "etiquetas": interfaz.TextIO,
                "descripcion": interfaz.EntryIO,
                "uri": interfaz.EntryIO,
                "tipo": interfaz.MultipleOptionIO
            },
            entities.entity_clothing: {
                "_id": interfaz.EntryIO,
                "etiqueta": interfaz.EntryIO,
                "etiquetas": interfaz.TextIO,
                "descripcion": interfaz.EntryIO,
                "tipo": interfaz.RadioIO
            }}


opciones = {entities.entity_animal: {
                "nivel_trofico": entities.trophic_levels_wikidata,
                "habitat": entities.habitats_envo,
                "taxon_comun": entities.taxons,
                "habitat_incluye": entities.habitats_envo,
                "tipo_uso": entities.uso_animal
            },
            entities.entity_plant: {
                "tipo": entities.tipo_plantas,
                "vegetal": entities.vegetales
            },
            entities.entity_vehicle: {
                "tipo": entities.tipo_vehiculos
            },
            entities.entity_clothing: {
                "tipo": entities.tipo_prendas
            }}


mapeos = {entities.entity_animal: {
                "nivel_trofico": entities.trophic_levels_mapping,
                "habitat": entities.habitat_mapping}, entities.entity_plant: {}, entities.entity_vehicle: {},entities.entity_clothing: {}}
