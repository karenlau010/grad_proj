from PyQt4.QtCore import *  
from PyQt4.QtGui import *  
import sys  
   
class TextEdit(QTextEdit):  
   
    def __init__(self,parent=None):  
        super(TextEdit,self).__init__(parent)  
        self.cmp=None  
   
    def setCompleter(self,completer):  
        if self.cmp:  
            self.disconnect(self.cmp,0,0)  
        self.cmp=completer  
        if (not self.cmp):  
            return  
        self.cmp.setWidget(self)  
        self.cmp.setCompletionMode(QCompleter.PopupCompletion)  
        self.cmp.setCaseSensitivity(Qt.CaseInsensitive)  
        self.connect(self.cmp,SIGNAL('activated(QString)'),self.insertCompletion)  
   
    def completer(self):  
        return self.cmp  
   
    def insertCompletion(self,string):  
        tc=self.textCursor()  
        tc.movePosition(QTextCursor.StartOfWord,QTextCursor.KeepAnchor)  
        tc.insertText(string)  
        self.setTextCursor(tc)  
   
    def textUnderCursor(self):  
        tc=self.textCursor()  
        tc.select(QTextCursor.WordUnderCursor)  
        return tc.selectedText()  
   
    def keyPressEvent(self,e):  
        print(e.text())  
        if (self.cmp and self.cmp.popup().isVisible()):  
            if e.key() in (Qt.Key_Enter,Qt.Key_Return,Qt.Key_Escape,Qt.Key_Tab,Qt.Key_Backtab):  
                e.ignore()  
                return  
        isShortcut=((e.modifiers() & Qt.ControlModifier) and e.key()==Qt.Key_E)  
        if (not self.cmp or not isShortcut):  
            super(TextEdit,self).keyPressEvent(e)  
   
        ctrlOrShift = e.modifiers() & (Qt.ControlModifier | Qt.ShiftModifier)  
        if (not self.cmp or (ctrlOrShift and e.text().isEmpty())):  
            return  
   
        eow=QString("~!@#$%^&*()_+{}|:\"<>?,./;'[]\\-=")  
        hasModifier = (e.modifiers() != Qt.NoModifier) and not ctrlOrShift  
        completionPrefix = self.textUnderCursor()  
        if (not isShortcut and (hasModifier or e.text().isEmpty() or completionPrefix.length()<2  
                       or eow.contains(e.text().right(1)))):  
            self.cmp.popup().hide()  
            return  
        self.cmp.update(completionPrefix)  
        self.cmp.popup().setCurrentIndex(self.cmp.completionModel().index(0, 0))  
   
        cr = self.cursorRect()  
        cr.setWidth(self.cmp.popup().sizeHintForColumn(0)  
                    + self.cmp.popup().verticalScrollBar().sizeHint().width())  
        self.cmp.complete(cr)  
   
class Completer(QCompleter):  
    def __init__(self,stringlist,parent=None):  
        super(Completer,self).__init__(parent)  
        self.stringlist=stringlist  
        self.setModel(QStringListModel())  
   
    def update(self,completionText):  
        filtered=self.stringlist.filter(completionText,Qt.CaseInsensitive)  
        self.model().setStringList(filtered)  
        self.popup().setCurrentIndex(self.model().index(0, 0))  
   
   
app=QApplication(sys.argv)         
li=QStringList()  
li<<'The'<<'that'<<'Red'<<'right'<<'what'  
cmp=Completer(li)  
window=QMainWindow()  
edit=TextEdit()  
edit.setCompleter(cmp)  
window.setCentralWidget(edit)  
window.show()  
app.exec_()  
