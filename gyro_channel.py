from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from pyqtgraph import GraphicsLayoutWidget
import numpy as np

class GyroChannel(QHBoxLayout):
    def __init__(self, name: str):
        super(GyroChannel, self).__init__()
        self.name = name
        self.zero = 0
        self.prevTime = -1
        self.intValue = 0
        self.rawValues = np.zeros(500)
        self.intValues = np.zeros(500)
        self.ptr = 0        

        # GUI things
        self.nameLbl = QLabel(self.name)
        self.zeroLbl = QLabel("Zero value: ")
        self.zeroInput = QLineEdit()

        self.rawLabel = QLabel("Raw value: ")
        self.currLabel = QLabel("Current value: ")
        self.resetBtn = QPushButton("Reset integration")

        self.resetBtn.clicked.connect(self.resetIntegration)
        self.zeroInput.returnPressed.connect(self.setZeroValue)

        self.plotLayout = GraphicsLayoutWidget()
        self.plotRaw = self.plotLayout.addPlot(title=self.name)
        self.curveRaw = self.plotRaw.plot(self.rawValues)
        self.plotInt = self.plotLayout.addPlot(title=self.name + " integrated")
        self.curveInt = self.plotInt.plot(self.intValues)

        self.adjustLayout = QVBoxLayout()
        self.adjustLayout.addWidget(self.nameLbl)
        self.adjustLayout.addWidget(self.zeroLbl)
        self.adjustLayout.addWidget(self.zeroInput)
        self.adjustLayout.addWidget(self.rawLabel)
        self.adjustLayout.addWidget(self.currLabel)
        self.adjustLayout.addWidget(self.resetBtn)

        self.addLayout(self.adjustLayout)
        self.addWidget(self.plotLayout)

    def resetIntegration(self):
        self.intValue = 0

    def setZeroValue(self):
        self.zero = int(self.zeroInput.text())
        self.zeroLbl.setText("Zero value: " + str(self.zero))
        self.resetIntegration()

    def update(self, time: float, value: float):
        self.rawLabel.setText("Raw value: " + str(value))
        dt = 0
        if self.prevTime == -1:
            dt = time
        else:
            dt = time - prevTime
            prevTime = time

        if dt > 1: # skip integration if dt is large
            return self.intValue

        self.intValue += dt * value - self.zero

        # update plots
        self.rawValues[:-1] = self.rawValues[1:]
        self.intValues[:-1] = self.intValues[1:]
        self.rawValues[-1] = value
        self.intValues[-1] = self.intValue
        
        ptr += 1
        self.curveRaw.setData(self.rawValues)
        self.curveRaw.setPos(ptr, 0)
        self.curveInt.setData(self.intValues)
        self.curveInt.setPos(ptr, 0)

        # return change in rotation for mesh
        return dt * value - self.zero






