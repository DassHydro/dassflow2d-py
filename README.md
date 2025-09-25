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

```plaintext
Algorithm 1: Solve Euler HLLC
Data: Uⁿ, Δ, bathymetry
Result: Uⁿ⁺¹

1  flux_arêtes ← [];
2  for i ← 0 to longueur(arêtes) do
3      k ← arêtes[i].cellules₀;
4      Uₖ ← Uₖⁿ;
5      hₖ* ← well_balance(Uₖ.h);
6      Uₖ* ← (hₖ*, hₖ*Uₖ.u, hₖ*Uₖ.v);
7      kₑ ← arêtes[i].cellules₁;
8      Uₖₑ ← Uₖₑⁿ;
9      hₖₑ* ← well_balance(Uₖₑ.h);
10     Uₖₑ* ← (hₖₑ*, hₖₑ*Uₖₑ.u, hₖₑ*Uₖₑ.v);
11     Sₚ ← compute_sp(Uₖ.h, hₖ*);
12     normal ← arêtes[i].normal;
13     flux ← hllc_solver(Uₖ*, Uₖₑ*, normal);
14     flux_post_rotation ← rotation(R, flux);
15     id ← arêtes[i].id;
16     flux_arêtes[id] ← arêtes[i].length × flux_post_rotation + Sₚ;
17 end
18 Uⁿ⁺¹ ← [];
19 for k ← 0 to longueur(cellules) do
20     arêtes_cellule ← cellules[k].arêtes;
21     flux_total ← 0;
22     for i ← 0 to longueur(arêtes_cellule) do
23         arête ← arêtes_cellule[i];
24         flux_total ← flux_total + flux_arêtes[arête.id];
25     end
26     périmètre ← cellules[k].périmètre;
27     U̅ₖⁿ⁺¹ ← Uₖⁿ - (Δ / périmètre) × flux_total;
28     Uⁿ⁺¹ ← correction(U̅ₖⁿ⁺¹);
29 end
```


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

## Contributions

This project is open to contributions. Feel free to fork and create a pull request!
