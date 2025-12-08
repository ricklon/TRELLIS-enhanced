# ✅ TRELLIS Installation Complete

## All Issues Resolved

Your TRELLIS installation is now **fully functional** with complete GPU acceleration!

### What Was Fixed

1. ✅ **PyTorch CUDA 12.1** - Installed with full RTX 3070 support
2. ✅ **XFormers Backend** - Configured as attention backend (flash-attn not available on Windows)
3. ✅ **Spaces Module** - Added HuggingFace Spaces support
4. ✅ **Nvdiffrast** - Built CUDA rendering extension
5. ✅ **Diff-Gaussian-Rasterization** - Built CUDA Gaussian splatting extension
6. ✅ **Windows Encoding** - Fixed UTF-8 issues throughout
7. ✅ **All Dependencies** - 146+ packages installed and verified

### Your System Configuration

- **GPU**: NVIDIA GeForce RTX 3070 (8GB VRAM)
- **CUDA**: 12.1 (compatible with driver 12.9)
- **PyTorch**: 2.4.0+cu121
- **Attention**: XFormers (GPU-accelerated)
- **Rendering**: Nvdiffrast + Diff-Gaussian-Rasterization (both with CUDA)

## Running TRELLIS

### Start the Application

```bash
uv run run.py
```

The server will start at: **http://localhost:7860**

### With Public Sharing

```bash
uv run run.py --share
```

This creates a public link you can share.

## Features Available

### Single Image to 3D
1. Upload an image (PNG, JPG, etc.)
2. Automatic background removal
3. Generate 3D model
4. Export as GLB file
5. Optional: Extract Gaussian splatting file (.ply)

### Multi-Image to 3D (Experimental)
1. Upload 2-3 views of an object
2. Choose algorithm (stochastic or multidiffusion)
3. Generate unified 3D model

### Settings You Can Adjust

**Generation Quality:**
- Sparse Structure Sampling Steps (default: 12)
- Structured Latent Sampling Steps (default: 12)
- Guidance Strength (controls how closely it follows the image)

**Output Quality:**
- Texture Size: 512, 1024, or 2048 (higher = better quality, more VRAM)
- Mesh Simplify: 0.90-0.98 (higher = more detail, larger file)

## Performance Expectations

On your RTX 3070:

| Task | Expected Time |
|------|---------------|
| Background Removal | 1-2 seconds |
| Sparse Structure Generation | 5-10 seconds |
| Latent Generation | 5-8 seconds |
| Mesh Extraction | 3-5 seconds |
| Video Rendering | 5-10 seconds |
| **Total** | **~30-45 seconds** |

## Memory Management

Your RTX 3070 has 8GB VRAM. Tips for optimal performance:

1. **Close GPU Applications**: Free up VRAM by closing:
   - LM Studio
   - Other AI models
   - Games or 3D applications

2. **Adjust Texture Size**:
   - Use 512 for quick previews
   - Use 1024 for balanced quality (recommended)
   - Use 2048 only if needed (uses more VRAM)

3. **Monitor GPU**:
   ```bash
   nvidia-smi
   ```

## Known Warnings (Safe to Ignore)

You'll see these warnings - they're **normal and harmless**:

- ⚠️ `Triton is not available` - Not needed on Windows
- ⚠️ `FutureWarning: torch.library.impl_abstract` - PyTorch deprecation
- ⚠️ `FutureWarning: torch.cuda.amp.custom_fwd` - Spconv deprecation
- ⚠️ `Could not preload rembg` - Background removal still works

## Troubleshooting

### Out of Memory Error

**Symptoms**: CUDA out of memory error during generation

**Solutions**:
1. Lower texture size to 512
2. Close other GPU applications
3. Restart the application
4. Check GPU usage: `nvidia-smi`

### Generation Fails

**Symptoms**: Error during generation

**Solutions**:
1. Check image format (PNG/JPG recommended)
2. Try a different image
3. Lower sampling steps
4. Restart the application

### Slow Performance

**Symptoms**: Takes longer than expected

**Check**:
```bash
uv run python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

Should show `CUDA: True`. If False, PyTorch isn't using GPU.

### Server Won't Start

**Symptoms**: Port already in use

**Solution**:
```bash
# Check what's using port 7860
netstat -ano | findstr :7860

# Kill the process or change port in run.py (line 64)
```

## Advanced Usage

### Batch Processing (Programmatic)

Create a script `batch_process.py`:

```python
import os
os.environ['SPCONV_ALGO'] = 'native'
os.environ['ATTN_BACKEND'] = 'xformers'

from PIL import Image
from trellis.pipelines import TrellisImageTo3DPipeline
from trellis.utils import postprocessing_utils

# Load pipeline
pipeline = TrellisImageTo3DPipeline.from_pretrained("JeffreyXiang/TRELLIS-image-large")
pipeline.cuda()

# Process multiple images
images = ["chair.png", "table.png", "lamp.png"]

for img_path in images:
    image = Image.open(img_path)
    processed = pipeline.preprocess_image(image)

    outputs = pipeline.run(
        processed,
        seed=42,
        formats=["gaussian", "mesh"],
        preprocess_image=False
    )

    # Save GLB
    glb = postprocessing_utils.to_glb(
        outputs['gaussian'][0],
        outputs['mesh'][0],
        simplify=0.95,
        texture_size=1024
    )
    glb.export(f"{img_path.replace('.png', '.glb')}")
    print(f"✓ Generated {img_path}")
```

Run with:
```bash
uv run python batch_process.py
```

### Custom Model Settings

Edit `run.py` to change default parameters:

```python
# Line 42 - Use different model
pipeline = TrellisImageTo3DPipeline.from_pretrained("your-model-name")

# Line 64 - Change port
server_port=8080,  # Instead of 7860
```

## Project Structure

```
TRELLIS/
├── run.py                          # Main runner (use this)
├── app.py                          # Gradio UI application
├── pyproject.toml                  # Dependencies (managed by UV)
├── test_setup.py                   # Verification script
├── INSTALLATION_COMPLETE.md        # This file
├── QUICKSTART.md                   # Quick reference
├── SETUP.md                        # Detailed setup guide
├── trellis/                        # Core library
│   ├── models/                     # 3D generation models
│   ├── pipelines/                  # Generation pipelines
│   ├── renderers/                  # Rendering (nvdiffrast, gaussian)
│   ├── representations/            # 3D formats (Gaussian, Mesh)
│   └── utils/                      # Utilities
├── extensions/
│   └── nvdiffrast/                # CUDA rendering extension
└── .venv/                          # Virtual environment

```

## Installed CUDA Extensions

All built successfully for Windows:

1. **nvdiffrast** - Differentiable rendering
   - Source: Local extensions/nvdiffrast
   - Version: 0.3.3
   - Status: ✅ Built with CUDA 12.1

2. **diff-gaussian-rasterization** - Gaussian splatting
   - Source: https://github.com/graphdeco-inria/diff-gaussian-rasterization
   - Version: 0.0.0
   - Status: ✅ Built with CUDA 12.1

## Files You Can Run

```bash
# Main application (recommended)
uv run run.py

# Verify installation
uv run python test_setup.py

# Direct app (alternative)
uv run python app.py

# Batch processing (create your own)
uv run python batch_process.py
```

## Next Steps

1. **Start TRELLIS**: `uv run run.py`
2. **Open browser**: http://localhost:7860
3. **Try an example**: Click on example images
4. **Generate your first 3D model**: Upload an image and click "Generate & Extract GLB"
5. **Download**: Get your GLB file and view in 3D software

## Resources

- **Paper**: https://huggingface.co/papers/2412.01506
- **Original Demo**: https://huggingface.co/spaces/JeffreyXiang/TRELLIS
- **Model**: JeffreyXiang/TRELLIS-image-large

## Support

If you encounter issues:

1. Check this document's troubleshooting section
2. Run `uv run python test_setup.py` to verify installation
3. Check GPU with `nvidia-smi`
4. Review the terminal output for error messages

---

**You're all set! TRELLIS is ready to generate 3D models from images with full GPU acceleration.** 🎉

Last updated: 2025-12-08
Installation: Complete
GPU: RTX 3070 ✅
CUDA: 12.1 ✅
Status: Fully Operational ✅
