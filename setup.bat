@echo off
REM Setup script for TRELLIS on Windows using uv

echo ========================================
echo TRELLIS Setup Script (Windows)
echo ========================================
echo.

REM Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: 'uv' is not installed or not in PATH
    echo.
    echo Please install uv first:
    echo   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo.
    pause
    exit /b 1
)

echo [1/5] Found uv installation
echo.

REM Check for CUDA
nvidia-smi >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [2/5] CUDA detected - GPU acceleration will be available
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
) else (
    echo [2/5] WARNING: CUDA/NVIDIA GPU not detected
    echo          The application will run on CPU (very slow)
)
echo.

echo [3/5] Installing Python dependencies with uv...
echo      This may take several minutes...
echo.
uv sync
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

echo [4/5] Building custom CUDA extensions (nvdiffrast)...
echo      This requires Visual Studio Build Tools with C++ support
echo.
cd extensions\nvdiffrast
uv pip install .
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Failed to build nvdiffrast
    echo          The app may still work with reduced performance
    echo          To fix: Install Visual Studio Build Tools with C++ support
)
cd ..\..
echo.

echo [5/5] Setup complete!
echo.
echo ========================================
echo IMPORTANT: Windows Configuration
echo ========================================
echo This setup uses xformers for attention (flash-attn not available on Windows)
echo Performance will be slightly lower than Linux but still GPU-accelerated
echo.
echo ========================================
echo You can now run TRELLIS with:
echo   uv run run.py
echo.
echo Or for public sharing:
echo   uv run run.py --share
echo ========================================
echo.
pause
