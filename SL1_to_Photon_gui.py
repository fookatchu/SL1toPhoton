import glob
import os
import sys
import zipfile
import tempfile
import argparse
import pyphotonfile
from PIL import Image
# from IPython import embed

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from gui.ui_mainwindow import Ui_MainWindow


class SL1Reader:
    def __init__(self, filepath):
        self.zf = zipfile.ZipFile(filepath, 'r')
        self._read_config()
        self.n_layers = 0
        for filename in self.zf.namelist():
            if ".png" in filename:
                self.n_layers += 1

    def _read_config(self):
        try:
            config = self.zf.read('config.ini')
        except KeyError:
            print('ERROR: Did not find %s in zip file' % filename)
        else:
            self.config = {}
            for line in config.decode().splitlines():
                key, value = line.strip().split('=')
                self.config[key.strip()] = value.strip()

    def extract_images(self, dirpath):
        try:
            os.makedirs(dirpath)
        except OSError:
            pass
        for filename in self.zf.namelist():
            if ".png" in filename:
                data = self.zf.read(filename)
                with open(os.path.join(dirpath, filename), 'bw') as f:
                    f.write(data)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.progressBar.setFormat("%v / %m")
        self.progressBar.setTextVisible(False)
        self.assignWidgets()
        self.setAcceptDrops(True)
        self.show()

    # The following three methods set up dragging and dropping for the app
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        """
        Drop files directly onto the widget
        File locations are stored in fname
        :param e:
        :return:
        """
        if e.mimeData().hasUrls:
            e.setDropAction(Qt.CopyAction)
            e.accept()
            # Workaround for OSx dragging and dropping
            for url in e.mimeData().urls():
                fname = str(url.toLocalFile())
            self.set_in_file(fname)
            # self.load_image()
        else:
            e.ignore()

    def assignWidgets(self):
        self.pushButton_open_in.clicked.connect(self.open_in_file)
        self.pushButton_open_out.clicked.connect(self.open_out_file)
        self.pushButton_convert.clicked.connect(self.convert)

    def open_in_file(self):
        infile, selected_filter = QFileDialog.getOpenFileName(self, "Open SL1-File", "", "SL1-Files (*.sl1);;")
        self.set_in_file(infile)

    def set_in_file(self, filepath):
        self.lineEdit_infile.setText(filepath)
        base, ext = os.path.splitext(filepath)
        self.lineEdit_outfile.setText(base + ".photon")
        sl1 = SL1Reader(filepath)
        self.exposureSpinBox.setValue(float(sl1.config['expTime']))
        self.exposureBottomLayersSpinBox.setValue(float(sl1.config['expTimeFirst']))
        self.layerHeightDoubleSpinBox.setValue(float(sl1.config['layerHeight']))
        self.bottomLayersSpinBox.setValue(int(sl1.config['numFade']))

    def open_out_file(self):
        filename, selected_filter = QFileDialog.getSaveFileName(self, "Save as", "", "Photon-Files (*.photon);;", options=QFileDialog.DontConfirmOverwrite)
        self.lineEdit_outfile.setText(filename)

    def convert(self):
        infile = self.lineEdit_infile.text()
        outfile = self.lineEdit_outfile.text()

        if not os.path.exists(infile):
            ret = QMessageBox.warning(self, "SL1 to Photon Converter", "The selected SL1-File does not exist.", QMessageBox.Ok)
            return

        if os.path.exists(outfile):
            ret = QMessageBox.warning(self, "SL1 to Photon Converter", "The selected Photon-File already exists. Overwrite?", QMessageBox.Yes, QMessageBox.Cancel)
            if ret == QMessageBox.Cancel:
                return

        if outfile.strip() == "":
            ret = QMessageBox.warning(self, "SL1 to Photon Converter", "Please enter the path to the output file.", QMessageBox.Ok)
            return

        sl1 = SL1Reader(infile)
        photon = pyphotonfile.Photon()
        photon.exposure_time = self.exposureSpinBox.value()
        photon.exposure_time_bottom = self.exposureBottomLayersSpinBox.value()
        # photon.layer_height = self.layerHeightDoubleSpinBox.value()   # we don't want to mess with this
        photon.bottom_layers = self.bottomLayersSpinBox.value()

        self.progressBar.setMaximum(sl1.n_layers)
        self.progressBar.setTextVisible(True)
        with tempfile.TemporaryDirectory() as tmpdirname:
            sl1.extract_images(tmpdirname)
            for i, filepath in enumerate(glob.glob(os.path.join(tmpdirname, '*.png'))):
                Image.open(filepath).rotate(180).save(filepath)
                photon.append_layer(filepath)
                self.progressBar.setValue(i+1)
                QApplication.processEvents()
        photon.write(outfile)
        ret = QMessageBox.information(self, "SL1 to Photon Converter", "Done!", QMessageBox.Ok)


def parse_arguments():
    pass

if __name__ == '__main__':
    app = QApplication()
    app.setOrganizationName("Orgizm.net")
    app.setOrganizationDomain("orgizm.net")
    app.setApplicationName("SL1 to Photon Converter")
    mainWin = MainWindow()
    ret = app.exec_()
    sys.exit(ret)
