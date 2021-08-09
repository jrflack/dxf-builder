from pathlib import Path
from typing import List, TypedDict, Optional, Union

import ezdxf
from ezdxf.document import Drawing
from ezdxf.layouts import Modelspace


class ShapeType:
    POLYLINE = "lines"
    ARC = "arc"
    MESH = "mesh"


class Shape(TypedDict):
    type: str
    xy_data: dict
    shape_specific_data: Optional[dict]
    hatch: bool


class DxfBuilder:
    drawing: Drawing
    msp: Modelspace
    shapes: List[Shape]

    def __init__(self,
                 shape: Union[List[Shape], Shape],
                 dxfversion: str = ezdxf.DXF2013):
        if not isinstance(shape, list):
            shape = [shape]

        self.shapes = shape
        self.drawing = ezdxf.new(dxfversion)
        self.msp = self.drawing.modelspace()

    def __build_drawing(self) -> Drawing:
        for shape in self.shapes:
            shape: Shape

            if shape.get("type") == ShapeType.POLYLINE:
                self.__add_lines_shape(shape)
            if shape.get("type") == ShapeType.ARC:
                self.__add_arc_shape(shape)
            if shape.get("type") == ShapeType.MESH:
                self.__add_mesh_shape(shape)

        return self.drawing

    def __add_mesh_shape(self, shape: Shape) -> None:
        mesh = self.msp.add_mesh()

        with mesh.edit_data() as mesh_data:
            mesh_data.vertices = list(shape.get("xy_data").values())
            mesh_data.faces = (shape.get("shape_specific_data") or dict()).get("faces", [])

    def __add_arc_shape(self, shape: Shape) -> None:

        shape_properties: dict
        shape_properties = shape.get("shape_specific_data", dict())

        if shape.get("hatch"):
            hatch = self.msp.add_hatch()
            edge_path = hatch.paths.add_edge_path()

            edge_path.add_arc(
                center=shape.get("xy_data").get("xy"),
                radius=float(shape_properties.get("radius", 1.0)),
                start_angle=float(shape_properties.get("start_angle", 0.0)),
                end_angle=float(shape_properties.get("angle", 360.0)),
            )

            return

        self.msp.add_arc(
            center=shape.get("xy_data").get("xy"),
            radius=float(shape_properties.get("radius", 1.0)),
            start_angle=float(shape_properties.get("start_angle", 0.0)),
            end_angle=float(shape_properties.get("angle", 360.0)),
        )

    def __add_lines_shape(self, shape: Shape) -> None:
        if shape.get("hatch"):
            hatch = self.msp.add_hatch()
            hatch.paths.add_polyline_path(list(shape.get("xy_data").values()))

            return

        self.msp.add_polyline2d(list(shape.get("xy_data").values()))

    def get_doc(self) -> Drawing:
        self.__build_drawing()

        return self.drawing

    def saveas(self, filename: Union[str, Path]):
        doc = self.__build_drawing()

        doc.saveas(filename)
