#!/usr/bin/python

"""
Read in new terms from a template and output them to OBO format.
"""

import datetime
import getpass
import os
import parseont
import sys

if len(sys.argv) < 3:
    sys.exit("\033[31m" + "Please provide a filename and ID start number." +
               "\033[0m")
else:
    pass

filename = sys.argv[1]
tid = int(sys.argv[2])

PREFIX = "XAO"
DEFAULT_NAMESPACE = "xenopus_anatomy"
STAGE_NAMESPACE = "xenopus_developmental_stage"

# Generate the ontology term dictionary.
ont = parseont.dict()

term_ids = {ont[k]["name"]:k for k in ont.keys() if ont[k]["namespace"] == DEFAULT_NAMESPACE}
stage_ids = {ont[k]["name"]:k for k in ont.keys() if ont[k]["namespace"] == STAGE_NAMESPACE}

base_tid = "0000000"

# A tab-delimited file with the new terms must exist in the templates folder.
with open(os.path.abspath(__file__ + "/../../templates/" + filename)) as f:
    content = f.read().splitlines()

print("\033[31m" + "Begin OBO output..." + "\033[0m")

# Skip the header row.
for line in content[1:]:
    bits = line.split("\t")
    print
    print("[Term]")
    new_id = PREFIX + ":" + base_tid[:7-len(str(tid))] + str(tid)
    # Add new term and ID to the dictionary.
    term_ids[bits[0]] = new_id
    print("id: " + new_id)
    print("name: " + bits[0])
    print("def: \"" + bits[1].replace("\"", "") + "\" [" + bits[2] + "]")
    if bits[3] != "":
        syns = bits[3].replace("\"", "").split(", ")
        for s in syns:
            print("synonym: \"" + s + "\" RELATED []")
    else:
        pass
    print("is_a: " + term_ids[bits[4]] + " ! " + bits[4])
    if bits[6] != "":
        dev_from = bits[6].replace("\"", "").split(", ")
        for s in dev_from:
            print("relationship: develops_from " + term_ids[s] + " ! " + s)
    else:
        pass
    if bits[7] != "":
        dev_into = bits[7].replace("\"", "").split(", ")
        for s in dev_into:
            print("relationship: develops_into " + term_ids[s] + " ! " + s)
    else:
        pass
    print("relationship: end_stage " + stage_ids[bits[8]] + " ! " + bits[8])
    if bits[5] != "":
        part_of = bits[5].replace("\"", "").split(", ")
        for s in part_of:
            print("relationship: part_of " + term_ids[s] + " ! " + s)
    else:
        pass
    print("relationship: start_stage " + stage_ids[bits[9]] + " ! " + bits[9])
    print("created_by: " + getpass.getuser())
    print("creation_date: " + datetime.datetime.now().isoformat()[:-7] + "Z")
    tid += 1

print("\033[31m" + "...end OBO output." + "\033[0m")
