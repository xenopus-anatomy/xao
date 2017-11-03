## Utilities

### Checkup

The `checkup.py` script loads the OBO-formatted ontology in the root directory, detects missing is_a parents, definitions, and start/end stages, and flags any inconsistencies in the stage ranges of related terms. Navigate to the `utilities` directory and execute the following:

    $ ./checkup.py

### Create new terms

The `templates` directory contains an Excel spreadsheet for creating new anatomy terms, which can then be processed and output as OBO-formatted text.

The template contains the following columns. Use term labels, not IDs. Multiple values should be comma-delimited.

 - Term label*
 - Definition*
 - Definition dbxref*
 - Synonym(s)
 - Parent term*
 - part_of term(s)
 - develops_from term(s)
 - develops_into term(s)
 - Start stage*
 - End stage*

*required

New terms that are specified as parents of other terms in the spreadsheet must be listed first.

Note that synonyms are given the scope *RELATED* by default; you can change this later in an ontology editor, if necessary.

Save a copy of your completed spreadsheet as a tab-delimited file in the `templates` directory. Navigate to the `utilities` directory and execute the term creation script. The tab-delimited template filename and starting term ID must be supplied as arguments; the latter should be one greater than the most recently created anatomy ID. For example:

    $ ./create_terms.py NewTerms.txt 5084

Copy the output, paste it at the end of the ontology OBO file in a plain-text editor, and save. You can reopen the file in OBO-Edit and save it again to ensure that the new terms were properly constructed.

### Dictionary

The `parseont` module constructs a Python dictionary of all anatomy and stage terms in the ontology OBO file in the root directory. You can load it via the command line after navigating to the `utilities` directory:

    $ python
    >>> import parseont
    >>> ont = parseont.dict()

Access term data by specifying its ID:

    >>> print(ont["XAO:0002000"])
    {'subset': ['frequent_anatomy_items'], 'end_stage': 'XAO:1000076', 'part_of': ['XAO:0004521'], 'xref': 'UBERON:0002120', 'synonym': ['head kidney', 'pronephros', 'vorniere'], 'name': 'pronephric kidney', 'start_stage': 'XAO:1000044', 'namespace': 'xenopus_anatomy', 'is_a': 'XAO:0003267', 'develops_from': ['XAO:0000264'], 'def': 'Organ that serves as a transient kidney, providing osmoregulation during early developmental stages, and then degenerates during metamorphosis.'}

To find the most recently used anatomy ID, execute the following:

    >>> ont = parseont.dict(rm_obsoletes=False)
    >>> ids = [k for k in ont.keys() if ont[k]["namespace"] != "xenopus_developmental_stage"]
    >>> max(ids)
