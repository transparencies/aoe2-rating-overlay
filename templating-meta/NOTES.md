# THOUGHTS & NOTES

## Validation of data
 -  our OverlayArchive and other data should be validated and checked for plausability
 - testing collection zip-archive
 - check assets-folder
   - if it is empty, svg should not have xref:link to any data and should embed pictures with base64
   - if files exist, check if they are linked in svg
 - template folder 
   - run inkscape against template folder content with `--vacuum-defs --export-plain-svg` to create a valid plain svg files
   - export IDs from templates with `--query-all template-filename.svg > export-template-filename-ids.txt`
 - config file
   - validate config against format specifications (yaml, json)
   - check if all exported IDs (not tspan, etc.) are defined in config file
     - parse `csv` (ID file)
     - output warnings for non-referenced IDs that exist in svg but not in config file

DESIGN DECISION: How do we deal with the archive? Do we create another folder in it and store all the information inside there? Like configured templates all the other language specific-files? That would have the advantage, that the package is easily downloadable in this state, we can store error logs inside etc. So if people want to continue working on that collection archive, they could just download the zip-file and start editing data. How should the process look like of an already configured archive when reuploading? Just delete the configured files and reconfigure or create diff and version it inside the archive?

--- Files should be fine here ---

## Mapping of config file values
 - the config file was parsed in the validation stage
 - first thing to do, would be to create a directory structure (e.g. in the OverlayArchive) to store the configured output files in
   - directory layout should be easy to use for versioning files `bin/<version>/<configured-language>/<directories-layout>/<configured-files>`
     - `version` comes from the config file's version information
     - `language` is an internal property to split the configured files for different platforms
 - we can start to map the values to their corresponding classes (TODO: DESIGN) and implement the corresponding methods

## API modules
 - create python classes that parse their corresponding `openapi`-file
 - map them to the content/basic functionality of the API file to a class
 - implement methods that expose the `request` to be made to get the corresponding data
 - create an `API-Handler` as a controller around all the `API classes` 
   - can be used to query for `requests` for the corresponding APIs

## USER-API
 - think of config file as input to a template file
   - only have input for the logic. this is also often more understandable for users.
 - ASTs can become too complex to be manageable as well
 - if we want to make it modular or there are many optional settings/sub-elements
   - we can make one object for each group
   - then consider possible parameters for this object
   - with a root object and a list of subobjects with parameter settings (inspired by openage API for example)
 - use cases expose which config options we need for the features and which features we have forgotten
 - large UMLs with many objects should have lesser details, otherwise it becomes quickly confusing
  - better create separate detailed UML diagrams for the individual subsystems
