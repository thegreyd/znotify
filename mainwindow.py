#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from query import Query
import search, torrent
from subprocess import call

form_class=loadUiType("mainwindow.ui")[0]

class MyWindowClass(QMainWindow, form_class):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        #setting up search tab treeview 
        self.SearchListModel = QStandardItemModel(0,len(search.header_data))
        self.SearchListModel.setHorizontalHeaderLabels(search.header_data)
        
        self.proxyModel = search.searchSortModel(None)
        self.proxyModel.setDynamicSortFilter(True)
        self.proxyModel.setSourceModel(self.SearchListModel)
        
        self.resultsBrowser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.resultsBrowser.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.resultsBrowser.setModel(self.proxyModel)
        self.resultsBrowser.setRootIsDecorated(False)
        self.resultsBrowser.setAllColumnsShowFocus(True)
        self.resultsBrowser.setSortingEnabled(True)
        self.resultsBrowser.setColumnWidth(search.headers["name"],400)
        #self.resultsBrowser.hideColumn(search.headers["categ"])

        self.combo_searchcateg.addItems(search.categories)
        self.btn_search.clicked.connect(self.Init_Search)
        self.search_bar.returnPressed.connect(self.Init_Search)
        self.search_bar.setFocus()
        

    def Reset_List(self):
        row = self.SearchListModel.rowCount()
        if row > 0:
            self.SearchListModel.removeRows(0, row)
        
    def Init_Search(self):
        search_Text = self.search_bar.text()

        if search_Text :
            self.status_label.setText("Status: Searching... ")
            
            category = self.combo_searchcateg.currentText()
            query_Obj = Query(search_Text, category)
            
            self.Reset_List()

            search_Obj = search.TorrentzSearch()
            results = search_Obj.search_now(query_Obj)
            self.Show_Results(results)
            self.resultsBrowser.scrollToTop()
        else:
            pass
    
    def Show_Results(self,results):
        if results :
            for tor_Obj in results:
                row=self.SearchListModel.rowCount()
                self.SearchListModel.insertRow(row)
                
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["hash"]), tor_Obj.thash)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["name"]), tor_Obj.title)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["size_Mb"]), tor_Obj.size_Mb)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["seeds"]), tor_Obj.seeds)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["peers"]), tor_Obj.peers)
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["categ"]), tor_Obj.categ)
                
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["size"]), self.Format_Size(tor_Obj))
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["age"]), self.Format_Age(tor_Obj))
                self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["date"]), self.Format_Date(tor_Obj))
                
            self.resultsBrowser.sortByColumn(search.headers["peers"], Qt.DescendingOrder)
            self.btn_description.setEnabled(True)
            self.btn_download.setEnabled(True)
            self.btn_download.clicked.connect(self.Open_Download)
            self.btn_description.clicked.connect(self.Open_Desc)
            status = "Status: {} Results Found. ".format(self.SearchListModel.rowCount())
        else :
            status = "Status: No Results Found. Please Check if you correctly typed the query."
        
        self.status_label.setText(status)
            
    def Format_Date(self,torrent_Obj):
        date_Obj = torrent_Obj.date
        return str(date_Obj)
        
    def Format_Size(self,torrent_Obj):
        
        return ""
    
    def Format_Age(self,torrent_Obj):
        time_Duration = torrent.TorrentzEngine.Calc_Age(torrent_Obj)
        return str(time_Duration)

    def Open_Download(self):
        indexes=set(i.row() for i in self.resultsBrowser.selectedIndexes())
        for i_row in indexes:
            title = self.proxyModel.data(self.proxyModel.index(i_row, search.headers["name"]))
            thash = self.proxyModel.data(self.proxyModel.index(i_row, search.headers["hash"]))
            link = torrent.TorrentzEngine.Magnet_Link(title, thash)
            call(["xdg-open",link])
            
    
    def Open_Desc(self):
        indexes=set(i.row() for i in self.resultsBrowser.selectedIndexes())
        for i_row in indexes:
            thash = self.proxyModel.data(self.proxyModel.index(i_row, search.headers["hash"]))
            link = torrent.TorrentzEngine.Desc_Link(thash)
            QDesktopServices.openUrl(QUrl(link))

if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    sys.exit(app.exec_())