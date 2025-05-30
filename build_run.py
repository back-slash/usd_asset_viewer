#####################################################################################################################################
# USD Asset Viewer | Build and Run Script
# TODO:
# MACOS: Add support for building on macOS
#####################################################################################################################################
# PYTHON
import os
import subprocess
import sys
import argparse
import tempfile

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
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as file:
        for command in command_list:
            file.write(f'{command}\n')
        batch_file = file.name
    if os_type == 'nt':
        subprocess.check_call([batch_file], shell=True)
    else:
        os.chmod(batch_file, 0o755)
        subprocess.check_call([batch_file], shell=True)


def init_submodules():
    """
    Initialize git submodules if they exist.
    """
    special_print("Initializing git submodules...")
    try:
        subprocess.run(["git", "submodule", "update", "--init", "--recursive"], check=True, cwd=os.path.dirname(__file__))
        special_print("Sub-modules initialized successfully...")
        return True
    except subprocess.CalledProcessError:
        special_print("Warning: git not found...")
        return False


def check_usd_build():
    """
    Check if the USD build exists in the expected location.
    """
    if os.path.exists(USD_PATH):
        special_print("USD build found at:", USD_PATH)
        return True
    include_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_.flag")
    return os.path.exists(include_path)


def build_usd_module():
    """
    Build the USD module using the provided script.
    """
    usd_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD")
    script_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD", "build_scripts", "build_usd.py")
    output_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_")
    command_list = [f'{python_name} "{script_path}" --ptex --usd-imaging "{output_path}"\n']    
    if os_type == 'nt':
        vs_path = find_vs_path()
        if not vs_path:
            print("Visual Studio not found. Please build OpenUSD manually.")
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
        return True


# WELP
def find_vs_path():
    """
    Crudely find a path to Visual Studio installation.
    """
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


def create_build():
    """
    Create the build directory and generate CMake files if they do not exist.
    """
    if not os.path.isfile(cmake_cache):
        special_print(f"Generating CMake files in directory: {build_directory}...")
        if not os.path.isdir(build_directory):
            os.makedirs(build_directory)
        subprocess.check_call(["cmake", "-S", ".", "-B", build_directory])


def run_build_process():
    """
    Run the build process using CMake.
    """
    special_print(f"Running CMake in directory: {build_directory}...")
    subprocess.check_call(["cmake", "--build", build_directory, "--config", "Release"])


def setup_virtual_environment():
    """
    Set up a virtual environment for the project if it does not already exist.
    """
    if not os.path.isdir(venv_directory):
        special_print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", venv_directory])


def install_python_dependencies():
    """
    Install Python dependencies from the requirements file.
    """
    special_print("Check/Install Python requirements...")
    run_python_command([f'{python_name} -m pip install -r "{requirements_file}"'])


def run():
    """
    Run the USD Asset Viewer application.
    """
    special_print("Running the USD Asset Viewer...")
    run_python_command([f"{python_name} build_run.py --run"])


def build_run():
    """
    Main function to build and run the USD Asset Viewer.
    """
    if not init_submodules():
        special_print("Submodules initialization failed. Please ensure git is installed and try again.")
        return
    setup_virtual_environment()
    install_python_dependencies()
    usd_build = False
    if not check_usd_build():
        usd_build = build_usd_module()
    if usd_build:
        usd_built_flag = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_.flag")
        with open(usd_built_flag, "w") as f:
            f.write("USD build completed successfully.\n")
    create_build()
    run_build_process()
    run()


def special_print(printable):
    """
    Print build script output in a special way.
    """
    colors = ['\033[91m', '\033[92m', '\033[94m']
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
