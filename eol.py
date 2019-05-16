import requests
import re


eol_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoib2toYWxpbDFAYWx1bW5vLnVuZWQuZXMiLCJlbmNyeXB0ZWRfcGFz" \
          "c3dvcmQiOiIkMmEkMTEkMUdYZzVIVDBVbC9GT2dQclZ3TjI0T1AvZElZek9salpGSWlkLlZzTWNJaURmc25vSlh4d20ifQ.X9iCTca" \
          "an9I1VuLASm4OQHqZgnhcemBZ1z6fyV1Gph8"


def get_objects(subj_id, props):

    headers = {"Authorization": "JWT " + eol_key}

    for prop in props:
        print("Resultados de la propiedad {0} para el sujeto {1}").format(prop, subj_id)

        query_props = "MATCH (p:Page {page_id: #SBJ#})-[:trait]->(t0:Trait), (t0:Trait)-[:predicate]->(tp0:Term) WHERE " \
                  "tp0.uri = '#PRED#' OPTIONAL MATCH (t0)-[:object_term]->(obj:Term) " \
                  "RETURN DISTINCT obj.name, obj.uri LIMIT 50"

        query = query_props.replace("#SBJ#", subj_id)
        query = query.replace("#PRED#", prop)

        parameters = {"query": query, "format": "csv"}

        result = requests.get("https://eol.org/service/cypher", params=parameters, headers=headers).content
        raw_lines = result.decode("UTF-8")
        lines = raw_lines.split("\n")
        for line in lines[1:]:
            if "," in line:
                print(line.split(",")[0])
                print(line.split(",")[1])
    return 1


def test_identifier(subj_id):
    url = "http://eol.org/pages/" + subj_id
    response = requests.get(url)
    if response.status_code == 200:
        return True
    return False


def get_eol_objects(subj_id, prop_uri):
    query = "MATCH (p:Page {page_id: #SBJ#})-[:trait]->(t0:Trait), (t0:Trait)-[:predicate]->(tp0:Term) WHERE " \
              "tp0.uri = '#PRED#' OPTIONAL MATCH (t0)-[:object_term]->(obj:Term) " \
              "RETURN DISTINCT obj.name, obj.uri LIMIT 100"

    query = re.sub("#SBJ#", subj_id, query)
    query = re.sub("#PRED#", prop_uri, query)

    objects = []

    headers = {"Authorization": "JWT " + eol_key}
    parameters = {"query": query, "format": "csv"}
    result = requests.get("https://eol.org/service/cypher", params=parameters, headers=headers).content
    raw_lines = result.decode("UTF-8")
    lines = raw_lines.split("\n")
    if len(lines) > 1:
        for line in lines[1:]:
            if "," in line:
                result_object = {"label": line.split(",")[0], "@id": line.split(",")[1]}
                objects.append(result_object)
    return objects
