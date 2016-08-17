"""
OBO ontology parsing module.

Author: Erik Segerdell
"""


import os


def dict(filename="xenopus_anatomy.obo", prefix="XAO",
           default_namespace="xenopus_anatomy"):

    """
    Returns a dictionary of terms and their properties. Part_of and
    develops_from relationship values and subsets are stored as lists and
    everything else as strings. Stops when the first [Typedef] is reached and
    removes obsolete terms.
    """

    fh = open(os.path.abspath(__file__ + "/../../" + filename))
    contents = [line.replace("\n", "") for line in fh]
    fh.close()
    ontology = {}

    for line in contents:
        if line == "[Typedef]":
            break
        elif line.startswith("id: " + prefix):
            this_id = line[4:]
            ontology[this_id] = { "namespace": default_namespace,
                                  "subset": [] }
        elif line.startswith("name: "):
            ontology[this_id]["name"] = line[6:]
        elif line.startswith("namespace: "):
            ontology[this_id]["namespace"] = line[11:]
        elif line.startswith("def: "):
            ontology[this_id]["def"] = line[6:line.index("[")-2]
        elif line.startswith("subset: "):
            ontology[this_id]["subset"].append(line[8:])
        elif line.startswith("xref: "):
            ontology[this_id]["xref"] = line[6:]
        elif line.startswith("is_a: "):
            ontology[this_id]["is_a"] = line[6:line.index("!")-1]
        elif line.startswith("relationship: "):
            rel_type = line[14:line.index("!")-len(prefix)-10]
            rel_id = line[line.index("!")-len(prefix)-9:line.index("!")-1]
            if rel_type == "part_of" or rel_type == "develops_from":
                if rel_type in ontology[this_id]:
                    ontology[this_id][rel_type].append(rel_id)
                else:
                    ontology[this_id][rel_type] = [rel_id]
            else:
                ontology[this_id][rel_type] = rel_id
        elif line == "is_obsolete: true":
            ontology.pop(this_id)
        else:
            pass

    return(ontology)
