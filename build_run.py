#####################################################################################################################################
# USD Asset Viewer | Build and Run Script
# TODO:
#
#####################################################################################################################################
# PYTHON
import os
import subprocess
import sys
import argparse
import tempfile
import glob
#####################################################################################################################################
parser = argparse.ArgumentParser(description="USD Asset Viewer Build and Run Script")
parser.add_argument("--run", action="store_true", help="run tool")
args = parser.parse_args()
#####################################################################################################################################
# SET VISUAL STUDIO PATH (WINDOWS)
#####################################################################################################################################
def find_vs_paths():
    drive_list = [f"{drive}:\\" for drive in "CDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{drive}:\\Program Files\\Microsoft Visual Studio")]
    if drive_list:
        vs_root = os.path.join(drive_list[0], "Program Files", "Microsoft Visual Studio")
    if not os.path.exists(vs_root):
        return []
    year_list = [directory for directory in os.listdir(vs_root) if directory.isdigit()]
    if not year_list:
        return []
    latest_year = max(year_list)
    editions = ["Community", "Professional", "Enterprise", "BuildTools"]
    found_paths = []
    for edition in editions:
        pattern = os.path.join(vs_root, latest_year, edition, "VC", "Auxiliary", "Build", "vcvarsall.bat")
        matches = glob.glob(pattern)
        found_paths.extend(matches)
    return found_paths
#####################################################################################################################################

os_type = os.name
build_directory = "build"
cmake_cache = os.path.join(build_directory, "CMakeCache.txt")
venv_directory = os.path.join(os.path.dirname(__file__), ".venv")
requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")


def build_usd_module_windows(python_path):
    vs_paths = find_vs_paths()
    for vs_path in vs_paths:
        if os.path.exists(vs_path):
            print(f"Setting up MSVC environment...")
            script_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD", "build_scripts", "build_usd.py")
            output_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_")
            with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as f:
                f.write(f'call "{vs_path}" x64\n')
                f.write(f'{python_path} "{script_path}" --ptex --usd-imaging "{output_path}"\n')
                batch_file = f.name
            subprocess.check_call([batch_file], shell=True)


def init_submodules():
    print("Initializing git submodules...")
    try:
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True, cwd=os.path.dirname(__file__))
        print("Sub-modules initialized successfully...")
        return True
    except subprocess.CalledProcessError:
        print("Warning: git not found")
        return False


def check_usd_build():
    include_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_")
    return os.path.exists(include_path)


def build_usd_module(python_path: str):
    print("Building git submodules...")
    script_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD", "build_scripts", "build_usd.py")
    output_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD")
    subprocess.run([python_path, script_path, "--ptex", "--usd-imaging", output_path])
    

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
    subprocess.call(venv_activate)


def install_python_dependencies(python_executable: str):
    print("Check/Install Python requirements...")
    subprocess.check_call([python_executable, "-m", "pip", "install", "-r", requirements_file])


def run(python_path: str):
    print("Running the USD Asset Viewer...")
    subprocess.run([python_path, "build_run.py", "--run"])


def build_run():
    init_submodules()
    python_path, venv_activate = setup_virtual_environment()
    activate_virtual_environment(venv_activate)
    install_python_dependencies(python_path)
    if not check_usd_build():
        if os_type == 'nt':
            build_usd_module_windows(python_path)
        else:
            build_usd_module(python_path)
    create_build()
    run_build_process()
    run(python_path)


#####################################################################################################################################


if not args.run:
    build_run()

else:
    python_path, venv_activate = setup_virtual_environment()
    activate_virtual_environment(venv_activate)
    import tool.base_tool as bt
    bt.USDAssetViewer()