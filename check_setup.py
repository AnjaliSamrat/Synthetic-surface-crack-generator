#!/usr/bin/env python3
"""
Quick Setup Checker for Synthetic Surface Crack Generator
Run this script to verify your environment is set up correctly.

Usage: python check_setup.py
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Python 3.8+ required. Please upgrade Python.")
        return False
    return True

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print("\n📦 Checking Dependencies...")
    
    required_packages = {
        'tensorflow': 'TensorFlow',
        'numpy': 'NumPy',
        'matplotlib': 'Matplotlib',
        'jupyter': 'Jupyter',
    }
    
    all_installed = True
    for package, name in required_packages.items():
        if check_package(package):
            print(f"  ✓ {name} installed")
        else:
            print(f"  ❌ {name} NOT installed")
            all_installed = False
    
    return all_installed

def check_gpu():
    """Check if GPU is available for TensorFlow"""
    print("\n🎮 Checking GPU Availability...")
    try:
        import tensorflow as tf
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            print(f"  ✓ GPU detected: {len(gpus)} GPU(s) available")
            for gpu in gpus:
                print(f"    - {gpu.name}")
            return True
        else:
            print("  ℹ️  No GPU detected - will use CPU mode (slower but works!)")
            print("     To use free GPU: Open the notebook in Google Colab")
            return False
    except Exception as e:
        print(f"  ⚠️  Could not check GPU: {e}")
        return False

def print_next_steps(all_ok):
    """Print next steps based on setup status"""
    print("\n" + "="*60)
    if all_ok:
        print("✅ SETUP COMPLETE! You're ready to go!")
        print("\n📝 Next Steps:")
        print("   1. Start Jupyter Notebook:")
        print("      jupyter notebook")
        print("   2. Open: Synthetic_surface_cracked_generator.ipynb")
        print("   3. Run cells one by one (Shift + Enter)")
        print("\n📖 For detailed guide, see: ROADMAP.md")
    else:
        print("⚠️  SETUP INCOMPLETE")
        print("\n📝 To fix:")
        print("   1. Activate virtual environment:")
        print("      source venv/bin/activate  # Linux/macOS")
        print("      venv\\Scripts\\activate     # Windows")
        print("   2. Install dependencies:")
        print("      pip install -r requirements.txt")
        print("   3. Run this script again")
        print("\n📖 For help, see: ROADMAP.md (Troubleshooting section)")
    print("="*60)

def main():
    """Main setup checker"""
    print("="*60)
    print("🔍 Synthetic Surface Crack Generator - Setup Checker")
    print("="*60)
    
    # Check Python version
    python_ok = check_python_version()
    if not python_ok:
        print_next_steps(False)
        return
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check GPU (optional, won't fail the setup)
    check_gpu()
    
    # Print next steps
    print_next_steps(deps_ok)

if __name__ == "__main__":
    main()
