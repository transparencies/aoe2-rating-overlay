# Requirements

## System: Meta-Templating engine (MTE)

### Functional
- the subsystem should translate templates and a descriptive config file to language-specific templates
  - use: stable API to content creators, we are "language independent"/future-proof
- it should further create a language-specific service files
  - use: easily create requests for the exposed variables on the tempaltes
  - use: future proof for API adaption

#### Use-cases
##### UC1: Create a language-specific template, Input **svg + cfg**
- **Short description:** Content creator starts MTE with a single `svg-template` and `config file` to create files that are usable in our backend

- **Actors:** Content creator

- **Conditions:**
  - corresponding svg template is existing and valid
  - config file is existing and valid
  - svg template has IDs set in the right way
  - config file describes the functionality for the template

- **Operation description:**
  Content creators start the MTE with a template and a config file. MTE validates and parses input files, non-valid files throw errors. Missing values in the config file or properties not having the corresponding counterpart in either svg or config displays warnings, needed but missing values issue errors. Warnings and errors are written to a logfile next to the config file. Without errors the MTE starts configuring the files and outputs them to a place the content creator has set with a parameter on the CLI or the output file uses the same path where the input file came from. By default we don't replace the input file, so there is a default suffix that makes clear, that this file is already configured. During the process we show a progress bar to the user and give visual feedback on what is currently being worked on, we also write everything in a logfile depending on what verbosity/loglevel the content creator has chosen.

- **Consequences:** The configured file get written to a defined/default path or warnings/errors are shown and the process is terminated.

##### UC2: Create a language-specific template, Input **collection archive** 
- **Short description:** Content creator starts MTE with a an archive containing file to create templates that are usable in our backend

- **Actors:** Content creator

- **Conditions:**
  - zipfile is existing and folder layout is in standard form, zipfile is valid
  - corresponding svg templates are existing and valid
  - config file is existing and valid
  - svg templates have IDs set in the right way
  - config file describes the functionality for the templates

- **Operation description:**
  Content creators start the MTE with an archive file containing a standardized folder layout. MTE validates and parses input files, non-valid files throw errors. Missing values in the config file or properties not having the corresponding counterpart in either svg files or config file displays warnings, needed but missing values issue errors. Warnings and errors are written to a logfile next to the config file. Without errors the MTE starts configuring the files and outputs them to a place the content creator has set with a parameter on the CLI or the output file uses a new folder layout inside the same input archive. Files inside the archive can not get replaced with configured files. The new folder layout is depending on settings inside the config file (e.g. version, chosen programming language for the output files, etc.). During the process we show a progress bar to the user and give visual feedback on what is currently being worked on, we also write everything in a logfile depending on what verbosity/loglevel the content creator has chosen. The logfile should reside inside the archive as well. The archive functions as a transportable package containing everything in need to reconfigure the files with other settings or edit the templates in a graphics program.

- **Consequences:** The configured file get written into a subfolder structure inside the archive or warnings/errors are shown and the process is terminated.

### Qualitative
- the meta-templating process itself should be optimized for different forms of processing (e.g. live-preview, collection archive)
- it should not take more than **30 seconds up to 1 Minute** to process a collection archive completely
  - processing should be made transparent for the user (status messages, progress bars)

### Constraints

## System: API-Handler

### Functional

#### Use-cases

##### UC3: Create a language-specific service files from openapi and GraphQL APIs
- **Short description:**
- **Actor:** Content creator
- **Conditions:** 
- **Operation description:**
- **Consequences:**

### Qualitative

### Constraints


## System: Backend
### Functional
#### Use-cases

##### UC
- **Short description:**
- **Actors:**
- **Conditions:** 
- **Operation description:**
- **Consequences:**

### Qualitative
- the average response time of the backend should not exceed 125-150 ms

### Constraints


## System: Frontend
### Functional
- the frontend should be able to go to an less invasive error state/recover from an error if it lost connection to the backend, admin interface etc.
- dynamically resize with the dragging in OBS (e.g.)

#### Use-cases
##### UC
- **Short description:**
- **Actors:**
- **Conditions:**
- **Operation description:**
- **Consequences:**

### Qualitative
- the frontend should be able to display effects, animations and marquee fluently

### Constraints
