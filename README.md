# USD Asset Viewer
- A python/C++ tool for navigating USD (Universal Scene Description) scene hierarchies.


## Status
- WORK IN PROGRESS


## Current Screenshot
![USD Asset Viewer WIP Screenshot](docs/current_wip.png)


## Features
#### Core
- Hydra viewport
    - Default camera
    - Default lighting
    - Up axis selection
    - View modes:
        - Wireframe
        - Shaded with wireframe
        - Full shading
    - Camera selection
    - Disable scene or default lighting
    - OGL visualization for non-geometry objects:
        - Camera
        - XForm
        - Lights
        - Bone
- Outliner panel
    - Standard view
    - Skeleton view
    - Material view
- Details panel
    - Input / Output
- Trackbar panel
    - Animation playback
    - Scrubbing
#### Future
- Animation blending
    - Node based
    - Nodes
        - Add
        - Subtract
        - Mask
- Nodes
    - Visualize the scene as nodes



## Dependencies
#### Python
- OpenUSD
- imgui_bundle
- toml
#### C++
- OpenUSD
- glad


## Usage
- File > Open USD > *.usd


## License
- MIT License
