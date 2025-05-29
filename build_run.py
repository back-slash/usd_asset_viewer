#####################################################################################################################################
# USD Asset Viewer | Build and Run Script
# TODO:
#
#####################################################################################################################################
# PYTHON
import os
import subprocess
import sys
#####################################################################################################################################

os_type = os.name
build_directory = "build"
cmake_cache = os.path.join(build_directory, "CMakeCache.txt")
venv_directory = os.path.join(os.path.dirname(__file__), ".venv")
requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")


def init_submodules():
    print("Initializing git submodules...")
    try:
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True, cwd=os.path.dirname(__file__))
        print("Sub-modules initialized successfully...")
        return True
    except subprocess.CalledProcessError:
        print("Warning: git not found")
        return False

def build_usd_module(python_path: str):
    print("Building git submodules...")
    script_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD", "build_scripts", "build_usd.py")
    subprocess.check_call([python_path, f"build_scripts/build_usd.py"])    
    

def create_build():
    if not os.path.isfile(cmake_cache):
        print(f"Generating CMake files in {build_directory}...")
        if not os.path.isdir(build_directory):
            os.makedirs(build_directory)
        subprocess.check_call(["cmake", "-S", ".", "-B", build_directory])
        return True

def run_build_process():
    print(f"Running CMake in {build_directory}...")
    subprocess.check_call(["cmake", "--build", build_directory, "--config", "Release"])

def setup_virtual_environment() -> str:
    if not os.path.isdir(venv_directory):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_directory])
    if os_type == 'nt':
        venv_activate = os.path.join(os.path.dirname(__file__), ".venv/Scripts/activate.bat")
    else:
        venv_activate = os.path.join(os.path.dirname(__file__), ".venv/bin/activate")
    python_path = os.path.join(os.path.dirname(venv_activate), "python")
    return python_path, venv_activate

def activate_virtual_environment(venv_activate):
    print(f"Activating virtual environment...")
    subprocess.call(venv_activate, shell=True)

def install_python_dependencies(python_executable: str):
    print("Check/Install Python requirements...")
    subprocess.check_call([python_executable, "-m", "pip", "install", "-r", requirements_file])

def build_run():
    create_build()
    run_build_process()
    python_path, venv_activate = setup_virtual_environment()
    activate_virtual_environment(venv_activate)
    install_python_dependencies(python_path)
    import tool.base_tool as tbase
    ui = tbase.USDAssetViewer()

build_run()