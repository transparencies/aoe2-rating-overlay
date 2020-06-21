# Requirements

## Meta-Templating engine

### Functional
- the subsystem should translate templates and a descriptive config file to language-specific templates
  - use: stable API to content creators, we are "language independent"/future-proof
- it should further create a language-specific service files
  - use: easily create requests for the exposed variables on the tempaltes
  - use: future proof for API adaption

### Qualitative
- the meta-templating process itself should be optimized for different forms of processing (e.g. live-preview, collection archive)
- it should not take more than **30 seconds up to 1 Minute** to process a collection archive completely
  - processing should be made transparent for the user (status messages, progress bars)

### Constraints


## Backend
### Functional

### Qualitative
- the average response time of the backend should not exceed 125-150 ms

### Constraints


## Frontend
### Functional
- the frontend should be able to go to an less invasive error state if it lost connection to the backend, admin interface etc.
  - actually it should be able to be controlled in it's basic funkctionality (switching states etc.) without connection to the backend
- the frontend should be able to display effects, animations and marquee fluently
- frontend overlay should be able to dynamically resize with the dragging in OBS (e.g.) (even possible?)

### Qualitative


### Constraints
