#!/bin/bash
# Setup script for TRELLIS on Linux/Mac using uv

set -e

echo "========================================"
echo "TRELLIS Setup Script (Linux/Mac)"
echo "========================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "ERROR: 'uv' is not installed or not in PATH"
    echo ""
    echo "Please install uv first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo ""
    exit 1
fi

echo "[1/5] Found uv installation"
echo ""

# Check for CUDA
if command -v nvidia-smi &> /dev/null; then
    echo "[2/5] CUDA detected - GPU acceleration will be available"
    nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
else
    echo "[2/5] WARNING: CUDA/NVIDIA GPU not detected"
    echo "         The application will run on CPU (very slow)"
fi
echo ""

echo "[3/5] Installing Python dependencies with uv..."
echo "     This may take several minutes..."
echo ""
uv sync

echo ""
echo "[4/5] Building custom CUDA extensions (nvdiffrast)..."
echo ""
cd extensions/nvdiffrast
uv pip install .
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to build nvdiffrast"
    echo "         The app may still work with reduced performance"
fi
cd ../..

echo ""
echo "[5/5] Setup complete!"
echo ""
echo "========================================"
echo "You can now run TRELLIS with:"
echo "  uv run run.py"
echo ""
echo "Or for public sharing:"
echo "  uv run run.py --share"
echo "========================================"
echo ""
