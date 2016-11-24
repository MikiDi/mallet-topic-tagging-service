#!usr/bin/python3
import os
import rdflib

import helpers

from . import mallet_tools

def trainingset_topics_query(path):
    """
    Build a SPARQL-query that imports the MALLET-topic id's and their
    corresponding keywords for a certain trainingset-file.
    Takes the path to the trainingset's keys.txt-file
    """
    mu_uri = "http://mu.semte.ch/vocabularies/ext/topic-tools/"
    voc_ns = rdflib.namespace.Namespace(mu_uri + "voc/")
    # res_ns = rdflib.namespace.Namespace(mu_uri + "resources/")
    graph = rdflib.graph.Graph()

    for topic_id, threshold, keywords in mallet_tools.parse_topicfile(path):
        topic_uri = rdflib.term.URIRef(mu_uri + "resources/" + "malletTopic/" +
            str(topic_id))
        graph.add((topic_uri, # type MalletTopic
                   rdflib.namespace.RDF["type"],
                   voc_ns["MalletTopic"]))
        graph.add((topic_uri, # Topic id
                   voc_ns["hasTopicId"],
                   rdflib.term.Literal(topic_id)))
        graph.add((topic_uri, # Topic string
                   voc_ns["hasTopicString"],
                   rdflib.term.Literal(''.join(keywords))))

    serialized_triples = graph.serialize(format='nt')
    return """
    INSERT DATA {{
        GRAPH <{0}> {{
            {1}
        }}
    }}
    """.format(os.getenv('MU_APPLICATION_GRAPH'), serialized_triples)

if __name__ == "__main__":
    path = os.path.join(os.getenv('TRAIN_PATH'), "topics/keys.txt")
    query = trainingset_topics_query(path)
    print("Inserting query:", query)
    try:
        helpers.update(query)
    except Exception as e:
        helpers.log("Querying SPARQL-endpoint failed:\n" + str(e))
