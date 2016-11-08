##Development

###Editing tools

The Xenopus Anatomy Ontology is avialable in Open Biomedical Ontologies (OBO) and Web Ontology Language (OWL) file formats and may be edited in either [OBO-Edit](http://oboedit.org/) or [Protégé](http://protege.stanford.edu/), respectively. Although it is acceptable to use either program exclusively, OBO-Edit is often a convenient choice for adding new terms, definitions, and definition cross-references, while Protégé makes it easy to subsequently add relationships (OWL `SubClasses Of`).

If you use Protégé to create new terms (OWL `Classes`), you must configure it to generate proper URIs. Use the [dictionary](https://github.com/xenopus-anatomy/xao/blob/master/doc/utilities.md#dictionary) utility to find the most recently used XAO anatomy ID. Then in Protégé do the following:

 - Open Preferences and select the New Entities tab.
 - Set the Entity URI to end with *Auto-generated ID*.
 - Set the Auto-generated ID to be *Numeric (iterative)*.
	 - Prefix: *XAO_*
	 - Suffix: *(leave blank)*
	 - Digit count: *7*
	 - Start: one number greater than the XAO ID you found above.

After creating each new class, add the following annotations:

 - has_obo_namespace: `xenopus_anatomy`
 - id: `XAO:<number>`

The ID number is based on the newly generated URI. Hover over the new class in the class hierarchy and look at the tooltip. If, for example, the URI ends with *XAO_0005084*, then the annotation value is *XAO:0005084*.

###Scripts

Command-line Python tools for performing some quality control checks and automating term creation are described on the [utilities](https://github.com/xenopus-anatomy/xao/blob/master/doc/utilities.md) page.

###Workflow

Ontology updates should be made in one or more [Git](https://git-scm.com/) branches. The branch name is lowercase underscore, e.g. `brain_structures`. A long-lived or jointly developed branch should be pushed to the server.

Whichever your editing tool preference, you can keep the `xenopus_anatomy` OBO and OWL files in sync within the current branch with the [oboformat-tools](https://github.com/oboformat/oboformat-tools) package. It is a good idea to back up your files before running the converter so you don't inadvertently overwrite your work.

##Making a release

When it is time to make a new XAO release, merge any changes that should be included in the release with the `master` branch. Sync the OBO and OWL versions of the ontology if necessary and commit the changes.

Run the [checkup](https://github.com/xenopus-anatomy/xao/blob/master/doc/utilities.md#checkup) utility to ensure that the ontology has a complete `is_a` structure and all terms have definitions and valid stage ranges. Fix and commit any outstanding issues.

Obtain the OBO Ontology Release Tool (Oort), included in the [OWLTools](https://github.com/owlcollab/owltools) package. It generates release files and ontology subsets, assigns a version IRI, and provides ontology metadata and reasoner reports.

In preparation, open the `xenopus_anatomy.obo` file in a plain text editor and update the `remark` line in the header with the new XAO version number designated by Xenbase, e.g.:

    remark: Version: 4.0

Add or update any other `remarks` as needed.

Delete the header's `data-version` line.

Save the file. (There is no need to convert it to an OWL file at this time.)

Delete the `Oort` directory, if one exists, from the repository.

In the top level directory, execute the release runner with the following commands:

    $ export PATH="$PATH:/path/to/owltools/OWLTools-Oort/bin"
    $ ontology-release-runner --outdir Oort xenopus_anatomy.obo

Check the `xao-reasoner-report` in the freshly generated `Oort` directory. If any problems were encountered, fix them and rerun the release.

Delete the existing `xenopus_anatomy` files from the top level directory. Copy the `xao.obo` and `xao.owl` files that are in the `Oort` directory, paste them into the top level directory, and rename them `xenopus_anatomy.obo` and `xenopus_anatomy.owl`.

Commit all changes.

Set a Git tag with a `v` prefix. The version must be exactly the same as the one you put in the OBO file header, e.g.:

    $ git tag v4.0

Push the updates to the server.

Put copies of the `xenopus_anatomy` OBO and OWL files on [Xenbase FTP](http://www.xenbase.org/other/static/ftpDatafiles.jsp).

A variety of external sites should then pick up the release automatically. A couple of days afterwards, check the sites listed on the [README](https://github.com/xenopus-anatomy/xao/blob/master/README.md#browsesearchmetadata) page. The XAO entry at [NCBO BioPortal](http://bioportal.bioontology.org/ontologies/XAO) must be manually updated by Xenbase staff. If any ontology metadata on [OBO Foundry](http://www.obofoundry.org/ontology/xao.html) needs to be updated, submit an [issue request](https://github.com/OBOFoundry/OBOFoundry.github.io/issues).
