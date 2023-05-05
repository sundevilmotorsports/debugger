import sys
import getopt
import numpy as np
import serial
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
import pyqtgraph as pg
from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem, GLGridItem, GLAxisItem
from stl import mesh
from gyro_channel import GyroChannel

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
yawl = GyroChannel("yaw rate")
rolll = GyroChannel("roll rate")
pitchl = GyroChannel("pitch rate")
port = ""
window.setLayout(layout)
window.show()
view = GLViewWidget()

button = QPushButton("Reset Mesh")



# SDM-23 mesh
# x: longitudinal
# y: lateral
stl_mesh = mesh.Mesh.from_file('SDM23.STL')
points = stl_mesh.points.reshape(-1, 3)
faces = np.arange(points.shape[0]).reshape(-1, 3)
mesh_data = MeshData(vertexes=points, faces=faces)
mesh = GLMeshItem(meshdata=mesh_data, smooth=True, drawFaces=True, drawEdges=True, edgeColor=(0, 1, 0, 1))
def update():
    line = ser.readline().decode('utf-8')
    data = line.split(',')
    time = float(data[0])
    yaw = float(data[1])
    pitch = float(data[3])
    roll = float(data[2])
    dy = yawl.update(time, yaw)
    dr = rolll.update(time, roll)
    dp = pitchl.update(time, pitch)

    mesh.rotate(dy, 0, 0, 1)
    mesh.rotate(dr, 1, 0, 0)
    mesh.rotate(dp, 0, 1, 0)

def reset_mesh():
    mesh.rotate(0, 0, 0, 1, local=True)
    mesh.rotate(0, 1, 0, 0, local=True)
    mesh.rotate(0, 0, 1, 0, local=True)

button.clicked.connect(reset_mesh)


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hi:p:", ["port="])
    for opt, arg in opts:
        if opt == '-h':
            print("main.py -p <port>")
            sys.exit()
        elif opt in ("-p", "--port"):
            port = arg

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

    layout.addLayout(yawl)
    layout.addLayout(pitchl)
    layout.addLayout(rolll)
    layout.addWidget(button)

    ser = serial.Serial(port)
    ser.flushInput()

    timer = pg.QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(1)
    app.exec()

