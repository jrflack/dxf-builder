import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from ezdxf.document import Drawing
from ezdxf.entities import Arc, Mesh
from ezdxf.entities.hatch import Hatch
from ezdxf.entities.polyline import Polyline
from ezdxf.lldxf.tags import Tags
from ezdxf.lldxf.tagwriter import TagCollector
from matplotlib import pyplot as plt

from src.dxf_builder import DxfBuilder
from .data import shapes

SHOW_PLOT = False


def test_it_builds_shape_1():
    doc = DxfBuilder(shapes[0]).get_doc()

    show_plot(doc)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)
    assert isinstance(entity, Polyline)

    entity: Polyline

    assert len(entity.vertices) == 11

    for vertex, coord in zip(entity.vertices, shapes[0]["xy_data"].values()):
        vx, vy, _ = vertex.format()

        assert (vx, vy,) == coord


def test_it_builds_shape_2():
    doc = DxfBuilder(shapes[1]).get_doc()

    show_plot(doc)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)
    assert isinstance(entity, Polyline)

    entity: Polyline

    assert len(entity.vertices) == 2

    for vertex, coord in zip(entity.vertices, shapes[1]["xy_data"].values()):
        vx, vy, _ = vertex.format()

        assert (vx, vy,) == coord


def test_it_builds_shape_3():
    doc = DxfBuilder(shapes[2]).get_doc()

    show_plot(doc)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)
    assert isinstance(entity, Hatch)

    entity: Hatch

    with open("test_shape_3.dxf", "r") as f:
        expected_doc = ezdxf.read(f)
        expected_hatch = next(entity for entity in expected_doc.entities)
        writer = TagCollector()
        expected_hatch.export_dxf(writer)
        expected = Tags(writer.tags)

    writer = TagCollector()
    entity.export_dxf(writer)
    tags = Tags(writer.tags)

    assert tags == expected


def test_it_builds_shape_4():
    doc = DxfBuilder(shapes[3]).get_doc()

    show_plot(doc)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)
    assert isinstance(entity, Arc)

    entity: Arc

    with open("test_shape_4.dxf", "r") as f:
        expected_doc = ezdxf.read(f)
        expected_entity = next(entity for entity in expected_doc.entities)
        writer = TagCollector()
        expected_entity.export_dxf(writer)
        expected = Tags(writer.tags)

    writer = TagCollector()
    entity.export_dxf(writer)
    tags = Tags(writer.tags)

    assert tags == expected


def test_it_builds_shape_5():
    doc = DxfBuilder(shapes[5]).get_doc()

    show_plot(doc)

    assert len(doc.entities) == 1
    entity = next(entity for entity in doc.entities)

    assert isinstance(entity, Mesh)

    entity: Mesh

    for vertex, expected in zip(entity.vertices, list(shapes[5]["xy_data"].values())):
        assert vertex == expected

    for face, expected in zip(entity.faces, list(shapes[5]["shape_specific_data"]["faces"])):
        assert face.tolist() == expected


def show_plot(doc: Drawing) -> None:
    if SHOW_PLOT is False:
        return

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    out = MatplotlibBackend(ax)
    Frontend(ctx, out).draw_layout(doc.modelspace(), finalize=True)
    fig.show()
