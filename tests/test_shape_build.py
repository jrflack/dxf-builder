import pytest
from _pytest.config import Config
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.document import Drawing
from ezdxf.entities import Arc, Mesh, PolylinePath, EdgePath, ArcEdge
from ezdxf.entities.hatch import Hatch
from ezdxf.entities.polyline import Polyline
from matplotlib import pyplot as plt

from dxf_builder import DxfBuilder
from .data import shapes


@pytest.fixture()
def should_show_plot(pytestconfig: Config) -> bool:
    return pytestconfig.getoption("show_plot")


def test_it_builds_shape_1(should_show_plot: bool):
    doc = DxfBuilder(shapes[0]).get_doc()

    show_plot(doc, should_show_plot)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)
    assert isinstance(entity, Polyline)

    entity: Polyline

    assert len(entity.vertices) == 11

    for vertex, coord in zip(entity.vertices, shapes[0]["xy_data"].values()):
        vx, vy, _ = vertex.format()

        assert (vx, vy,) == coord


def test_it_builds_shape_2(should_show_plot: bool):
    doc = DxfBuilder(shapes[1]).get_doc()

    show_plot(doc, should_show_plot)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)
    assert isinstance(entity, Polyline)

    entity: Polyline

    assert len(entity.vertices) == 2

    for vertex, coord in zip(entity.vertices, shapes[1]["xy_data"].values()):
        vx, vy, _ = vertex.format()

        assert (vx, vy,) == coord


def test_it_builds_shape_3(should_show_plot: bool):
    doc = DxfBuilder(shapes[2]).get_doc()

    show_plot(doc, should_show_plot)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)
    assert isinstance(entity, Hatch)

    entity: Hatch

    assert entity.has_solid_fill is True

    assert len(entity.paths.paths) == 1
    path = entity.paths.paths[0]

    assert isinstance(path, EdgePath)
    assert len(path.edges) == 1
    edge = path.edges[0]
    assert isinstance(edge, ArcEdge)

    assert edge.center == shapes[2]["xy_data"]["xy"]
    assert edge.radius == shapes[2]["shape_specific_data"]["radius"]
    assert edge.end_angle == shapes[2]["shape_specific_data"]["angle"]


def test_it_builds_shape_4(should_show_plot: bool):
    doc = DxfBuilder(shapes[3]).get_doc()

    show_plot(doc, should_show_plot)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)
    assert isinstance(entity, Arc)

    entity: Arc

    assert entity.dxf.get("center") == shapes[3]["xy_data"]["xy"]
    assert entity.dxf.get("radius") == shapes[3]["shape_specific_data"]["radius"]
    assert entity.dxf.get("end_angle") == shapes[3]["shape_specific_data"]["angle"]


def test_it_builds_shape_5(should_show_plot: bool):
    doc = DxfBuilder(shapes[5]).get_doc()

    show_plot(doc, should_show_plot)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)

    assert isinstance(entity, Mesh)

    entity: Mesh

    for vertex, expected in zip(entity.vertices, list(shapes[5]["xy_data"].values())):
        assert vertex == expected

    for face, expected in zip(entity.faces, list(shapes[5]["shape_specific_data"]["faces"])):
        assert face.tolist() == list(expected)


def test_it_builds_shape_6(should_show_plot: bool):
    doc = DxfBuilder(shapes[6]).get_doc()

    show_plot(doc, should_show_plot)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)

    entity: Hatch

    assert len(entity.paths.paths) == 1
    path = entity.paths.paths[0]

    path: PolylinePath

    for vertex, expected in zip(path.vertices, list(shapes[6]["xy_data"].values())):
        vertex = vertex[0], vertex[1]
        assert vertex == expected

    assert entity.has_pattern_fill is True


def show_plot(doc: Drawing, show: bool = False) -> None:
    if show is False:
        return

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(doc.modelspace(), finalize=True)
    fig.show()
