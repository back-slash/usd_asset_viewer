#!/bin/bash

BUILD_USD_PY="external/OpenUSD/build_scripts/build_usd.py"
BUILD_USD_ARGS="--ptex --usd-imaging external/OpenUSD_"
VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating Python virtual environment in $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi

echo "Activating virtual environment and installing requirements..."
source "$VENV_DIR/bin/activate"
python -m pip install -r requirements.txt
git submodule update --init --recursive
python "$BUILD_USD_PY" $BUILD_USD_ARGS "$@"