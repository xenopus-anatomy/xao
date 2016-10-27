#!/usr/bin/python

"""
Check the Xenopus Anatomy Ontology OBO file for missing is_a parents,
definitions, and start/end stages and check stage range consistency.
"""

import os
import parseont

"""
Specify terms that should be excluded from some of the checks: the ontology
root term, "unspecified", terms with unusual stage ranges, in vitro anatomy,
developmental stages, and anatomical sites.
"""

fh = open(os.path.abspath(__file__ + "/../exclude.txt"))
EXCLUDE_ID = [line.split("\t")[0] for line in fh]
fh.close()

EXCLUDE_NAMESPACE = ["xenopus_anatomy_in_vitro", "xenopus_developmental_stage"]
EXCLUDE_SUBSET = "anatomical_site_slim"

"""
Specify the name of the staging series file. This should contain a plain text
list of developmental stages in the order of their timing, one stage per line,
and named exactly as they are in the ontology.
"""
STAGE_FN = "NF_stages.txt"

def check_for_missing(attrib, attrib_text):

    """
    Checks terms in the dictionary for missing is_a parents, definitions, or
    start or end stages.
    """

    print("\033[31m" + "Checking for terms lacking " + attrib_text + "..." +
            "\033[0m")

    ct = 0
    for key in ontology.keys():
        if (key not in EXCLUDE_ID and
              ontology[key]["namespace"] not in EXCLUDE_NAMESPACE and
              EXCLUDE_SUBSET not in ontology[key]["subset"] and
              attrib not in ontology[key].keys()):
            print(key + "\t" + ontology[key]["name"])
            ct += 1
        else:
            pass

    # Print exceptions and provide a count.
    print(str(ct) + " terms(s)" + "\n")
    return(ct)

def stage_range():

    """
    Checks terms in the dictionary for start and end stage consistency. Each
    anatomical entity must exist entirely within the stage range of its is_a
    parent, sometime during the stage range of its part_of parent, it must have
    a start stage that occurs within or abuts the stage range of its
    develops_from parent, and it must have an end stage that at least abuts the
    stage range of its develops_into parent.
    """

    print("\033[31m" + "Checking stage range consistency..." + "\033[0m")

    # Create the developmental stage list.
    fh = open(os.path.abspath(__file__ + "/../" + STAGE_FN))
    stages = [line.replace("\n", "") for line in fh]
    fh.close()

    ct = 0
    for key in ontology.keys():
        if (key not in EXCLUDE_ID and
              ontology[key]["namespace"] not in EXCLUDE_NAMESPACE
              and EXCLUDE_SUBSET not in ontology[key]["subset"]):
            par_id = ontology[key]["is_a"]
            if par_id not in EXCLUDE_ID:
                term_st_1 = ontology[ontology[key]["start_stage"]]["name"]
                term_st_2 = ontology[ontology[key]["end_stage"]]["name"]
                par_st_1 = ontology[ontology[par_id]["start_stage"]]["name"]
                par_st_2 = ontology[ontology[par_id]["end_stage"]]["name"]
                if (stages.index(term_st_1) < stages.index(par_st_1) or
                      stages.index(term_st_2) > stages.index(par_st_2)):
                    print(ontology[key]["name"] +
                            " [" + term_st_1 + " to " + term_st_2 + "]" +
                            " is_a " +
                            ontology[par_id]["name"] +
                            " [" + par_st_1 + " to " + par_st_2 + "]")
                    ct += 1
                else:
                    pass
            else:
                pass
        else:
            pass

    for key in ontology.keys():
        if (ontology[key]["namespace"] not in EXCLUDE_NAMESPACE and
                "part_of" in ontology[key].keys()):
            for par_id in ontology[key]["part_of"]:
                term_st_1 = ontology[ontology[key]["start_stage"]]["name"]
                term_st_2 = ontology[ontology[key]["end_stage"]]["name"]
                par_st_1 = ontology[ontology[par_id]["start_stage"]]["name"]
                par_st_2 = ontology[ontology[par_id]["end_stage"]]["name"]
                if (stages.index(term_st_2) < stages.index(par_st_1) or
                      stages.index(term_st_1) > stages.index(par_st_2)):
                    print(ontology[key]["name"] +
                            " [" + term_st_1 + " to " + term_st_2 + "]" +
                            " part_of " +
                            ontology[par_id]["name"] +
                            " [" + par_st_1 + " to " + par_st_2 + "]")
                    ct += 1
                else:
                    pass
        else:
            pass

    for key in ontology.keys():
        if (key not in EXCLUDE_ID and "develops_from" in ontology[key].keys()):
            for par_id in ontology[key]["develops_from"]:
                term_st_1 = ontology[ontology[key]["start_stage"]]["name"]
                term_st_2 = ontology[ontology[key]["end_stage"]]["name"]
                par_st_1 = ontology[ontology[par_id]["start_stage"]]["name"]
                par_st_2 = ontology[ontology[par_id]["end_stage"]]["name"]
                if (stages.index(term_st_1) < stages.index(par_st_1) or
                      stages.index(term_st_1) > (stages.index(par_st_2) + 1)):
                    print(ontology[key]["name"] +
                            " [" + term_st_1 + " to " + term_st_2 + "]" +
                            " develops_from " +
                            ontology[par_id]["name"] +
                            " [" + par_st_1 + " to " + par_st_2 + "]")
                    ct += 1
                else:
                    pass
        else:
            pass

    for key in ontology.keys():
        if (key not in EXCLUDE_ID and "develops_into" in ontology[key].keys()):
            for par_id in ontology[key]["develops_into"]:
                term_st_1 = ontology[ontology[key]["start_stage"]]["name"]
                term_st_2 = ontology[ontology[key]["end_stage"]]["name"]
                par_st_1 = ontology[ontology[par_id]["start_stage"]]["name"]
                par_st_2 = ontology[ontology[par_id]["end_stage"]]["name"]
                if (stages.index(term_st_1) > stages.index(par_st_1) or
                      stages.index(term_st_2) < (stages.index(par_st_1) - 1)):
                    print(ontology[key]["name"] +
                            " [" + term_st_1 + " to " + term_st_2 + "]" +
                            " develops_into " +
                            ontology[par_id]["name"] +
                            " [" + par_st_1 + " to " + par_st_2 + "]")
                    ct += 1
                else:
                    pass
        else:
            pass

    # Print exceptions and provide a count.
    print(str(ct) + " error(s)" + "\n")
    return()

"""
Generate the ontology term dictionary and run the various checks. Check for
missing is_a parents, definitions, start and end stages are completed first.
Stage range consistency can be checked only if all anatomical entities have
is_a parents and complete start and end stages.
"""

ontology = parseont.dict()

ct_i = check_for_missing("is_a", "an is_a parent")
check_for_missing("def", "a definition")
ct_s = check_for_missing("start_stage", "a start stage")
ct_e = check_for_missing("end_stage", "an end stage")

if ct_i + ct_s + ct_e == 0:
    stage_range()
else:
    print("\033[31m" + "Ontology must be is_a and stage complete before" +
            " stage range integrity can be checked." + "\033[0m")
