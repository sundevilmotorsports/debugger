import sys
import getopt
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem, GLGridItem, GLAxisItem
from stl import mesh
from gyro_channel import GyroChannel

if __name__ == "__main__":
    port = ""
    app = QApplication(sys.argv)
    window = QWidget()
    layout = QVBoxLayout()

    window.setLayout(layout)
    window.show()
    view = GLViewWidget()

    opts, args = getopt.getopt(sys.argv[1:], "hi:p:", ["port="])
    for opt, arg in opts:
        if opt == '-h':
            print("main.py -p <port>")
            sys.exit()
        elif opt in ("-p", "--port"):
            port = arg

    # SDM-23 mesh
    # x: longitudinal
    # y: lateral
    stl_mesh = mesh.Mesh.from_file('SDM23.STL')
    points = stl_mesh.points.reshape(-1, 3)
    faces = np.arange(points.shape[0]).reshape(-1, 3)
    mesh_data = MeshData(vertexes=points, faces=faces)
    mesh = GLMeshItem(meshdata=mesh_data, smooth=True, drawFaces=True, drawEdges=True, edgeColor=(0, 1, 0, 1))
    mesh.rotate(90, 1, 0, 0) 
    mesh.rotate(90, 0, 0, 1)
    mesh.scale(0.1,0.1,0.1)
    mesh.translate(-3,-1.5,0)
    view.addItem(mesh)

    # grid
    grid = GLGridItem()
    grid.scale(2,2,1)
    view.addItem(grid)

    # axis
    axis = GLAxisItem()
    axis.setSize(5,-1,1)
    axis.scale(5,5,5)
    view.addItem(axis)

    view.show()

    yawl = GyroChannel("yaw rate")
    layout.addLayout(yawl)
    app.exec()

