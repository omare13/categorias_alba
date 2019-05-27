# Documentos de MongoDB son diccionarios python
# Ming permite que los documentos se representen por clases mapeadas

# Los imports necesarios para el mapeo de clases y definición de atributos:
from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty
# Mapper -> https://ming.readthedocs.io/en/latest/api/ming.odm.html#ming.odm.mapper.Mapper
# El mapeador mantiene información de las clases mapeadas para su relación con la validación
# El mapeador también compila las clases mapeadas si aún no lo han sido
# from ming.odm import Mapper


# Las clases que heredan de MappedClass definen el schema o modelo de datos
class Animal(MappedClass):
    _id = FieldProperty(schema.ObjectId)
    etiqueta = FieldProperty(schema.String)
    etiquetas = FieldProperty(schema.Array(schema.String))
    descripcion = FieldProperty(schema.String(if_missing=""))
    uri = FieldProperty(schema.String())
    eol_id = FieldProperty(schema.String())
    nivel_trofico = FieldProperty(schema.Object({
        "etiqueta": schema.String(required=False),
        "uri": schema.String(required=False)
    }))
    habitat_incluye = FieldProperty(schema.Array(schema.Object({
        "etiqueta": schema.String(required=False),
        "uri": schema.String(required=False)
    })))
    habitat = FieldProperty(schema.Object({
        "etiqueta": schema.String(required=False),
        "uri": schema.String(required=False)
    }))
    taxon_comun = FieldProperty(schema.Object({
        "etiqueta": schema.String(required=False),
        "uri": schema.String(required=False)
    }))
    tipo_uso = FieldProperty(schema.Array(schema.Object({
        "etiqueta": schema.String(required=False),
        "uri": schema.String(required=False)
    })))


class Planta(MappedClass):
    _id = FieldProperty(schema.ObjectId)
    etiqueta = FieldProperty(schema.String)
    etiquetas = FieldProperty(schema.Array(schema.String))
    descripcion = FieldProperty(schema.String(if_missing=""))
    uri = FieldProperty(schema.String())
    eol_id = FieldProperty(schema.String())
    tipo = FieldProperty(schema.Object({
        "etiqueta": schema.String(required=True),
        "uri": schema.String(required=True)
    }))
    vegetal = FieldProperty(schema.Object({
        "etiqueta": schema.String(required=True),
        "uri": schema.String(required=True)
    }))


class Vehiculo(MappedClass):
    _id = FieldProperty(schema.ObjectId)
    etiqueta = FieldProperty(schema.String)
    etiquetas = FieldProperty(schema.Array(schema.String))
    descripcion = FieldProperty(schema.String(if_missing=""))
    uri = FieldProperty(schema.String())
    tipo = FieldProperty(schema.Object({
        "etiqueta": schema.String(required=True),
        "uri": schema.String(required=True)
    }))


class Prenda(MappedClass):
    _id = FieldProperty(schema.ObjectId)
    etiqueta = FieldProperty(schema.String)
    etiquetas = FieldProperty(schema.Array(schema.String))
    descripcion = FieldProperty(schema.String(if_missing=""))
    uri = FieldProperty(schema.String())
    tipo = FieldProperty(schema.Object({
        "etiqueta": schema.String(required=True),
        "uri": schema.String(required=True)
    }))


# Al final del modelo de datos, se debe llamar a la compilación del mapeado
# Mapper.compile_all()
