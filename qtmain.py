'''
Created on Jun 22, 2017

@author: bgrivna

Qt GUI main for rgbaggregator
'''

import os
import sys

from PyQt5 import QtWidgets

import rgb

class AggregatorWindow(QtWidgets.QWidget):
    def __init__(self, app):
        self.app = app
        self.lastFileDialogPath = os.path.expanduser("~")
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle("CSDCO/LacCore RGB Aggregator 0.0.2")
        
        self.rgbDirText = LabeledLineText(self, "RGB Directory")
        self.chooseRGBDirButton = QtWidgets.QPushButton("...", self)
        self.chooseRGBDirButton.clicked.connect(self.chooseRGBDir)
        self.outputPathText = LabeledLineText(self, "Output File")
        self.chooseOutputFileButton = QtWidgets.QPushButton("...", self)
        self.chooseOutputFileButton.clicked.connect(self.chooseOutputFile)
        
        vlayout = QtWidgets.QVBoxLayout(self)
        dirlayout = self.makeFileLayout(self.rgbDirText, self.chooseRGBDirButton, "Directory containing section RGB files - only *.csv files will be processed")
        vlayout.addLayout(dirlayout)
        outputlayout = self.makeFileLayout(self.outputPathText, self.chooseOutputFileButton, "File to which all section RGB data will be written")
        vlayout.addLayout(outputlayout)
        
        # average rows
        avgLayout = QtWidgets.QHBoxLayout()
        self.avgRowsCheckbox = QtWidgets.QCheckBox(self)
        self.avgRowsCheckbox.clicked.connect(self.avgRowsChecked)
        avgLayout.addWidget(self.avgRowsCheckbox)
        self.avgLabel1 = QtWidgets.QLabel("Average every")
        avgLayout.addWidget(self.avgLabel1)
        self.avgRowsText = QtWidgets.QLineEdit(self)
        self.avgRowsText.setMaximumWidth(50)
        avgLayout.addWidget(self.avgRowsText)
        self.avgLabel2 = QtWidgets.QLabel("rows of data")
        avgLayout.addWidget(self.avgLabel2)
        self.avgRowsChecked() # disable controls to match checkbox state
        avgLayout.addStretch(1) # push widgets to left
        vlayout.addLayout(avgLayout)
        
        vlayout.addWidget(QtWidgets.QLabel("Log!", self))
        self.logArea = QtWidgets.QTextEdit(self)
        self.logArea.setReadOnly(True)
        self.logArea.setToolTip("Big, Heavy, Wood!")
        vlayout.addWidget(self.logArea)
        
        self.aggButton = QtWidgets.QPushButton("Let's Aggregate!")
        self.aggButton.clicked.connect(self.aggregate)
        vlayout.addWidget(self.aggButton, stretch=1)

    def aggregate(self):
        rgbDir = self.rgbDirText.text()
        if not os.path.exists(rgbDir):
            self._warnbox("Badness", "RGB directory {} does not exist".format(rgbDir))
            return
        outFile = self.outputPathText.text()
        if not os.path.exists(os.path.dirname(outFile)):
            self._warnbox("Badness", "Destination directory {} does not exist".format(os.path.dirname(outFile)))
            return
        averageRows = None
        if self.avgRowsCheckbox.isChecked():
            try:
                averageRows = int(self.avgRowsText.text())
            except ValueError:
                self._warnbox("Badness", "Average Rows must be an integer > 1")
                return
            if averageRows < 2:
                self._warnbox("Badness", "Average Rows must be an integer > 1")
                return
        self.aggButton.setEnabled(False)
        self.logArea.clear()
        try:
            rgb.aggregateRGBFiles(rgbDir, outFile, averageRows, self)
        except Exception as err:
            self.report("\nSUPER FATAL ERROR: " + str(err))
        self.aggButton.setEnabled(True)
        
    def report(self, text, newline=True):
        text += "\n" if newline else ""
        self.logArea.insertPlainText(text)
        self.app.processEvents() # force GUI update
        
    def _warnbox(self, title, message):
        QtWidgets.QMessageBox.warning(self, title, message)
        
    def chooseRGBDir(self):
        dlg = QtWidgets.QFileDialog(self, "Choose RGB file directory", self.lastFileDialogPath)
        selectedDir = dlg.getExistingDirectory(self)
        if selectedDir != "":
            self.report("Selected RGB directory {}".format(selectedDir))
            self.rgbDirText.setText(selectedDir)
        
    def chooseOutputFile(self):
        dlg = QtWidgets.QFileDialog(self, "Choose output file", self.lastFileDialogPath)
        selectedFile, dummyFilter = dlg.getSaveFileName(self)
        if selectedFile != "":
            self.report("Selected output file {}".format(selectedFile))
            self.outputPathText.setText(selectedFile)
            
    def avgRowsChecked(self):
        checked = self.avgRowsCheckbox.isChecked()
        self.avgRowsText.setEnabled(checked)
        self.avgLabel1.setEnabled(checked)
        self.avgLabel2.setEnabled(checked)
    
    def makeDescLabel(self, desc):
        label = QtWidgets.QLabel(desc)
        label.setStyleSheet("QLabel {font-size: 11pt;}")
        return label
    
    # return layout with editText (includes label) and chooserButton on one line,
    # descText on the next with minimal vertical space between the two
    def makeFileLayout(self, editText, chooserButton, descText):
        layout = QtWidgets.QVBoxLayout()
        hlayout = QtWidgets.QHBoxLayout()
        hlayout.addWidget(editText)
        hlayout.addSpacing(10)
        hlayout.addWidget(chooserButton)
        layout.addLayout(hlayout)
        layout.setSpacing(0)
        layout.addWidget(self.makeDescLabel(descText))
        return layout

class LabeledLineText(QtWidgets.QWidget):
    def __init__(self, parent, label):
        QtWidgets.QWidget.__init__(self, parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        self.label = QtWidgets.QLabel(label, parent)
        self.edit = QtWidgets.QLineEdit(parent)
        layout.addWidget(self.label)
        layout.addSpacing(10)
        layout.addWidget(self.edit)
        
    def text(self):
        return self.edit.text()
    
    def setText(self, newText):
        self.edit.setText(newText)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AggregatorWindow(app)
    window.show()
    sys.exit(app.exec_())