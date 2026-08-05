'''
A script that goes through every vertex in a selected polygon or multipolygon layer
'''

from qgis.PyQt.QtGui import QKeySequence, QShortcut
from qgis.core import QgsPointXY

SCALE = 1/42500

canvas = iface.mapCanvas()

layer = iface.activeLayer()
features = list(layer.getFeatures())

if not features:
    raise Exception("No features in active layer!")

vertices = []

for feature in features:
    geom = feature.geometry()

    if geom.isMultipart():
        polygons = geom.asMultiPolygon()
    else:
        polygons = [geom.asPolygon()]

    for polygon in polygons:
        for ring in polygon:
            # Skip the duplicate closing vertex
            for pt in ring[:-1]:
                vertices.append(QgsPointXY(pt))

if not vertices:
    raise Exception("No vertices found!")

i = 0

def show_vertex():
    v = vertices[i]

    canvas.setCenter(v)
    canvas.zoomScale(SCALE)
    canvas.refresh()

    print(f"Vertex {i+1}/{len(vertices)}  ({v.x():.3f}, {v.y():.3f})")

def next_vertex():
    global i
    if i < len(vertices) - 1:
        i += 1
        show_vertex()

def back_vertex():
    global i
    if i > 0:
        i -= 1
        show_vertex()

# Jump to first vertex
show_vertex()

# Remove previous shortcuts
for name in ("next_shortcut", "back_shortcut"):
    if name in globals():
        try:
            globals()[name].activated.disconnect()
        except Exception:
            pass
        globals()[name].deleteLater()
        del globals()[name]

# Create new shortcuts
next_shortcut = QShortcut(QKeySequence("N"), iface.mainWindow())
back_shortcut = QShortcut(QKeySequence("B"), iface.mainWindow())

next_shortcut.activated.connect(next_vertex)
back_shortcut.activated.connect(back_vertex)

print(f"Loaded {len(features)} feature(s) with {len(vertices)} vertices.")
print("Controls:")
print("[N]ext vertex, [B]ack to previous vertex.")