import os
import subprocess
import textwrap
import rdflib
import helpers, escape_helpers
if not hasattr(subprocess, 'run'):# <python 3.5
    subprocess.run = subprocess.call

from . import mallet_tools

def build_select_query():
    return """
    PREFIX ost: <http://w3id.org/ost/ns#> #Open Standard for Tourism Ecosystems Data
    SELECT ?subject ?text WHERE {{
        GRAPH <{0}> {{
            ?event a ost:Event;
                ost:infoUrl ?subject.
            ?subject <{1}> ?text.
        }}
    }}
    """.format(os.getenv('MU_APPLICATION_GRAPH'),
               "http://mu.semte.ch/vocabularies/ext/topic-tools/voc/hasScrapedContent")

def build_insert_query(weights_by_subject):
    mu_uri = "http://mu.semte.ch/vocabularies/ext/topic-tools/"
    voc_ns = rdflib.namespace.Namespace(mu_uri + "voc/")
    res_ns = rdflib.namespace.Namespace(mu_uri + "resources/")

    retval = []
    for subject, topics in weights_by_subject.items():
        graph = rdflib.graph.Graph()
        subject_uri = rdflib.term.URIRef(subject)
        for topic, weight in topics.items():
            topicscore_uri = res_ns[helpers.generate_uuid()]
            mallet_topic_uri = rdflib.term.URIRef(mu_uri + "resources/" +
                "malletTopic/" + str(topic))
            graph.add((subject_uri, # type MalletTopic
                       voc_ns["hasTopicScore"],
                       topicscore_uri))
            graph.add((topicscore_uri,
                       voc_ns["hasScore"],
                       rdflib.term.Literal(weight)))
            graph.add((topicscore_uri,
                       voc_ns["hasTopic"],
                       mallet_topic_uri))
        retval.append("""
        INSERT DATA {{
            GRAPH <{0}> {{
                {1}
            }}
        }}
        """.format(os.getenv('MU_APPLICATION_GRAPH'), graph.serialize(format='nt').decode('utf-8')))
    return retval

def write_mallet_input(contents, dir):
    """
    Place files for mallet input in input folder
    contents: dictionary with "subject: text"-pairs
    dir: folder for mallet input files
    returns a "uuid: subject"-dictionary (as subject urls aren't valid filenames)
    """
    retval = {}
    for subject, text in contents.items():
        fn = helpers.generate_uuid()
        path = os.path.join(dir, fn)
        with open(path, 'w') as f:
            res = f.write(text)
            if res > 0:
                retval[fn] = subject
            else:
                helpers.log("Couldn't write {} to MALLET input file".format(fn))
    return retval

def run():
    # Query sparql
    select_query = build_select_query()
    try:
        results = helpers.query(select_query)["results"]["bindings"]
    except Exception as e:
        helpers.log("Querying SPARQL-endpoint failed:\n" + str(e))
        return
    contents = {result["subject"]["value"]: result["text"]["value"] \
        for result in results} # Key names dependent of ?...-names in query!
    # prepare MALLET run (text from store -> files)
    mallet_input_dir = os.getenv('INPUT_PATH')
    os.makedirs(mallet_input_dir, exist_ok=True)
    fn_map = write_mallet_input(contents, mallet_input_dir)
    # Run MALLET
    try:
        mallet_command = "/start.sh"
        subprocess.run(mallet_command)
    except subprocess.CalledProcessError as e:
        helpers.log("Failed to run MALLET ...\n" + str(e))
    # Read in MALLET results from files
    mallet_output = mallet_tools.process_file(os.path.join(os.getenv('OUTPUT_PATH'),
                                                           'output.txt'))
    # Make a map of weights by subject (map back from uuid to subject-url)
    weights_by_subject = {fn_map[os.path.basename(path)]: topics \
        for nr, path, topics in mallet_output}
    insert_querys = build_insert_query(weights_by_subject)
    for q in insert_querys:
        try:
            helpers.log(q)
            helpers.update(q)
        except Exception as e:
            helpers.log("Querying SPARQL-endpoint failed:\n" + str(e))
