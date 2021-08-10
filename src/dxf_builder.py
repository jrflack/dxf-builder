from enum import Enum
from pathlib import Path
from typing import List, TypedDict, Optional, Union

import ezdxf
from ezdxf.document import Drawing
from ezdxf.layouts import Modelspace


class StrEnum(str, Enum):
    ...


class ShapeType(StrEnum):
    POLYLINE = "lines"
    ARC = "arc"
    MESH = "mesh"
    RECT = "rectangle"


class GenericShapeProps:
    is_closed: bool
    color: int
    pattern_name: Optional[str]

    def __init__(self,
                 is_closed: bool,
                 color: int,
                 pattern_name: Optional[str]):
        self.is_closed = is_closed
        self.color = color
        self.pattern_name = pattern_name


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
            shape_type = shape.get("type")

            if ShapeType.POLYLINE == shape_type:
                self.__add_lines_shape(shape)
            if ShapeType.ARC == shape_type:
                self.__add_arc_shape(shape)
            if ShapeType.MESH == shape_type:
                self.__add_mesh_shape(shape)
            if ShapeType.RECT == shape_type:
                self.__add_polygon_shape(shape)

        return self.drawing

    def __add_polygon_shape(self, shape: Shape) -> None:
        shape_props = self.__get_generic_shape_props(shape)

        hatch = self.msp.add_hatch(color=shape_props.color)

        if shape_props.pattern_name is not None:
            hatch.set_pattern_fill(name=shape_props.pattern_name, color=shape_props.color)

        hatch.paths.add_polyline_path(
            path_vertices=self.__get_shape_vertices(shape),
            is_closed=shape_props.is_closed
        )

    def __add_mesh_shape(self, shape: Shape) -> None:
        shape_props = self.__get_generic_shape_props(shape)

        mesh = self.msp.add_mesh(dxfattribs=dict(
            color=shape_props.color
        ))

        with mesh.edit_data() as mesh_data:
            mesh_data.vertices = self.__get_shape_vertices(shape)
            mesh_data.faces = shape.get("shape_specific_data", dict()).get("faces", [])

    def __add_arc_shape(self, shape: Shape) -> None:
        shape_props = shape.get("shape_specific_data", dict())
        generic_shape_props = self.__get_generic_shape_props(shape)

        center = shape.get("xy_data").get("xy")
        radius = float(shape_props.get("radius", 1.0))
        start_angle = float(shape_props.get("start_angle", 0.0))
        end_angle = float(shape_props.get("angle", 360.0))

        if shape.get("hatch"):
            hatch = self.msp.add_hatch(color=generic_shape_props.color)

            if generic_shape_props.pattern_name is not None:
                hatch.set_pattern_fill(name=generic_shape_props.pattern_name, color=generic_shape_props.color)

            edge_path = hatch.paths.add_edge_path()

            edge_path.add_arc(
                center=center,
                radius=radius,
                start_angle=start_angle,
                end_angle=end_angle
            )

            return

        self.msp.add_arc(
            center=center,
            radius=radius,
            start_angle=start_angle,
            end_angle=end_angle,
            dxfattribs=dict(
                color=generic_shape_props.color
            )
        )

    def __add_lines_shape(self, shape: Shape) -> None:

        shape_props = self.__get_generic_shape_props(shape)

        if shape.get("hatch"):
            hatch = self.msp.add_hatch()
            hatch.paths.add_polyline_path(
                path_vertices=self.__get_shape_vertices(shape),
                is_closed=shape_props.is_closed,
            )

            return

        self.msp.add_polyline2d(
            points=self.__get_shape_vertices(shape),
            close=shape_props.is_closed,
        )

    @staticmethod
    def __get_generic_shape_props(shape: Shape) -> GenericShapeProps:
        shape_props = shape.get("shape_specific_data", dict())

        return GenericShapeProps(
            is_closed=bool(shape_props.get("is_closed", True)),
            color=int(shape_props.get("color", 7)),
            pattern_name=shape_props.get("pattern_name"),
        )

    @staticmethod
    def __get_shape_vertices(shape: Shape) -> list:
        return list(shape.get("xy_data").values())

    def get_doc(self) -> Drawing:
        self.__build_drawing()

        return self.drawing

    def saveas(self, filename: Union[str, Path]):
        doc = self.__build_drawing()

        doc.saveas(filename)
