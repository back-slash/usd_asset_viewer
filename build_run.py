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
import shutil
#####################################################################################################################################
USD_PATH = "" # Root directory for manually compiled OpenUSD
#####################################################################################################################################
parser = argparse.ArgumentParser()
parser.add_argument("--run", action="store_true")
parser.add_argument("--usd-path", type=str)
args = parser.parse_args()
if args.usd_path:
    USD_PATH = args.usd_path
#####################################################################################################################################
os_type = os.name
if os_type == 'nt': python_name = "python"
else: python_name = "python3"
build_directory = "build"
cmake_cache = os.path.join(build_directory, "CMakeCache.txt")
venv_directory = os.path.join(os.path.dirname(__file__), ".venv")
requirements_file = os.path.join(os.path.dirname(__file__), "requirements.txt")
capured_env = os.environ.copy()
#####################################################################################################################################


def run_python_command(command_list: list, venv: bool = True, cwd: str | None = None, env: dict = capured_env) -> None:
    """
    Run a Python command w/ or w/o virtual environment.
    """
    if venv:
        if os_type == 'nt':
            venv_activate = os.path.join(os.path.dirname(__file__), ".venv/Scripts/activate.bat")
            command_list.insert(0, f'call "{venv_activate}"')
        else:
            venv_activate = os.path.join(os.path.dirname(__file__), ".venv/bin/activate")
            command_list.insert(0, f'. "{venv_activate}"')
    file_type = ".bat" if os_type == 'nt' else ""
    with tempfile.NamedTemporaryFile(mode='w', suffix=file_type, delete=False) as file:
        for command in command_list:
            file.write(f'{command}\n')
        batch_file = file.name
    if os_type == 'nt':
        try:
            subprocess.run([batch_file], shell=True, env=env)
        except subprocess.CalledProcessError as e:
            special_print(f"Error running command: {e}")
            return
    else:
        os.chmod(batch_file, 0o755)
        try:
            subprocess.run([batch_file], shell=True, cwd=cwd, env=env)
        except subprocess.CalledProcessError as e:
            special_print(f"Error running command: {e}")
            return


def init_submodules() -> bool:
    """
    Initialize git submodules if they exist.
    """
    special_print("Initializing git sub-modules...")
    try:
        run_python_command(["git submodule update --init --recursive"], venv=False, cwd=os.path.dirname(__file__))
        special_print("Sub-modules initialized successfully...")
        return True
    except:
        return False


def check_usd_build(usd_path) -> bool:
    """
    Check if the USD build exists in the expected location.
    """
    build_flag_file = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_.flag")
    if os.path.exists(build_flag_file):
        return True
    elif os.path.exists(usd_path):
        special_print(f"USD build found at: {usd_path}")
        return True
    else:
        special_print("USD build not found...")
        return False


def build_usd_module() -> bool:
    """
    Build the USD module using the provided script.
    """
    script_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD", "build_scripts", "build_usd.py")
    output_path = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_")
    command_list = [f'{python_name} "{script_path}" --ptex --usd-imaging "{output_path}"\n']
    build = False
    if os_type == 'nt':
        vs_path = find_vs_path()
        if not vs_path:
            print("Visual Studio not found. Please build OpenUSD manually.")
            return False
        command_list.insert(0, f'call "{vs_path}" x64\n',)
        special_print("Using Visual Studio at: {vs_path}")
        special_print("Building OpenUSD...")
        run_python_command(command_list)
        build = os.path.exists(os.path.join(output_path, "lib", "python"))
    else:
        special_print("Building OpenUSD...")
        run_python_command(command_list, venv=True)
        build = os.path.exists(os.path.join(output_path, "lib", "python"))
    if build:
        usd_built_flag = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_.flag")
        with open(usd_built_flag, "w") as f:
            f.write("USD build completed successfully.")
    return build


def check_and_install(package):
    if not shutil.which("apt"):
        special_print("'apt' package manager not found.")
        return
    try:
        special_print(f"Checking for {package}...")
        subprocess.run(
            ["dpkg", "-s", package],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"{package} is already installed.")
    except:
        print(f"{package} not found. Installing...")
        subprocess.run(
            ["sudo", "apt", "update"], check=True
        )
        subprocess.run(
            ["sudo", "apt", "install", "-y", package], check=True
        )


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
        run_python_command([f"cmake -S . -B {build_directory}"], venv=False)


def run_build_process():
    """
    Run the build process using CMake.
    """
    special_print(f"Running CMake in directory: {build_directory}...")
    run_python_command([f"cmake --build {build_directory} --config Release"], venv=False)


def setup_virtual_environment():
    """
    Set up a virtual environment for the project if it does not already exist.
    """
    if not os.path.isdir(venv_directory):
        special_print("Creating virtual environment...")
        run_python_command([f'{python_name} -m venv {venv_directory}'], venv=False)


def install_python_dependencies():
    """
    Install Python dependencies from the requirements file.
    """
    special_print("Check/Install Python requirements...")
    run_python_command([f'{python_name} -m pip install -r "{requirements_file}"'])

def install_dependencies():
    """
    Install system dependencies.
    """
    if os_type != 'nt':
        check_and_install("git")
        check_and_install("python3-dev")
        check_and_install("python3-venv")
        check_and_install("cmake")        
        check_and_install("build-essential")
        check_and_install("libboost-all-dev")
        check_and_install("libxt-dev")
        check_and_install("libx11-dev")
        check_and_install("libgl1-mesa-dev")
        check_and_install("zlib1g-dev")

def run():
    """
    Run the USD Asset Viewer application.
    """
    special_print("Running the USD Asset Viewer...")
    env = os.environ.copy()
    global USD_PATH
    if not USD_PATH:
        USD_PATH = os.path.join(os.path.dirname(__file__), "external", "OpenUSD_")
    bin = os.path.join(USD_PATH, "bin")
    lib = os.path.join(USD_PATH, "lib")
    python_lib = os.path.join(USD_PATH, "lib", "python")
    env["PATH"] = str(bin) + os.pathsep + str(lib) + os.pathsep + os.environ.get("PATH", "")
    env["PYTHONPATH"] = str(python_lib) + os.pathsep + os.environ.get("PYTHONPATH", "")
    run_python_command([f"{python_name} build_run.py --run"], env=env)


def build_run():
    """
    Main function to build and run the USD Asset Viewer.
    """
    install_dependencies()
    if not init_submodules():
        special_print("Sub-module initialization failed. Please ensure git is installed.")
        return
    setup_virtual_environment()
    install_python_dependencies()
    if not check_usd_build(USD_PATH):
        build = build_usd_module()
    else:
        build = True
    if build:
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
# Entry

if not args.run:
    build_run()
else:
    import tool.base_tool as base_tool
    base_tool.USDAssetViewer()
