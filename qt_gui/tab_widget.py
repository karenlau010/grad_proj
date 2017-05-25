# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tab_widget.ui'
#
# Created: Thu May 25 13:26:52 2017
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget1 = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget1.setGeometry(QtCore.QRect(6, -1, 791, 561))
        self.tabWidget1.setStyleSheet(_fromUtf8("font: 75 italic 12pt \"Agency FB\";"))
        self.tabWidget1.setObjectName(_fromUtf8("tabWidget1"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.lineEdit1 = QtGui.QLineEdit(self.tab_1)
        self.lineEdit1.setGeometry(QtCore.QRect(40, 50, 361, 31))
        self.lineEdit1.setObjectName(_fromUtf8("lineEdit1"))
        self.label1 = QtGui.QLabel(self.tab_1)
        self.label1.setGeometry(QtCore.QRect(40, 10, 171, 31))
        self.label1.setObjectName(_fromUtf8("label1"))
        self.pushButton1 = QtGui.QPushButton(self.tab_1)
        self.pushButton1.setGeometry(QtCore.QRect(40, 90, 75, 31))
        self.pushButton1.setStyleSheet(_fromUtf8("font: 75 italic 12pt \"Agency FB\";"))
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))
        self.label2 = QtGui.QLabel(self.tab_1)
        self.label2.setGeometry(QtCore.QRect(60, 140, 351, 21))
        self.label2.setStyleSheet(_fromUtf8("font: 75 italic 12pt \"Agency FB\";"))
        self.label2.setText(_fromUtf8(""))
        self.label2.setObjectName(_fromUtf8("label2"))
        self.pushButton2 = QtGui.QPushButton(self.tab_1)
        self.pushButton2.setGeometry(QtCore.QRect(670, 140, 75, 31))
        self.pushButton2.setStyleSheet(_fromUtf8("font: 75 italic 12pt \"Agency FB\";"))
        self.pushButton2.setObjectName(_fromUtf8("pushButton2"))
        self.textEdit1 = QtGui.QTextEdit(self.tab_1)
        self.textEdit1.setGeometry(QtCore.QRect(30, 180, 721, 321))
        self.textEdit1.setReadOnly(True)
        self.textEdit1.setObjectName(_fromUtf8("textEdit1"))
        self.tabWidget1.addTab(self.tab_1, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget1.addTab(self.tab_2, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.filename = u'../tag/after_tag/中国高血压防治指南_.txt_mm_ner_rrule'

        self.retranslateUi(MainWindow)
        self.tabWidget1.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton1, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.click_ok)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.click_file_load)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label1.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; font-style:italic;\">输入查询语句</span></p></body></html>", None))
        self.pushButton1.setText(_translate("MainWindow", "确定", None))
        self.pushButton2.setText(_translate("MainWindow", "读取文件", None))
        self.tabWidget1.setTabText(self.tabWidget1.indexOf(self.tab_1), _translate("MainWindow", "查询", None))
        self.tabWidget1.setTabText(self.tabWidget1.indexOf(self.tab_2), _translate("MainWindow", "其他", None))

    def click_ok(self):
        input_text = unicode(self.lineEdit1.text().toUtf8(), 'utf-8', 'ignore')
        print input_text, type(input_text)
        self.label2.setText(_fromUtf8(input_text))

    def click_file_load(self):
        fh = None
        try:
            fh = QtCore.QFile(self.filename)
            if not fh.open(QtCore.QIODevice.ReadOnly):
                raise IOError(str(fh.errorString()))
            stream = QtCore.QTextStream(fh)
            stream.setCodec("UTF-8")
            self.textEdit1.setPlainText(stream.readAll())
            self.textEdit1.document().setModified(False)
        except EnvironmentError as e:
            QMessageBox.warning(self, "Python Editor -- Load Error",
                    "Failed to load {0}: {1}".format(self.filename, e))
        finally:
            if fh is not None:
                fh.close()