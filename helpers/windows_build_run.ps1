$buildDir = "build"

if (-not (Test-Path (Join-Path $buildDir "CMakeCache.txt"))) {
    Write-Host "CMake files not found. Generating CMake files in $buildDir..."
    if (-not (Test-Path $buildDir)) {
        New-Item -ItemType Directory -Path $buildDir | Out-Null
    }
    cmake -S . -B $buildDir
}

Write-Host "Running CMake build in $buildDir..."
cmake --build $buildDir --config Release

Write-Host "Running loader.py in the virtual environment..."
$venvActivate = Join-Path $PSScriptRoot "..\.venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    Write-Host "Activating virtual environment..."
    & $venvActivate
}

python loader.py
