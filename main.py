import sys

from PySide6 import QtWidgets, QtGui
import resources

assert resources

from py_ballisticcalc import MultiBC, TableG7, Unit

__version__ = '1.0.0'


class MBC2DRG(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MBC2DRG")

        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setFixedSize(400, 250)
        self.resize(400, 250)

        self.lt = QtWidgets.QGridLayout(self)
        self.setLayout(self.lt)

        self.lt.addWidget(QtWidgets.QLabel("Velocity, mps"), 0, 0)
        self.lt.addWidget(QtWidgets.QLabel("BC, G7"), 0, 1)

        defdata = [
            {'BC': 0.393, "V": 914},
            {'BC': 0.386, "V": 762},
            {'BC': 0.374, "V": 609},
            {'BC': 0.37, "V": 452},
            {'BC': 0, "V": 0},
        ]

        self.velocities = [
            QtWidgets.QSpinBox(self),
            QtWidgets.QSpinBox(self),
            QtWidgets.QSpinBox(self),
            QtWidgets.QSpinBox(self),
            QtWidgets.QSpinBox(self),
        ]
        self.mbc = [
            QtWidgets.QDoubleSpinBox(self),
            QtWidgets.QDoubleSpinBox(self),
            QtWidgets.QDoubleSpinBox(self),
            QtWidgets.QDoubleSpinBox(self),
            QtWidgets.QDoubleSpinBox(self),
        ]

        for i in range(5):
            self.velocities[i].setRange(0, 2000)
            self.velocities[i].setSingleStep(1)
            self.velocities[i].setValue(defdata[i]["V"])
            self.mbc[i].setRange(0, 2)
            self.mbc[i].setSingleStep(0.001)
            self.mbc[i].setValue(defdata[i]["BC"])
            self.mbc[i].setDecimals(3)
            self.lt.addWidget(self.velocities[i], i + 1, 0)
            self.lt.addWidget(self.mbc[i], i + 1, 1)


        self.fl = QtWidgets.QFormLayout(self)
        self.lt.addLayout(self.fl, 6, 0, 1, 1)


        self.w = QtWidgets.QDoubleSpinBox(self)
        self.w.setRange(10, 1000)
        self.w.setSingleStep(1)
        self.w.setDecimals(1)
        self.w.setValue(300)

        self.d = QtWidgets.QDoubleSpinBox(self)
        self.d.setRange(0.1, 10)
        self.d.setSingleStep(0.1)
        self.d.setDecimals(3)
        self.d.setValue(0.338)

        self.l = QtWidgets.QDoubleSpinBox(self)
        self.l.setRange(0.1, 10)
        self.l.setSingleStep(0.1)
        self.l.setDecimals(3)
        self.l.setValue(1.7)

        self.fl.addRow(QtWidgets.QLabel("Weight, grain"), self.w)
        self.fl.addRow(QtWidgets.QLabel("Diameter, inch"), self.d)
        self.fl.addRow(QtWidgets.QLabel("Length, inch"), self.l)

        self.calculate = QtWidgets.QPushButton("Create .DRG")
        self.lt.addWidget(self.calculate, self.lt.rowCount()-1, 1, 1, 1)

        self.calculate.clicked.connect(self.get_cdm)

    def get_cdm(self):
        data = []

        for i in range(5):
            v = self.velocities[i].value()
            bc = self.mbc[i].value()
            if v > 0 and bc > 0:
                data.append({'BC': bc, "V": Unit.MPS(v)})

        w = Unit.GRAIN(self.w.value())
        d = Unit.INCH(self.d.value())
        cdm = MultiBC(TableG7, d, w, data).cdm

        self.save(cdm)

    def save(self, cdm):
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save the update file",
            "CDM.drg",
            "Plain text .drg (*.drg)"
        )

        w = round((Unit.GRAIN(self.w.value()) >> Unit.GRAM) / 1000, 6)
        d = round((Unit.INCH(self.d.value()) >> Unit.CENTIMETER) / 100, 6)
        ln = {round((Unit.INCH(self.l.value()) >> Unit.CENTIMETER) / 100, 6)}

        if filepath:
            with open(filepath, 'w') as fp:
                fp.write(f"CFM, {self.d.value()} undefined ({self.w.value()}gr), " +
                         f"{w}, {d}, {ln}, ".replace("0.", '.') +
                         f"Undefined\n")
                fp.writelines(
                    [f"{round(p['CD'], 6)}\t{round(p['Mach'], 6)}\n" for p in cdm]
                )



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MBC2DRG()
    icon = QtGui.QIcon(':/resources/icon1.ico')
    app.setWindowIcon(icon)
    window.show()

    window.activateWindow()
    app.exit(app.exec())


if __name__ == '__main__':
    main()
