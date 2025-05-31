# USD Asset Viewer
- A python/C++ tool for navigating USD (Universal Scene Description) scene hierarchies.

## Status
- 1 Month Project
- Day 30/31
- WORK IN PROGRESS

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

## Installation
#### Compatibility:
- Windows (Tested)
- Linux (Tested)
- Mac (WIP)
#### Requirments:
- git
- Python >=3.10
- C ++ Compiler
    - Windows: VS 2019+ (OpenUSD)


#### Steps:
1) Open terminal or powershell.
2) `git clone https://github.com/back-slash/usd_asset_viewer.git`
3) `cd usd_asset_viewer`
4) Linux Only: `chmod 775 build_usd_linux.sh` then `./build_usd_linux.sh`. Wait for OpenUSD to build.
5) If you have OpenUSD or are on Linux, add the root path to step 6: `--usd-path path/to/usd` or enter in `build_run.py`.
6) Windows: `python build_run.py` Linux: `python3 build_run.py`
7) Allow build script to install all dependencies.
8) Once building is complete USD Asset Viewer will open.
9) Future runs can be done using step 6.


## Usage
- File > Open USD > *.usd


## License
- MIT License
