shapes = [
    {
        "type": "lines",
        "xy_data": {
            "coordinate_1": (10, 0),
            "coordinate_2": (10, 10),
            "coordinate_3": (20, 10),
            "coordinate_4": (30, 10),
            "coordinate_5": (30, 10),
            "coordinate_6": (30, -30),
            "coordinate_7": (30, -30),
            "coordinate_8": (20, -30),
            "coordinate_9": (20, -30),
            "coordinate_10": (20, 0),
            "coordinate_11": (20, 0),
        },
        "hatch": False
    },
    {
        "type": "lines",
        "xy_data": {
            "coordinate_1": (10, 0),
            "coordinate_2": (10, 10),
        },
        "hatch": False
    },
    {
        "type": "arc",
        "xy_data": {
            "xy": (-55, 0),  # Centre of the ellipse
        },
        "shape_specific_data": {
            "radius": 10,  # TODO: Was missing in the sample data
            "angle": 360,  # Rotation of the ellipse in degrees (counterclockwise).
        },
        "hatch": True
    },
    {
        "type": "arc",
        "xy_data": {
            "xy": (-40, 0),  # Centre of the ellipse
        },
        "shape_specific_data": {
            "radius": 25,
            "angle": 360,  # Rotation of the ellipse in degrees (counterclockwise).
        },
        "hatch": False
    },
    {
        "type": "arc",
        "xy_data": {
            "xy": (-100, 0),  # Centre of the ellipse
        },
        "shape_specific_data": {
            "radius": 10,  # TODO: Was missing in the sample data
            "angle": 360,  # Rotation of the ellipse in degrees (counterclockwise).
        },
        "hatch": False
    },
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
                (0, 1, 2, 3),
                (4, 5, 6, 7),
                (0, 1, 5, 4),
                (1, 2, 6, 5),
                (3, 2, 6, 7),
                (0, 3, 7, 4),
            ],
            "color": 3
        },
        "hatch": False
    },
    {
        "type": "rectangle",
        "xy_data": {
            "coordinate_1": (0, 0),
            "coordinate_2": (10, 0),
            "coordinate_3": (10, 10),
            "coordinate_4": (0, 10),
        },
        "shape_specific_data": {
            "is_closed": True,  # default
            "pattern_name": "ANSI31",
            "color": 7  # default
        }
    }
]
