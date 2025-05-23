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
    - View modes:
        - Wireframe
        - Shaded with wireframe
        - Full shading
    - OGL visualization for non-geometry objects:
        - Camera
        - XForm
        - Lights
        - Bone (Solid and XRay)
- Outliner panel:
    - Standard view
    - Skeleton view
    - Material view
- Details panel:
    - Input / Output
- Trackbar panel:
    - Animation Modes:
        - In Place
        - Root Motion
#### Future
- Animation blending
    - Node Editor:
        - Add
        - Subtract
        - Mask
- Nodes
    - Visualize the scene as nodes


## Installation
#### COMPATIBILITY
- Windows (Tested)
- Linux (Tested)
- Mac (WIP)

#### USD
- Clone OpenUSD https://github.com/PixarAnimationStudios/OpenUSD
- Install using provided build script. Include `--usd-imaging` and `--ptex` and fllow instructions
- Set OpenUSD path in `CMakeLists.txt`
#### GLAD
Go to https://glad.dav1d.de/ to download GLAD (4.5). Set path in `CMakeLists.txt`
#### PYBIND
Go to https://github.com/pybind/pybind11 and clone. Set path in `CMakeLists.txt`
#### PYTHON
Tested on Python 3.12
Dependencies:
- imgui_bundle
- toml


## Usage
- Once all dependencies and installed, and paths set in `CMakeLists.txt`, run `build_run.py`
- File > Open USD > *.usd


## License
- MIT License
