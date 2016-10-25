#!/usr/bin/python

"""
Read new terms created in an Excel template and output them to OBO format.
"""


import datetime
import getpass
import os
import parseont
import sys


"""
Complete and save a tab-delimited file named NewTerms.txt in the templates
directory. It should contain the following columns. Use term labels, not IDs.
Multiple values should be comma-separated.

TO DO - Move this to the README.

* Term label
* Definition
* Definition dbxref (XX:<new dbxref>)
* Synonym(s) - automatically set to RELATED
* Parent term
* part_of term(s)
* develops_from term(s)
* develops_into term(s)
* Start stage
* End stage
"""


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

ont = parseont.dict()
term_ids = {ont[k]["name"]:k for k in ont.keys() if ont[k]["namespace"] == DEFAULT_NAMESPACE}
stage_ids = {ont[k]["name"]:k for k in ont.keys() if ont[k]["namespace"] == STAGE_NAMESPACE}

base_tid = "0000000"

with open(os.path.abspath(__file__ + "/../../templates/" + filename)) as f:
    content = f.read().splitlines()

# Skip the header row.
for line in content[1:]:
    bits = line.split("\t")
    print
    print("[Term]")
    print("id: " + PREFIX + ":" + base_tid[:7-len(str(tid))] + str(tid))
    print("name: " + bits[0])
    print("def: \"" + bits[1].replace("\"", "") + "\" [" + bits[2] + "]")
    syns = bits[3].replace("\"", "").split(", ")
    for syn in syns:
        print("synonym: \"" + syn + "\" RELATED []")
    print("is_a: " + term_ids[bits[4]] + " ! " + bits[4])
    dev_froms = bits[6].replace("\"", "").split(", ")
    for dev_from in dev_froms:
        print("relationship: develops_from " + term_ids[dev_from] + " ! " + dev_from)
    dev_intos = bits[7].replace("\"", "").split(", ")
    for dev_into in dev_intos:
        print("relationship: develops_into " + term_ids[dev_into] + " ! " + dev_into)
    print("relationship: end_stage " + stage_ids[bits[8]] + " ! " + bits[8])
    part_ofs = bits[5].replace("\"", "").split(", ")
    for part_of in part_ofs:
        print("relationship: part_of " + term_ids[part_of] + " ! " + part_of)
    print("relationship: start_stage " + stage_ids[bits[9]] + " ! " + bits[9])
    print("created_by: " + getpass.getuser())
    print("creation_date: " + datetime.datetime.now().isoformat()[:-7] + "Z")
    tid += 1
