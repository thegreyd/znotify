from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import torrent, query

form_class=loadUiType("create_filter_dialog.ui")[0]

class FilterDialog(QDialog, form_class):
    filter_Obj = query.Filter()

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.combo_sizeul.addItems(query.Query.size_units_keywords)
        self.combo_ageunit.addItems(query.Query.age_units_keywords)
        self.combo_categ.addItems(torrent.TorrentzEngine.categories)

    def accept(self):
        
        self.filter_Obj.search_String = self.keywords_bar.text()
        self.filter_Obj.category = self.combo_categ.currentText()
        
        self.filter_Obj.min_Seeds = self.spin_seeds.value()
        self.filter_Obj.min_Age = self.spin_age.value()
        self.filter_Obj.min_Age_Unit = self.combo_ageunit.currentText()
        self.filter_Obj.max_Size = self.spin_sizeul.value()
        self.filter_Obj.max_Size_Unit = self.combo_sizeul.currentText()
        
        self.filter_Obj.rate_Minute = self.spin_rate.value()
        
        self.filter_Obj.safe_Search = self.check_safesearch.isChecked()
        self.filter_Obj.email_Notify = self.check_email.isChecked()

        if self.radio_notify.isChecked():
            self.filter_Obj.action = query.Filter.actions["notify"]
        elif self.radio_ignore.isChecked():
            self.filter_Obj.action = query.Filter.actions["ignore"]
        elif self.radio_notifyanddownload.isChecked():
            self.filter_Obj.action = query.Filter.actions["notifyanddownload"]
        elif self.radio_download.isChecked():
            self.filter_Obj.action = query.Filter.actions["download"]

        QDialog.accept(self)