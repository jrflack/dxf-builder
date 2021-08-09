# dxf-builder

A python package to build DXF files from dict input

[comment]: <> (## Setup)

[comment]: <> (```)

[comment]: <> (pip install dxfbuilder # yet to publish)

[comment]: <> (```)

## Supported shape samples:

 - Polyline path

```python
{
    "type": "lines",
    "xy_data": {
        "coordinate_1": (10, 0),
        "coordinate_2": (10, 10),
        "coordinate_3": (20, 10),
        "coordinate_4": (30, 10),
    },
    "hatch": True or False
}
```

-  Arc

```python
{
    "type": "arc",
    "xy_data": {
        "xy": (-40, 0),  # Centre of the ellipse
    },
    "shape_specific_data": {
        "radius": 25,
        "angle": 360,  # Rotation of the ellipse in degrees (counterclockwise).
    },
    "hatch": True or False
}
```

- Mesh

```python
{
    "type": "mesh",
    "xy_data": {
        "vertex_1": (0, 0, 0),
        "vertex_2": (1, 0, 0),
        "vertex_3": (1, 1, 0),
        "vertex_4": (0, 1, 0),
        "vertex_5": (0, 0, 1),
        "vertex_6": (1, 0, 1),
        "vertex_7": (1, 1, 1),
        "vertex_8": (0, 1, 1),
    },
    "shape_specific_data": {
        "faces": [
            [0, 1, 2, 3],
            [4, 5, 6, 7],
            [0, 1, 5, 4],
            [1, 2, 6, 5],
            [3, 2, 6, 7],
            [0, 3, 7, 4],
        ]
    },
    "hatch": False # yet to implement hatch for mesh
}
```