# Requirements

## System: Meta-Templating engine (MTE)

### Functional
- the subsystem should translate templates and a descriptive config file to language-specific templates
  - use: stable API to content creators, we are "language independent"/future-proof
- it should further create a language-specific service files
  - use: easily create requests for the exposed variables on the tempaltes
  - use: future proof for API adaption

#### Use-cases
##### Create a language-specific template, Input svg + cfg
- Short description: Content creator starts MTE with a single `svg-template` and `config file` to create files that are usable in our backend

- Actor: Content creator

- Condition: 
  - svg template is existing and valid
  - config file is existing and valid
  - svg template has IDs set in the right way
  - config file describes the functionality for the template

- Operation description:
  Content creators start the MTE with a template and a config file. MTE validates and parses input files, non-valid files throw errors. Missing values in the config file or properties not having the corresponding counterpart in either svg or config displays warnings, needed but missing values issue errors. Warnings and errors are written to a logfile next to the config file. Afterwards the MTE starts configuring the files and outputs them to a place the content creator has set with a parameter on the CLI or the output file uses the same path where the input file came from. By default we don't replace the input file, so there is a default suffix that makes clear, that this file is already configured. During the process we show a progress bar to the user and give visual feedback on what is currently worked on, we also write everything in a logfile depending on what verbosity/loglevel the content creator chose.

- Consequences: The configured file get written to a defined/default path or warnings/errors are shown. If values are missing in the config file we 

##### Create a language-specific template, Input collection archive 
- Short description:
- Actor: Content creator
- Condition: 
  - zipfile is existing and layout is in standard form, zipfile is valid
  - svg template is existing and valid
  - config file is existing and valid
  - svg template has IDs set in the right way
  - config file describes the functionality for the template
- Operation description:
  - 
- Consequences:

##### Create a language-specific service files from openapi and GraphQL APIs
- Short description:
- Actor: Content creator
- Condition: 
- Operation description:
- Consequences:


### Qualitative
- the meta-templating process itself should be optimized for different forms of processing (e.g. live-preview, collection archive)
- it should not take more than **30 seconds up to 1 Minute** to process a collection archive completely
  - processing should be made transparent for the user (status messages, progress bars)

### Constraints


## System: Backend
### Functional
#### Use-cases

### Qualitative
- the average response time of the backend should not exceed 125-150 ms

### Constraints
### Subsystems


## System: Frontend
### Functional
- the frontend should be able to go to an less invasive error state/recover from an error if it lost connection to the backend, admin interface etc.
- dynamically resize with the dragging in OBS (e.g.)

#### Use-cases

### Qualitative
- the frontend should be able to display effects, animations and marquee fluently

### Constraints

### Subsystems
