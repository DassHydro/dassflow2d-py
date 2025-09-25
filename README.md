# Dassflow2d-py

This repository is a translation and optimization of [dassflow2d](https://github.com/DassHydro/dassflow2d).
So far, only the direct translation is considered. The inverse problem will be tackled later.

---

## Description
This project aims to simulate water flows using the shallow water equations.

### Architecture

You can find the detailed architecture [here](docs/markdown/architecture.md)

---

### Future
The next steps of the project are to implement the resolution method for Euler x HLLC.
The algorithm for such implementation is already done. Here is the pseudo-code:

You can see extensive description of future work [here](docs/markdown/todo.md)

---

## Setup
To set up the project, we recommend using a virtual environment of your choice to manage package installation.
All packages needed are stored in `requirements.txt`, and you have to use `pip install -r requirements.txt` to install all of them.

### Venv
The Python virtual environment module is supported. You just have to run these two commands:
```bash
./scripts/venvinstall.sh
source .venv/bin/activate
```

### Anaconda

There is no Anaconda script to use, though you can do the same as with `venv`.
You will need to create a virtual environment, then use `pip install -r requirements.txt`.

---

## Run

To launch the application, please enter the following command
``` bash
python dassflow2d
```
with the correct arguments.
Change python with whatever python executable name you have (`py`, `python3` ...)

Note that a config file is required, you can find a demo file set in `docs/demo/`

---

## Contributions

This project is open to contributions. Feel free to fork and create a pull request!
