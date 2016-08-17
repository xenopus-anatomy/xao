#!/usr/bin/python

"""
Check Xenopus Anatomy Ontology OBO-formatted file for missing is_a parents,
  definitions, and stages, and for stage range consistency.

Author: Erik Segerdell
"""


import os
import parseont


"""
Specify the names of the ontology and staging series files. The staging series
file contains a plain text list of developmental stages, in the order of their
timing, one stage per line and named exactly as they are in the ontology.
Provide the OBO ontology prefix and default namespace.
"""
ont_file = "xenopus_anatomy.obo"
stage_file = "NF_stages.txt"
prefix = "XAO"
default_namespace = "xenopus_anatomy"

ont_file = os.path.abspath(__file__ + "/../../" + ont_file)
stage_file = os.path.abspath(__file__ + "/../" + stage_file)


"""
Specify terms that will be excluded from some of the checks:
* Ontology root term and "unspecified"
* Terms with unusual stage ranges
* In vitro anatomy terms
* Developmental stages
* Anatomical site terms
"""
exclude_id = ["XAO:0000000",
              "XAO:0000220",
              "XAO:0000256",
              "XAO:0003003",
              "XAO:0003048",
              "XAO:0003185",
              "XAO:0004492"]
exclude_namespace = ["xenopus_anatomy_in_vitro", "xenopus_developmental_stage"]
exclude_subset = "anatomical_site_slim"


def check_for_missing(attrib, attrib_name):

    """
    Check terms in the dictionary for missing is_a parents, definition, or
    start or end stage. Print exceptions and provide a count.
    """

    print("Checking for terms lacking " + attrib_name + "...\n")

    ct = 0
    for key in ontology.keys():
        if (key not in exclude_id and
              ontology[key]["namespace"] not in exclude_namespace and
              exclude_subset not in ontology[key]["subset"] and
              attrib not in ontology[key].keys()):
            print(key + "\t" + ontology[key]["name"])
            ct += 1
        else:
            pass

    print("\n" + str(ct) + " terms(s)")
    print(div)

    return(ct)


def stage_range(stage_file):

    """
    Check terms in the dictionary for start/end stage consistency. Read the
    staging series file and create a list of stages. An anatomical entity must
    exist within the stage range of its is_parent, sometime during the stage
    range of its part_of parent, and it must have a start stage that occurs
    within or abuts the stage range of its develops_from parent. Print
    exceptions and provide a count.
    """

    print("Checking stage range consistency...\n")

    fh = open(stage_file)
    stages = [line.replace("\n", "") for line in fh]
    fh.close()

    ct = 0
    for key in ontology.keys():
        if (key not in exclude_id and
              ontology[key]["namespace"] not in exclude_namespace
              and exclude_subset not in ontology[key]["subset"]):
            par_id = ontology[key]["is_a"]
            if par_id not in exclude_id:
                term_st_1 = ontology[ontology[key]["start_stage"]]["name"]
                term_st_2 = ontology[ontology[key]["end_stage"]]["name"]
                par_st_1 = ontology[ontology[par_id]["start_stage"]]["name"]
                par_st_2 = ontology[ontology[par_id]["end_stage"]]["name"]
                if (stages.index(term_st_1) < stages.index(par_st_1) or
                      stages.index(term_st_2) > stages.index(par_st_2)):
                    print(ontology[key]["name"] + ": " + term_st_1 +
                            " to " + term_st_2 + "\nis_a " +
                            ontology[par_id]["name"] + ": " +
                            par_st_1 + " to " + par_st_2 + "\n")
                    ct += 1
                else:
                    pass
            else:
                pass
        else:
            pass

    for key in ontology.keys():
        if (ontology[key]["namespace"] not in exclude_namespace and
                "part_of" in ontology[key].keys()):
            for par_id in ontology[key]["part_of"]:
                term_st_1 = ontology[ontology[key]["start_stage"]]["name"]
                term_st_2 = ontology[ontology[key]["end_stage"]]["name"]
                par_st_1 = ontology[ontology[par_id]["start_stage"]]["name"]
                par_st_2 = ontology[ontology[par_id]["end_stage"]]["name"]
                if (stages.index(term_st_2) < stages.index(par_st_1) or
                      stages.index(term_st_1) > stages.index(par_st_2)):
                    print(ontology[key]["name"] + ": " + term_st_1 +
                            " to " + term_st_2 + "\npart_of " +
                            ontology[par_id]["name"] + ": " +
                            par_st_1 + " to " + par_st_2 + "\n")
                    ct += 1
                else:
                    pass
        else:
            pass

    for key in ontology.keys():
        if (key not in exclude_id and "develops_from" in ontology[key].keys()):
            for par_id in ontology[key]["develops_from"]:
                term_st_1 = ontology[ontology[key]["start_stage"]]["name"]
                term_st_2 = ontology[ontology[key]["end_stage"]]["name"]
                par_st_1 = ontology[ontology[par_id]["start_stage"]]["name"]
                par_st_2 = ontology[ontology[par_id]["end_stage"]]["name"]
                if (stages.index(term_st_1) < stages.index(par_st_1) or
                      stages.index(term_st_1) > (stages.index(par_st_2) + 1)):
                    print(ontology[key]["name"] + ": starts at " +
                            term_st_1 + "\ndevelops_from " +
                            ontology[par_id]["name"] + ": " +
                            par_st_1 + " to " + par_st_2 + "\n")
                    ct += 1
                else:
                    pass
        else:
            pass

    print("\n" + str(ct) + " error(s)")
    print(div)

    return()


"""
Load the ontology file and call functions to run the various checks. Checks for
missing is_a parents, definitions, start and end stages are done first. Stage
range consistency can be checked only if all anatomical entities have is_a
parents and both start and end stages.
"""

# TODO - Pass in the parameters.
ontology = parseont.dict()

# TODO - Improve the output formatting.
div = "=================================================="
print("\nLoaded file " + ont_file + "\n")
print(div)

ct_i = check_for_missing("is_a", "an is_a parent")
check_for_missing("def", "a definition")
ct_s = check_for_missing("start_stage", "a start stage")
ct_e = check_for_missing("end_stage", "an end stage")

if ct_i + ct_s + ct_e == 0:
    stage_range(stage_file)
else:
    print("Ontology must be is_a and stage complete before stage range " +
            "integrity can be checked.\n")
    print(div)
