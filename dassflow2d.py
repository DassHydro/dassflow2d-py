#!/usr/bin/env python3
import os
import sys

# Add src/main/py to PYTHONPATH
pythonpath = os.path.join('src', 'main', 'py')
os.environ["PYTHONPATH"] = f"{pythonpath}{os.pathsep}{os.environ.get('PYTHONPATH', '')}"

# Run the target script, passing all arguments
target_script = os.path.join('src', 'main', 'py', 'fr', 'dasshydro', 'dassflow2d_py', 'run_shallow_water_model.py')
os.execv(sys.executable, [sys.executable, str(target_script)] + sys.argv[1:])