import os
import subprocess
import sys

build_dir = "build"
cmake_cache = os.path.join(build_dir, "CMakeCache.txt")

if not os.path.isfile(cmake_cache):
    print(f"Generating CMake files in {build_dir}...")
    if not os.path.isdir(build_dir):
        os.makedirs(build_dir)
    subprocess.check_call(["cmake", "-S", ".", "-B", build_dir])

print(f"Running CMake build in {build_dir}...")
subprocess.check_call(["cmake", "--build", build_dir, "--config", "Release"])

print("Running in virtual env...")
venv_activate = os.path.join(os.path.dirname(__file__), "../.venv/bin/activate")

if os.path.isfile(venv_activate):
    print("Activating virtual environment...")
    python_executable = os.path.join(os.path.dirname(venv_activate), "python")
else:
    python_executable = sys.executable

subprocess.check_call([python_executable, "loader.py"])