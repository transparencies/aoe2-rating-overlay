# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
Documentation:
- Added instructions to setup the overlay

Overlay:
- change circle size
- fix 2nd player rank
- display unranked and deranked players
- layout fixes


## [1.0.0] - 2020-06-03
### Added
Overlay:
- Display equal shades of red
- Choose red and green colour value to circumvent video compression (chroma subsampling) on lower resolutions
- Cutoff rank and don't show ranks lower than 999
- Scale names properly on first render, i.e. during show animation

Backend:
- Remote control
- Websocket heartbeat
- Hide/show and reload overlay

[Unreleased]: https://github.com/aoe-assoc/aoe2-rating-overlay/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/aoe-assoc/aoe2-rating-overlay/releases/tag/v1.0.0
