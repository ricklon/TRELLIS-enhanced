# TRELLIS Quick Start Guide

## Your System Configuration

✅ **GPU**: NVIDIA GeForce RTX 3070 (8GB VRAM)
✅ **CUDA**: Version 12.9
✅ **PyTorch**: 2.4.0+cu121 (CUDA enabled)
✅ **Attention Backend**: XFormers (flash-attn not available on Windows)
✅ **Status**: Ready to run!

**Note**: This Windows setup uses XFormers instead of flash-attention. Performance is excellent and fully GPU-accelerated, though slightly slower than flash-attention on Linux.

## Installation Complete

All dependencies have been installed successfully:
- PyTorch 2.4.0 with CUDA 12.1 support
- Gradio 4.44.1 with LitModel3D
- XFormers for efficient attention
- Spconv for sparse convolutions
- All other required packages (146 total)

## Running TRELLIS

### Basic Usage

```bash
uv run run.py
```

This will:
1. Set environment variables automatically
2. Load the TRELLIS model (downloads ~several GB on first run)
3. Launch Gradio interface at http://localhost:7860
4. Use your RTX 3070 GPU for acceleration

### With Public Sharing

To create a shareable public link:

```bash
uv run run.py --share
```

### Direct App Execution

You can also run the original app.py:

```bash
uv run python app.py
```

## Testing Your Setup

To verify everything is working:

```bash
uv run python test_setup.py
```

Expected output:
```
✓ PyTorch 2.4.0+cu121
  CUDA available: True
  GPU: NVIDIA GeForce RTX 3070
  GPU Memory: 8.0 GB
✓ All critical imports successful!
✓ Basic CUDA tensor operations working
✓ All tests passed! TRELLIS is ready to run.
```

## Usage Tips

### Memory Management

Your RTX 3070 has 8GB VRAM. To optimize:

1. **Close GPU applications**: Free up VRAM by closing:
   - LM Studio (if running)
   - Other GPU-intensive apps

2. **Adjust settings in UI**:
   - Texture Size: Use 1024 or 512 (instead of 2048)
   - Mesh Simplify: Keep at 0.95
   - Sampling Steps: Lower for faster generation

3. **Monitor memory**:
   ```bash
   nvidia-smi
   ```

### First Run

The first time you run TRELLIS:
- Model weights will download (~several GB)
- Background removal model (rembg) will download
- This only happens once

### Performance

Expected generation times on RTX 3070:
- Image preprocessing: ~1-2 seconds
- 3D generation: ~30-60 seconds
- GLB extraction: ~5-10 seconds

## Features

### Single Image Mode
1. Upload an image (or use examples)
2. Adjust generation settings (optional)
3. Click "Generate & Extract GLB"
4. Download your 3D model!

### Multi-Image Mode
1. Switch to "Multiple Images" tab
2. Upload 2-3 views of the object
3. Choose algorithm (stochastic or multidiffusion)
4. Generate 3D model from multiple angles

### Export Formats
- **GLB**: Standard 3D model format (smaller, ~few MB)
- **Gaussian Splatting**: Advanced format (~50MB, click "Extract Gaussian")

## Troubleshooting

### Out of Memory Error

If you see CUDA out of memory:
```bash
# Check GPU usage
nvidia-smi

# Free up memory by closing apps or reducing:
# - Texture size to 512
# - Image resolution
# - Close browser tabs
```

### Slow Generation

Check if using GPU:
```bash
uv run python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

Should show `CUDA: True`

### Model Download Issues

If model download fails:
```bash
# Set cache directory with more space
export HF_HOME=D:/huggingface_cache  # Windows
uv run run.py
```

## Project Structure

```
TRELLIS/
├── run.py              # UV runner (recommended)
├── app.py              # Original Gradio app
├── test_setup.py       # Installation test
├── pyproject.toml      # Dependencies
├── QUICKSTART.md       # This file
├── SETUP.md            # Detailed setup guide
├── trellis/            # Core library
│   ├── models/        # 3D generation models
│   ├── pipelines/     # Generation pipeline
│   └── renderers/     # Visualization
└── .venv/             # Virtual environment (created by uv)
```

## Commands Reference

```bash
# Run TRELLIS
uv run run.py

# Run with public sharing
uv run run.py --share

# Test installation
uv run python test_setup.py

# Update dependencies
uv sync

# Check GPU status
nvidia-smi

# Check CUDA in Python
uv run python -c "import torch; print(torch.cuda.is_available())"
```

## Advanced Configuration

### Environment Variables

Already set automatically by `run.py`:
```bash
SPCONV_ALGO=native
```

### Custom Model

Edit `run.py` line 42 to use different model:
```python
pipeline = TrellisImageTo3DPipeline.from_pretrained("your-model-here")
```

### Custom Port

Edit `run.py` line 59:
```python
demo.launch(server_port=8080)  # Change from 7860
```

## Resources

- **Paper**: https://huggingface.co/papers/2412.01506
- **Original Space**: https://huggingface.co/spaces/JeffreyXiang/TRELLIS
- **Model**: JeffreyXiang/TRELLIS-image-large

## Next Steps

1. Run `uv run run.py` to start TRELLIS
2. Open http://localhost:7860 in your browser
3. Upload an image or try examples
4. Generate your first 3D model!

---

**Ready to create 3D magic!** 🎨✨
