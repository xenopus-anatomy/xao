#!/usr/bin/python

import datetime
import os
import parseont

"""
The source file should have the following columns:

* Name
* ID
* Definition
* Synonym
* Parent
* Part of
* Start stage
* End stage

"""

CREATED_BY = "eriksegerdell"
DEFAULT_NAMESPACE = "xenopus_anatomy"
STAGE_NAMESPACE = "xenopus_developmental_stage"

# TODO - Pass in the parameters.
ont = parseont.dict()
term_ids = {ont[k]["name"]:k for k in ont.keys() if ont[k]["namespace"] == DEFAULT_NAMESPACE}
stage_ids = {ont[k]["name"]:k for k in ont.keys() if ont[k]["namespace"] == STAGE_NAMESPACE}

# TODO - Read in csv instead of tab-delimited.
# TODO - Provide the filename as an argument.
with open(os.path.abspath(__file__ + "/../../data.txt")) as f:
    content = f.read().splitlines()

for line in content:
    bits = line.split("\t")
    print
    print("[Term]")
    # TODO - Auto-generate the IDs.
    print("id: " + bits[1])
    print("name: " + bits[0])
    print("def: \"" + bits[2].replace("\"", "") + "\" []")
    # TODO - Add support for definition xref.
    # TODO - Add synonyms.
    print("is_a: " + term_ids[bits[4]] + " ! " + bits[4])
    # TODO - Add support for develops_from and into relationships.
    print("relationship: end_stage " + stage_ids[bits[7]] + " ! " + bits[7])
    # TODO - Add part_of relationships.
    print("relationship: start_stage " + stage_ids[bits[6]] + " ! " + bits[6])
    print("created_by: " + CREATED_BY)
    print("creation_date: " + datetime.datetime.now().isoformat()[:-7] + "Z")
