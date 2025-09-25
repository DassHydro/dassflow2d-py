# dassflow2d-py

This repository is a translation and optimization of [dassflow2d](https://github.com/DassHydro/dassflow2d)
So far, only the direct translation is considered. The inverse problem will be tackled later.

## Description

This project aims to simulate water flows using the shallow water equations

### Architecture

Here you can find the architecture of the project in detail

User Layer:
<img width="352" height="511" alt="user" src="https://github.com/user-attachments/assets/a7bbc8d4-d423-4630-9704-29c075236aa4" />

Model Layer:
<img width="1733" height="776" alt="model" src="https://github.com/user-attachments/assets/7d831996-8d6f-4381-bd37-ff2b0e33a828" />

Mesh:
<img width="732" height="782" alt="mesh" src="https://github.com/user-attachments/assets/dedf536f-bc65-4d5a-9cd0-8f85e029fa4e" />

Resolution Layer:
<img width="1607" height="454" alt="resolution" src="https://github.com/user-attachments/assets/e46c3bc8-a586-4e05-9412-663e9a064bd8" />

### Future

The next stepts of the project is to implements the resolution method for euler x hllc.
The algorithm for such implementation is already done, here is the pseudo-code:
<img width="1241" height="1754" alt="pseudo-code" src="https://github.com/user-attachments/assets/04f4be64-80a3-41ae-92ec-fbf0d5807bf4" />

## Setup

To setup the project, we reccomend to use a virtual environment of your choice to manage packages installation.
All packages needed are stored in `requirements.txt` and you have to use `pip install -r requirements.txt` to install all of them.
Although this is simple, there is some support scripts for installation.

### Venv

Virtual environment python module is supported, you just have to run these two commands:

`./scripts/venvinstall.sh`
`source .venv/bin/activate`

### Anaconda

There is no anaconda script to use, though you can do the same as venv.
You will need to create a virtual environment, then use `pip install -r requirements.txt`

## Contributions

This project is open to contributions, feel free to fork and create a pull request
