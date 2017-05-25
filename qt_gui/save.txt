# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tab_widget.ui'
#
# Created: Thu May 25 20:19:34 2017
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

class MyHighlighter(QtGui.QSyntaxHighlighter):
    def __init__(self, parent):
        QtGui.QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlight_data = []
        
        self.matched_format = QtGui.QTextCharFormat()
        brush = QtGui.QBrush(QtCore.Qt.yellow, QtCore.Qt.SolidPattern)
        self.matched_format.setBackground(brush)
    '''
    def highlightBlock(self, text):
        index = 0
        length = 0
        for item in self.highlight_data:
            index = text.indexOf(item, index + length)
            length = len(item)
            self.setFormat(index, length, self.matched_format)
    '''
    def highlightBlock(self, text):
        index = 0
        length = 0
        is_change = True
        while is_change == True: #Attention point...
            is_change = False
            for item in self.highlight_data:
                if item.count('\n') != 0:
                    itemList = item.split('\n')
                    for part in itemList:
                        index = text.indexOf(part, index + length)
                        if index == -1:
                            index = 0
                        else:
                            length = len(part)
                            self.setFormat(index, length, self.matched_format)
                            is_change = True
                else:
                    index = text.indexOf(item, index + length)
                    if index != -1:
                        is_change = True
                    length = len(item)
                    self.setFormat(index, length, self.matched_format)
    
    def setHighlightData(self, highlight_data):
        self.highlight_data = highlight_data


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(834, 598)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget1 = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget1.setEnabled(True)
        self.tabWidget1.setGeometry(QtCore.QRect(6, -1, 791, 561))
        self.tabWidget1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget1.setStyleSheet(_fromUtf8("font: 75 italic 12pt \"Agency FB\";"))
        self.tabWidget1.setObjectName(_fromUtf8("tabWidget1"))
        self.tab_1 = QtGui.QWidget()
        self.tab_1.setObjectName(_fromUtf8("tab_1"))
        self.lineEdit1 = QtGui.QLineEdit(self.tab_1)
        self.lineEdit1.setGeometry(QtCore.QRect(40, 50, 600, 30))
        self.lineEdit1.setObjectName(_fromUtf8("lineEdit1"))
        self.label1 = QtGui.QLabel(self.tab_1)
        self.label1.setGeometry(QtCore.QRect(40, 10, 171, 31))
        self.label1.setObjectName(_fromUtf8("label1"))
        self.pushButton1 = QtGui.QPushButton(self.tab_1)
        self.pushButton1.setGeometry(QtCore.QRect(140, 90, 111, 31))
        self.pushButton1.setStyleSheet(_fromUtf8("font: 75 italic 12pt \"Agency FB\";"))
        self.pushButton1.setObjectName(_fromUtf8("pushButton1"))
        self.label2 = QtGui.QLabel(self.tab_1)
        self.label2.setGeometry(QtCore.QRect(40, 140, 600, 30))
        self.label2.setStyleSheet(_fromUtf8("font: 75 italic 12pt \"Agency FB\";"))
        self.label2.setText(_fromUtf8(""))
        self.label2.setObjectName(_fromUtf8("label2"))
        self.pushButton2 = QtGui.QPushButton(self.tab_1)
        self.pushButton2.setGeometry(QtCore.QRect(670, 140, 75, 31))
        self.pushButton2.setStyleSheet(_fromUtf8("font: 75 italic 12pt \"Agency FB\";"))
        self.pushButton2.setObjectName(_fromUtf8("pushButton2"))
        self.textEdit1 = QtGui.QTextEdit(self.tab_1)
        self.textEdit1.setGeometry(QtCore.QRect(30, 180, 721, 321))
        self.textEdit1.setStyleSheet(_fromUtf8("font: 12pt \"Agency FB\";"))
        self.textEdit1.setReadOnly(True)
        self.textEdit1.setObjectName(_fromUtf8("textEdit1"))
        self.pushButton3 = QtGui.QPushButton(self.tab_1)
        self.pushButton3.setGeometry(QtCore.QRect(40, 90, 75, 31))
        self.pushButton3.setObjectName(_fromUtf8("pushButton3"))
        self.checkBox1 = QtGui.QCheckBox(self.tab_1)
        self.checkBox1.setEnabled(True)
        self.checkBox1.setGeometry(QtCore.QRect(650, 60, 101, 16))
        self.checkBox1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.checkBox1.setStyleSheet(_fromUtf8("font: 75 12pt \"Agency FB\";"))
        self.checkBox1.setCheckable(True)
        self.checkBox1.setChecked(False)
        self.checkBox1.setObjectName(_fromUtf8("checkBox1"))
        self.tabWidget1.addTab(self.tab_1, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget1.addTab(self.tab_2, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 834, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.filename = u'../tag/medical_texts/中国高血压防治指南_.txt'
        self.highlighter = MyHighlighter(self.textEdit1)
        self.search_sent = u''
        

        self.retranslateUi(MainWindow)
        self.tabWidget1.setCurrentIndex(0)
        QtCore.QObject.connect(self.pushButton1, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.click_ok)
        QtCore.QObject.connect(self.pushButton2, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.click_file_load)
        QtCore.QObject.connect(self.pushButton3, QtCore.SIGNAL(_fromUtf8("clicked()")), MainWindow.click_search)
        QtCore.QObject.connect(self.checkBox1, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), MainWindow.check_tips)
        self.checkBox1.setChecked(True) #change the state artificially
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.pushButton1, self.pushButton2)
        MainWindow.setTabOrder(self.pushButton2, self.lineEdit1)
        MainWindow.setTabOrder(self.lineEdit1, self.textEdit1)
        MainWindow.setTabOrder(self.textEdit1, self.tabWidget1)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label1.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:20pt; font-style:italic;\">输入查询语句</span></p></body></html>", None))
        self.pushButton1.setText(_translate("MainWindow", "分析查询语句", None))
        self.pushButton2.setText(_translate("MainWindow", "读取文件", None))
        self.pushButton3.setText(_translate("MainWindow", " 查找", None))
        self.checkBox1.setText(_translate("MainWindow", "提示性提问", None))
        self.tabWidget1.setTabText(self.tabWidget1.indexOf(self.tab_1), _translate("MainWindow", "查询", None))
        self.tabWidget1.setTabText(self.tabWidget1.indexOf(self.tab_2), _translate("MainWindow", "其他", None))

    def click_ok(self):
        self.search_sent = unicode(self.lineEdit1.text().toUtf8(), 'utf-8', 'ignore')
        self.label2.setText(_fromUtf8(self.search_sent))

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
    
    def click_search(self):
        self.search_sent = unicode(self.lineEdit1.text().toUtf8(), 'utf-8', 'ignore')
        ###TODO...
        highlight_data = []
        highlight_data.append(self.search_sent)
        self.highlighter.setHighlightData(highlight_data)
        self.highlighter.rehighlight()
        ###DONE...
    
    def check_tips(self):
        if self.checkBox1.isChecked():
            print 'checked...'
        else:
            print 'not checked...'
