#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test script to verify TRELLIS installation
"""
import os
import sys

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ['SPCONV_ALGO'] = 'native'

def test_imports():
    """Test that all critical packages can be imported"""
    print("Testing imports...")

    try:
        import torch
        print(f"✓ PyTorch {torch.__version__}")
        print(f"  CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  CUDA version: {torch.version.cuda}")
            print(f"  GPU: {torch.cuda.get_device_name(0)}")
            print(f"  GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
        else:
            print("  ⚠ WARNING: CUDA not available - will run on CPU (very slow)")
    except ImportError as e:
        print(f"✗ PyTorch import failed: {e}")
        return False

    try:
        import torchvision
        print(f"✓ Torchvision {torchvision.__version__}")
    except ImportError as e:
        print(f"✗ Torchvision import failed: {e}")
        return False

    try:
        import gradio
        print(f"✓ Gradio {gradio.__version__}")
    except ImportError as e:
        print(f"✗ Gradio import failed: {e}")
        return False

    try:
        import spconv
        print(f"✓ Spconv (for sparse convolutions)")
    except ImportError as e:
        print(f"✗ Spconv import failed: {e}")
        return False

    try:
        import xformers
        print(f"✓ XFormers {xformers.__version__}")
    except ImportError as e:
        print(f"✗ XFormers import failed: {e}")
        return False

    try:
        from trellis.pipelines import TrellisImageTo3DPipeline
        print(f"✓ TRELLIS pipeline")
    except ImportError as e:
        print(f"✗ TRELLIS pipeline import failed: {e}")
        return False

    try:
        import rembg
        print(f"✓ Rembg (background removal)")
    except ImportError as e:
        print(f"✗ Rembg import failed: {e}")
        return False

    print("\n✓ All critical imports successful!")
    return True

def test_cuda_ops():
    """Test basic CUDA operations"""
    import torch

    if not torch.cuda.is_available():
        print("\n⚠ Skipping CUDA tests (no GPU available)")
        return True

    print("\nTesting CUDA operations...")
    try:
        # Create a small tensor on GPU
        x = torch.randn(10, 10).cuda()
        y = torch.randn(10, 10).cuda()
        z = torch.matmul(x, y)
        print(f"✓ Basic CUDA tensor operations working")

        # Test memory
        allocated = torch.cuda.memory_allocated() / 1024**2
        print(f"✓ GPU memory allocated: {allocated:.2f} MB")

        return True
    except Exception as e:
        print(f"✗ CUDA operations failed: {e}")
        return False

def main():
    print("=" * 60)
    print("TRELLIS Installation Test")
    print("=" * 60)
    print()

    if not test_imports():
        print("\n✗ Import test failed!")
        return 1

    if not test_cuda_ops():
        print("\n✗ CUDA test failed!")
        return 1

    print("\n" + "=" * 60)
    print("✓ All tests passed! TRELLIS is ready to run.")
    print("=" * 60)
    print()
    print("To start TRELLIS, run:")
    print("  uv run run.py")
    print()

    return 0

if __name__ == "__main__":
    exit(main())
