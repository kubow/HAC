import pyqtgraph as pg
import numpy

data = numpy.random.normal(size=1000)
pg.plot(data, title="Simplest possible plotting example")

data = numpy.random.normal(size=(500,500))
pg.image(data, title="Simplest possible image example")


if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()


# Switch to using white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')