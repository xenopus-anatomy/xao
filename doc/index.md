##Development

The Xenopus Anatomy Ontology is provided in both Open Biomedical Ontologies (OBO) and Web Ontology Language (OWL) file formats and may be edited in either [OBO-Edit](http://oboedit.org/) or [Protégé](http://protege.stanford.edu/), respectively. Whichever your editing tool preference, be sure the OBO and OWL versions are synced before committing a change to the repository. You can accomplish this with the [oboformat-tools](https://github.com/oboformat/oboformat-tools) file converter.

Changes are made in a git branch. Make a local branch by executing the following command:

    git checkout -b <branch>

The branch name is lower case underscore, e.g. `brain_structures`. A long-lived or jointly developed branch is pushed to the server:

    git push origin <branch>

Rebase the branch from time to time as follows:

    git rebase master

This integrates the branch with the master, detects conflicts, and facilitates subsequent merge.

Execute the merge with the following commands:

    git checkout master
    git merge --no-ff <branch>

Note the `--no-ff` option, which ensures that an audit trail of the merge is kept in a commit log, even if there are no merge conflicts.

##Making a release

When it is time to make a new XAO release, merge any changes that should be included in the release with the master branch.

Run the script to ensure the ontology is `is_a` complete and all terms have definitions and valid stage ranges. In the top level directory, execute the following:

    python scripts/obo_ontology_checks.py

Fix any outstanding issues.

Make sure the ontology header contains the following:

    data-version: <release>
    date: <date>
    remark: <version>

where `data-version` is the release date in YYYY-MM-DD format, `date` is the time stamp of the most recent saved OBO file, and the `remark` contains the new version number assigned by Xenbase, e.g.:

    data-version: 2015-05-27
    date: 27:05:2015 22:52
    remark: Version: 4.0

Manually edit these lines as necessary and sync the OWL version with it. 

Commit the changes.

Set a git tag with a v prefix, e.g.:

    git tag v4.0

Update the server:

    git push
    git push --tags

Put copies of the relevant release files on Xenbase FTP.

A variety of external sites should then automatically pick up the release. A couple of days after the release, check the sites listed on the [README](https://github.com/xenopus-anatomy/xao/blob/master/README.md) page. The XAO entry at [NCBO BioPortal](http://bioportal.bioontology.org/ontologies/XAO) must be manually updated by Xenbase staff. If any ontology metadata on [OBO Foundry](http://www.obofoundry.org/ontology/xao.html) needs to be updated, submit an [issue request](https://github.com/OBOFoundry/OBOFoundry.github.io/issues).
