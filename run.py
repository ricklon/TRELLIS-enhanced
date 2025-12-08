#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRELLIS runner script compatible with uv
Sets up environment and launches the Gradio app
"""
import os
import sys

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Set environment variables before importing torch
os.environ['SPCONV_ALGO'] = 'native'
# Use xformers for attention (flash_attn not available on Windows)
os.environ['ATTN_BACKEND'] = 'xformers'

def main():
    """Main entry point for TRELLIS application"""
    print("Starting TRELLIS - Image to 3D Generation")
    print("=" * 50)

    # Import here to ensure environment is set
    import torch
    import numpy as np
    from PIL import Image
    from trellis.pipelines import TrellisImageTo3DPipeline

    # Check CUDA availability
    if torch.cuda.is_available():
        print(f"✓ CUDA is available")
        print(f"  GPU: {torch.cuda.get_device_name(0)}")
        print(f"  CUDA Version: {torch.version.cuda}")
        print(f"  Device Count: {torch.cuda.device_count()}")
    else:
        print("⚠ CUDA is NOT available - running on CPU (will be slow)")

    print("=" * 50)
    print("Loading TRELLIS pipeline...")
    print("This may take a while on first run (downloading model weights)")

    # Load the pipeline
    pipeline = TrellisImageTo3DPipeline.from_pretrained("JeffreyXiang/TRELLIS-image-large")

    if torch.cuda.is_available():
        pipeline.cuda()
        print("✓ Pipeline loaded on GPU")
    else:
        print("✓ Pipeline loaded on CPU")

    # Preload rembg (background removal)
    try:
        print("Preloading background removal model...")
        # Create a simple test image with actual values (not zeros) to avoid numpy warnings
        test_image = np.ones((512, 512, 3), dtype=np.uint8) * 128
        pipeline.preprocess_image(Image.fromarray(test_image))
        print("✓ Background removal model loaded")
    except Exception as e:
        print(f"⚠ Warning: Could not preload rembg: {e}")

    print("=" * 50)
    print("Launching Gradio interface...")

    # Import the app module and inject our initialized pipeline
    import app as app_module
    app_module.pipeline = pipeline

    # Launch with public sharing disabled by default (can be enabled with --share flag)
    share = "--share" in sys.argv

    # Try to launch on available port, starting from 7860
    max_attempts = 10
    base_port = int(os.environ.get('GRADIO_SERVER_PORT', 7860))

    for attempt in range(max_attempts):
        try:
            port = base_port + attempt
            print(f"Attempting to launch on port {port}...")
            app_module.demo.launch(
                server_name="0.0.0.0",  # Allow external access
                server_port=port,
                share=share
            )
            break  # Success - exit the loop
        except OSError as e:
            error_msg = str(e).lower()
            # Check if it's a port-in-use error (various forms)
            is_port_error = any([
                "address already in use" in error_msg,
                "10048" in str(e),
                "cannot find empty port" in error_msg
            ])

            if is_port_error:
                if attempt < max_attempts - 1:
                    print(f"Port {port} is in use, trying next port...")
                    continue
                else:
                    print(f"Could not find an available port after {max_attempts} attempts")
                    raise
            else:
                raise  # Re-raise if it's a different error

if __name__ == "__main__":
    main()
