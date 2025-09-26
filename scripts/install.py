import os
import subprocess
import sys

def main():
    answer = input("Do you want to proceed with installation? (y/n) ").strip().lower()
    if answer == 'y':
        print("Proceeding with installation...")

        # Check if build module is installed, if not, install it
        try:
            import build # type: ignore
        except ImportError:
            print("The 'build' module is not installed. Installing it now...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "build"])

        # Build the package
        print("Building the package...")
        subprocess.check_call([sys.executable, "-m", "build"])

        # Install the produced .whl file
        print("Installing the produced .whl file...")
        whl_files = [f for f in os.listdir("dist") if f.endswith(".whl")]
        if whl_files:
            subprocess.check_call([sys.executable, "-m", "pip", "install", f"dist/{whl_files[0]}"])
            print("Installation completed!")
        else:
            print("No .whl file found in the dist directory.")
    else:
        print("Installation cancelled.")

if __name__ == "__main__":
    main()
