# Dassflow2d-py

This repository is a translation and optimization of [dassflow2d](https://github.com/DassHydro/dassflow2d).
So far, only the direct translation is considered. The inverse problem will be tackled later.

---

## Description
This project aims to simulate water flows using the shallow water equations.

### Architecture
Here you can find the architecture of the project in detail:

**User Layer:**
```mermaid
classDiagram
    class Configuration {
        + Configuration(source: T) c()
        + getTemporalScheme() TemporalScheme
        + getSpatialScheme() SpatialScheme
        + getMeshFileName() string
        + getBoundaryConditionFile() string
        + getInitialStateFileName() string
        + getBathymetryFileName() string
        + getHydrographsFile() string
        + getRatingCurveFile() string
        + getManningFileName() string
        + getResultFilePath() string
        + getOutputMode() OutputMode
        + getSimulationTime() float
        + getDeltaToWrite() float
        + getDefaultDelta() float
        + updateValues(values: Map~string, string~)
        + loadFromFile(filePath: string, source: T) Configuration
    }
```

**Model Layer:**
``` mermaid
classDiagram
    %% Enums
    class OutputMode {
        <<enumeration>>
        VTK
        TECPLOT
        GNUPLOT
        HDF5
    }

    class ResolutionMethod {
        <<interface>>
        + solve(dof: TimeStepState, delta: float, mesh: Mesh, bathymetry: Map~Cell, float~): TimeStepState
    }

    %% Abstract Classes
    class BoundaryCondition {
        <<abstract>>
        + getBoundaryType(): BoundaryType
        + update(bathy: Map~Cell, float~, state: TimeStepState, simtime: float)
    }

    %% Classes
    class ShallowWaterModel {
        + ShallowWater(cfg: Configuration) c()
        + run()
    }

    class Mesh {
        <<abstract>>
    }

    class AdaptiveTimeStep {
        + get_delta_using_cfl(mesh: Mesh, dof: TimeStepState): float
    }

    class ResultWriter {
        + ResultWriter(path: string, dtw: float) c()
        + isTimeToWrite(delta: float): boolean
        + save(result: TimeStepState, simtime: float)
        + writeAll(output_mode: OutputMode)
    }

    class TimeStepState {
        <<abstract>>
        - cellToNodeMap: Map~Cell, Node~
        + getNode(cell: Cell): Node
    }

    class Node {
        + h: float
        + u: float
        + v: float
    }

    %% Relationships
    ShallowWaterModel --> Mesh
    ShallowWaterModel "1" *-- "0.." BoundaryCondition
    ShallowWaterModel --> TimeStepState
    ShallowWaterModel --> ResultWriter
    ShallowWaterModel --> AdaptiveTimeStep
    ShallowWaterModel --> ResolutionMethod

    %% Relationships
    TimeStepState --> Node : "Value in Map"
```

**Mesh:**
``` mermaid
classDiagram
    %% Enums
    class BoundaryType {
        <<enumeration>>
        INFLOW
        OUTFLOW
        WALL
    }

    %% Abstract Classes
    class Mesh {
        <<abstract>>
        +getSurface(): float
        +getVertexNumber(): int
        +getVertices(): Vertex[]
        +getEdgeNumber(): int
        +getEdges(): Edge[]
        +getCellNumber(): int
        +getCells(): Cell[]
        +getBoundaryNumber(): int
        +getBoundaries(): Boundary[]
    }

    class Vertex {
        <<abstract>>
        +getCoordinates(): float[]
        +isBoundary(): boolean
    }

    class Cell {
        <<abstract>>
        +getSurface(): float
        +getPerimeter(): float
        +getVertices(): Vertex[]
        +getVertexNumber(): int
        +getEdges(): Edge[]
        +getNeighbors(): Cell[]
        +getGravityCenter(): float[]
        +isBoundary(): boolean
        +isGhost(): boolean
    }

    class Edge {
        <<abstract>>
        +getVertices(): Vertex[]
        +getCenter(): float[]
        +getLength(): float
        +getCells(): Cell[]
        +getNormalVector(): float[]
        +getFluxDirectionVector(): float[]
        +getVectorToCellCenter(cell: Cell): float[]
        +isBoundary(): boolean
        +getGhostCell(): Cell
    }

    class Boundary {
        <<abstract>>
        +getEdge(): Edge
        +getType(): BoundaryType
    }

    %% Relationships
    Mesh --* "0.." Vertex
    Mesh --* "0.." Cell
    Mesh --* "0.." Edge
    Mesh --o "0.." Boundary

    Boundary -->  Edge
    Boundary --> BoundaryType
```

**Resolution Layer:**
``` mermaid
classDiagram
    %% Enums
    class TemporalScheme {
        <<enumeration>>
        EULER
        SSP-RK2
        IMEX
    }

    class SpatialScheme {
        HLLC
        MUSCL
        LOW_FROUDE
    }

    %% Interfaces
    class ResolutionMethod {
        <<interface>>
        +solve(dof: TimeStepState, delta: float, mesh: Mesh, bathymetry: Map~Cell, float~): TimeStepState
    }

    class FrictionSourceTerm {
        <<interface>>
        +applyFriction(manning: float, manning_beta: float, dt: float, h: float, u: float, v: float): float[]
    }

    %% Concrete Implementations

    class EulerHLLC {
        <<concrete>>
    }

    %% Inheritance and Implementation Relationships
    ResolutionMethod <|.. EulerHLLC

    EulerHLLC -- FrictionSourceTerm
```

---

### Future
The next steps of the project are to implement the resolution method for Euler x HLLC.
The algorithm for such implementation is already done. Here is the pseudo-code:

<img width="1241" height="1754" alt="pseudo-code" src="https://github.com/user-attachments/assets/04f4be64-80a3-41ae-92ec-fbf0d5807bf4" />

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
