import os
import subprocess
import sys

build_dir = "build"
cmake_cache = os.path.join(build_dir, "CMakeCache.txt")

if not os.path.isfile(cmake_cache):
    print(f"CMake files not found. Generating CMake files in {build_dir}...")
    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    subprocess.check_call(["cmake", "-S", ".", "-B", build_dir])

print(f"Running CMake build in {build_dir}...")
subprocess.check_call(["cmake", "--build", build_dir, "--config", "Release"])

print("Running loader.py in the virtual environment...")
venv_activate = os.path.join(os.path.dirname(__file__), "../.venv/bin/activate")

if os.path.isfile(venv_activate):
    print("Activating virtual environment...")
    python_executable = os.path.join(os.path.dirname(venv_activate), "python")
else:
    python_executable = sys.executable

subprocess.check_call([python_executable, "loader.py"])