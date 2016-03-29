#TerminalMavenSearch
Simple python project to search for artifacts in the 
central maven repository from the terminal. Makes use
of the Rest API provided here http://search.maven.org/#api

#Motivation
To get started with python and make it easier
to obtain information about artifacts from the terminal.

#Requirements
Requires Python 2.7 to run. Untested on Windows.

#Usage
1. Download and extract zip file of this repository or clone using git.
2. Navigate to folder containing code.
3. Execute the following command:
```bash
python mvn_search.py [options]
```

#Documentation
Lists the optional arguments and their purpose.

-h, --help : Shows help message containing list of options that can
be provided

-s, --search : Basic search. Returns artifacts with search term 
appearing either in ArtifactId or GroupId

-g, --group : Returns all artifacts in specified group

-a, --artifact : Search all artifacts with specified artifact id

-c, --class_name : Search by class name. Returns list of artifacts, down
to the specific version containing the class

-fc, --fclass_name : Search by fully quantified class name.
Returns list of artifacts, down to the specific version containing the class

-cs, --checksum : Search artifact by SHA-1 checksum

-t, --tag : Search for all artifacts having specified tag

-st, --start : Get search results from index start
  
-r, --rows : Number of search results to be displayed

#Example
```bash
python mvn_search.py --artifact guice --start 10 --rows 4
```
returns the following output:
```bash
Searching for all artifacts with id guice ....
11 search results found

Id: com.google.inject:guice
GroupId: com.google.inject
ArtifactId: guice
Latest Version: 4.0
Version Count: 10
Last Updated: 2015-04-29
Packaging: jar
Available also: ['-sources.jar', '-javadoc.jar', '-test-sources.jar', '-tests.jar', '.jar', '-site.jar', '-no_aop.jar', '-classes.jar', '.pom']

Id: org.lunarray.model.extensions.descriptor:guice
GroupId: org.lunarray.model.extensions.descriptor
ArtifactId: guice
Latest Version: 1.0
Version Count: 1
Last Updated: 2014-07-27
Packaging: jar
Available also: ['-javadoc.jar', '-sources.jar', '.jar', '.pom']

Showing results 5 to 6 out of 11 results
```

#TODO
Publish on PyPI
