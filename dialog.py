from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import torrent, query

filter_class=loadUiType("create_filter_dialog.ui")[0]
options_class=loadUiType("options.ui")[0]
advancedsearch_class=loadUiType("advancedsearch.ui")[0]

class FilterDialog(QDialog, filter_class):
    
    def __init__(self, filter_Obj, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.filter_Obj = filter_Obj
        self.combo_sizeul.addItems(query.Query.size_units_keywords)
        self.combo_ageunit.addItems(query.Query.age_units_keywords)
        self.combo_categ.addItems(torrent.TorrentzEngine.categories)

    def accept(self):
        
        self.filter_Obj.search_String = self.keywords_bar.text()
        self.filter_Obj.category = self.combo_categ.currentText()
        
        self.filter_Obj.min_Seeds = self.spin_seeds.value()
        self.filter_Obj.max_Age = self.spin_age.value()
        self.filter_Obj.max_Size = self.spin_sizeul.value()
        self.filter_Obj.max_Age_Unit = query.Query.age_search_units_keywords[self.combo_ageunit.currentIndex()]
        self.filter_Obj.max_Size_Unit = query.Query.size_search_units_keywords[self.combo_sizeul.currentIndex()]
        
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

class EditFilterDialog():
    pass

class AdvancedSearchDialog(QDialog, advancedsearch_class):
    def __init__(self, query_Obj, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.query_Obj = query_Obj
        self.combo_age_unit.addItems(query.Query.age_units_keywords)
        self.combo_size_unit.addItems(query.Query.size_units_keywords)
        
        state = 2 if query_Obj.safe_Search else 0
        
        self.check_safe_search.setCheckState(state)
        self.spin_min_seeds.setValue(query_Obj.min_Seeds)
        self.spin_max_age.setValue(query_Obj.max_Age)
        self.spin_max_size.setValue(query_Obj.max_Size)
        self.combo_age_unit.setCurrentIndex(query.Query.age_units[query_Obj.max_Age_Unit])
        self.combo_size_unit.setCurrentIndex(query.Query.size_units[query_Obj.max_Size_Unit])

    def accept(self):
        self.query_Obj.safe_Search = self.check_safe_search.isChecked()
        self.query_Obj.min_Seeds = self.spin_min_seeds.value()
        self.query_Obj.max_Age = self.spin_max_age.value()
        self.query_Obj.max_Size = self.spin_max_size.value()
        self.query_Obj.max_Age_Unit = query.Query.age_search_units_keywords[self.combo_age_unit.currentIndex()]
        self.query_Obj.max_Size_Unit = query.Query.size_search_units_keywords[self.combo_size_unit.currentIndex()]
        QDialog.accept(self)



class OptionsDialog(QDialog, options_class):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setupUi(self)