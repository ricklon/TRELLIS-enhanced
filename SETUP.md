# TRELLIS Setup Guide with UV

This guide will help you set up and run TRELLIS on your local machine with full GPU acceleration using `uv` (Astral's fast Python package manager).

## Prerequisites

### 1. Install UV

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. System Requirements

- **Python**: 3.10 (uv will handle this automatically)
- **GPU**: NVIDIA GPU with CUDA support (recommended)
- **CUDA**: Version 12.0 or 12.1
- **RAM**: 16GB+ recommended
- **VRAM**: 8GB+ recommended
- **Disk Space**: ~10GB for models and dependencies

### 3. GPU Drivers

Make sure you have up-to-date NVIDIA drivers installed:
```bash
nvidia-smi
```

This should show your GPU information and CUDA version.

## Quick Start

### Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup

If you prefer to set up manually:

```bash
# 1. Sync dependencies
uv sync

# 2. Build CUDA extensions (optional but recommended)
cd extensions/nvdiffrast
uv pip install .
cd ../..
```

## Running TRELLIS

### Basic Usage

```bash
# Run with uv
uv run run.py
```

The application will:
1. Check for GPU/CUDA availability
2. Download model weights on first run (~several GB)
3. Launch Gradio web interface at http://localhost:7860

### With Public Sharing

To create a public shareable link:
```bash
uv run run.py --share
```

### Direct Python Execution

You can also run the original app.py:
```bash
uv run python app.py
```

## Configuration

### Environment Variables

The following environment variable is automatically set by `run.py`:
- `SPCONV_ALGO=native` - Required for sparse convolution operations

### GPU Memory

If you encounter out-of-memory errors:
1. Close other GPU applications
2. Reduce texture_size in the UI
3. Lower mesh_simplify value

## Troubleshooting

### Issue: "CUDA not available"

**Check CUDA installation:**
```bash
nvidia-smi
```

**Check PyTorch CUDA:**
```bash
uv run python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### Issue: "nvdiffrast build failed"

This is optional. The app can run without it but with reduced performance.

**Windows:** Install Visual Studio Build Tools with C++ support:
- Download from: https://visualstudio.microsoft.com/downloads/
- Select "Desktop development with C++"

**Linux:** Install build essentials:
```bash
sudo apt-get install build-essential
```

### Issue: "Model download is slow"

The first run downloads several GB of model weights. This is normal and only happens once.

To use a different cache directory:
```bash
export HF_HOME=/path/to/cache
uv run run.py
```

### Issue: "Out of memory"

**Reduce memory usage:**
1. Lower the texture size (512 instead of 1024)
2. Reduce sampling steps
3. Close other applications using GPU

### Issue: "uv not found"

Make sure uv is in your PATH. After installation, restart your terminal or run:

**Windows:**
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

**Linux/Mac:**
```bash
source ~/.bashrc  # or ~/.zshrc
```

## Project Structure

```
TRELLIS/
├── pyproject.toml          # Project dependencies and configuration
├── run.py                  # UV-compatible runner script
├── app.py                  # Original Gradio application
├── setup.bat              # Windows setup script
├── setup.sh               # Linux/Mac setup script
├── SETUP.md               # This file
├── requirements.txt       # Legacy pip requirements
├── trellis/               # Main package
│   ├── models/           # 3D generation models
│   ├── pipelines/        # Generation pipelines
│   ├── representations/  # 3D representations (Gaussian, Mesh)
│   └── renderers/        # Rendering utilities
└── extensions/
    └── nvdiffrast/       # Custom CUDA rasterization
```

## Development

### Install development dependencies

```bash
uv sync --extra dev
```

### Run tests

```bash
uv run pytest
```

### Format code

```bash
uv run black .
```

## Advanced Usage

### Using Different Model

Edit `run.py` to change the model:
```python
pipeline = TrellisImageTo3DPipeline.from_pretrained("your-model-name")
```

### Custom Port

Edit `run.py` and change:
```python
demo.launch(server_port=8080)  # Change from 7860
```

### Batch Processing

For programmatic use without Gradio UI:
```python
import os
os.environ['SPCONV_ALGO'] = 'native'

from trellis.pipelines import TrellisImageTo3DPipeline
from PIL import Image

pipeline = TrellisImageTo3DPipeline.from_pretrained("JeffreyXiang/TRELLIS-image-large")
pipeline.cuda()

image = Image.open("your_image.png")
outputs = pipeline.run(image, seed=42, formats=["gaussian", "mesh"])
```

## Performance Tips

1. **First Run**: Model download takes time - be patient
2. **GPU Memory**: Close unnecessary applications
3. **Image Size**: Larger images take more time/memory
4. **Sampling Steps**: Fewer steps = faster but lower quality
5. **Texture Size**: Lower texture size reduces memory usage

## Getting Help

- **Paper**: https://huggingface.co/papers/2412.01506
- **Original Space**: https://huggingface.co/spaces/JeffreyXiang/TRELLIS
- **Issues**: Check the GitHub repository

## License

MIT License - See LICENSE file for details
