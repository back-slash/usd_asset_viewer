# USD Asset Viewer
- A python/C++ tool for navigating USD (Universal Scene Description) scene hierarchies.

## Status
- 1 Month Project
- Day 31/31
- Month 1 Complete

## Current Screenshot
![USD Asset Viewer WIP Screenshot](docs/current_wip.png)

## Features

### Core (1 Month Project)
- Hydra viewport
    - Default camera
    - Default lighting
    - View modes:
        - Wireframe
        - Shaded with wireframe
        - Full shading
    - OGL visualization for non-geometry objects:
        - Grid
        - Orientation gizmo
        - Camera
        - XForm
        - Lights
        - Bone (solid and xray)
- Outliner panel:
    - Standard view
- Details panel:
    - Attributes
- Trackbar panel:
    - Animation Modes:
        - In place
        - Root motion

### Future
- Animation node editor:
    - Add
    - Subtract
    - Mask
- Material editor:
    - Add
    - Subtract
    - Multiply
    - Mask
- Convert to modern OGL

## Installation
#### Compatibility:
- Windows (Tested)
- Linux (Tested)
- Mac (WIP)
#### Requirments:
- git
- Python >=3.10
- venv
- C ++ Compiler
    - Windows: VS 2019+ (OpenUSD)


#### Steps:
0) Ensure requirements are met before install.
1) Open terminal or powershell.
2) `git clone https://github.com/back-slash/usd_asset_viewer.git`
3) `cd usd_asset_viewer`
4) If you already have OpenUSD, add the root path to step 6: `--usd-path path/to/usd` or enter in `build_run.py`.
5) Windows: `python build_run.py` Linux: `python3 build_run.py`
6) Allow build script to install all dependencies.
7) Once building is complete USD Asset Viewer will open.
8) Future runs can be done using step 5.


## Usage
- File > Open USD > *.usd


## License
- MIT License
