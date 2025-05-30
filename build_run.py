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
import pprint as pp

#####################################################################################################################################
USD_PATH = "" # USE IF MANUALLY BUILDING OR ALREADY HAVE USD BUILT
#####################################################################################################################################
parser = argparse.ArgumentParser()
parser.add_argument("--run", action="store_true")
args = parser.parse_args()
#####################################################################################################################################
os_type = os.name
if os_type == 'nt': python_name = "python"
else: python_name = "python3"
build_directory = "build"
cmake_cache = os.path.join(build_directory, "CMakeCache.txt")
venv_directory = os.path.join(os.path.dirname(__file__), ".venv")
requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
#####################################################################################################################################

def find_vs_path():
    common_path = "\\Program Files\\Microsoft Visual Studio"
    drive_list = [f"{drive}:\\" for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{drive}:{common_path}")]
    if drive_list:
        vs_root = os.path.join(drive_list[0], "Program Files", "Microsoft Visual Studio")
    if not os.path.exists(vs_root):
        return False
    year_list = [directory for directory in os.listdir(vs_root) if directory.isdigit()]
    if not year_list:
        return False
    latest_year = max(year_list)
    editions = ["Community", "Professional", "Enterprise", "BuildTools"]
    for edition in editions:
        path = os.path.join(vs_root, latest_year, edition, "VC", "Auxiliary", "Build", "vcvarsall.bat")
        if os.path.exists(path):
            return path


def run_python_command(command_list: list, venv: bool = True):
    """
    Run a Python command in the virtual environment.
    """
    if venv:
        if os_type == 'nt':
            venv_activate = os.path.join(os.path.dirname(__file__), ".venv/Scripts/activate.bat")
            command_list.insert(0, f'call "{venv_activate}"')
        else:
            venv_activate = os.path.join(os.path.dirname(__file__), ".venv/bin/activate")
            command_list.insert(0, f'. "{venv_activate}"')
    with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as file:
        for command in command_list:
            file.write(f'{command}\n')
        batch_file = file.name
    if os_type == 'nt':
        subprocess.check_call([batch_file], shell=True)
    else:
        os.chmod(batch_file, 0o755)
        subprocess.check_call([batch_file], shell=True)


def build_usd_module():
    usd_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD")
    script_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD", "build_scripts", "build_usd.py")
    output_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_")
    command_list = [f'{python_name} "{script_path}" --ptex --usd-imaging "{output_path}"\n']    
    if os_type == 'nt':
        vs_path = find_vs_path()
        if not vs_path:
            print("Visual Studio not found. Please install Visual Studio with C++ development tools.")
            return False
        command_list.insert(0, f'call "{vs_path}" x64\n',)
        run_python_command(command_list)
        return True
    else:
        command_list.insert(0, f'cd {usd_path}\n')        
        command_list.insert(1, f'{sys.executable} -m venv {os.path.join(usd_path, ".venv")}\n')
        command_list.insert(2, f'. {os.path.join(usd_path, ".venv", "bin", "activate")}\n')
        command_list.insert(3, f'pip install PySide6 PyOpenGL')
        command_list.append(f'rm -r .venv\n')
        run_python_command(command_list, venv=False)



def init_submodules():
    special_print("Initializing git submodules...")
    try:
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True, cwd=os.path.dirname(__file__))
        special_print("Sub-modules initialized successfully...")
    except subprocess.CalledProcessError:
        special_print("Warning: git not found")


def check_usd_build():
    if os.path.exists(USD_PATH):
        special_print("USD build found at:", USD_PATH)
        return True
    include_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_.flag")
    return os.path.exists(include_path)
    

def create_build():
    if not os.path.isfile(cmake_cache):
        special_print(f"Generating CMake files in {build_directory}...")
        if not os.path.isdir(build_directory):
            os.makedirs(build_directory)
        subprocess.check_call(["cmake", "-S", ".", "-B", build_directory])


def run_build_process():
    special_print(f"Running CMake in {build_directory}...")
    subprocess.check_call(["cmake", "--build", build_directory, "--config", "Release"])


def setup_virtual_environment():
    if not os.path.isdir(venv_directory):
        special_print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_directory])


def install_python_dependencies():
    special_print("Check/Install Python requirements...")
    run_python_command([f'{python_name} -m pip install -r "{requirements_file}"'])


def run():
    special_print("Running the USD Asset Viewer...")
    run_python_command([f"{python_name} build_run.py --run"])


def build_run():
    init_submodules()
    setup_virtual_environment()
    install_python_dependencies()
    usd_build = False
    if not check_usd_build():
        usd_build = build_usd_module()
    if usd_build:
        usd_built_flag = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_.flag")
        with open(usd_built_flag, "w") as f:
            f.write("USD build complete!\n")
    create_build()
    run_build_process()
    run()


def special_print(printable):
    """
    Print script notes
    """
    # Print each pound sign in a different ANSI color
    colors = ['\033[91m', '\033[92m', '\033[94m']  # Red, Green, Blue
    reset = '\033[0m'
    orange = '\033[95m'
    print(' '.join(f"{color}#{reset}" for color in colors), f"{orange}{printable}{reset}",)


#####################################################################################################################################


if not args.run:
    build_run()

else:
    if not USD_PATH:
        USD_PATH = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_", "lib", "python")
    sys.path.append(USD_PATH)
    import tool.base_tool as base_tool
    base_tool.USDAssetViewer()
