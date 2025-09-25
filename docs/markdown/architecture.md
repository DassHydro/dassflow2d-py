# Architecture

This markdown documentation presents class diagrams of the project architecture, layer by layer.

The documentation is segmented in the following layers:
- User Layer
- Model Layer
- Resolution Layer

## User Layer

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

## Model Layer

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

### Mesh details

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

## Resolution Layer

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
