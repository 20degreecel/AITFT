import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = [
    "torch",
    "rdkit",
    "pandas",
    "numpy",
    "scikit-learn",
    "requests",
    "tqdm"
]

print("=== SmartDTI Environment Verification ===")
for p in packages:
    try:
        __import__(p)
        print(f"[OK] {p} is already installed.")
    except ImportError:
        print(f"[..] {p} not found. Attempting installation...")
        try:
            install(p)
            print(f"[SUCCESS] {p} installed.")
        except Exception as e:
            print(f"[ERROR] Failed to install {p}: {e}")

print("\nNote: For Graph Neural Networks (GNNs), specialized libraries like 'torch-geometric' or 'DGL' should be installed matching your CUDA version.")
