#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import search, torrent, mail, transfers, dialog, query

form_class=loadUiType("mainwindow.ui")[0]

class MyWindowClass(QMainWindow, form_class):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.Setup_Transfers_Ui()
        self.Setup_Search_Ui()
        self.Setup_Toolbar()
        
    def Setup_Toolbar(self):
        self.actionNew.triggered.connect(self.Create_Filter)


    def Setup_Transfers_Ui(self):
        #setting up transfer tab treeviews

        self.TransferListModel = QStandardItemModel(0,len(transfers.headers_transfers_keywords))
        self.TransferListModel.setHorizontalHeaderLabels(transfers.headers_transfers_keywords)

        self.transfer_Proxy_Model = search.searchSortModel(None)
        self.transfer_Proxy_Model.setDynamicSortFilter(True)
        self.transfer_Proxy_Model.setSourceModel(self.TransferListModel)
        
        self.filters_Browser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.filters_Browser.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.filters_Browser.setModel(self.transfer_Proxy_Model)
        self.filters_Browser.setRootIsDecorated(False)
        self.filters_Browser.setAllColumnsShowFocus(True)
        self.filters_Browser.setSortingEnabled(True)
        self.filters_Browser.setColumnWidth(0,400)

        #setting torrents list in transfers tab

        self.TorrentListModel = QStandardItemModel(0,len(transfers.headers_torrents_keywords))
        self.TorrentListModel.setHorizontalHeaderLabels(transfers.headers_torrents_keywords)

        self.torrent_Proxy_Model = search.searchSortModel(None)
        self.torrent_Proxy_Model.setDynamicSortFilter(True)
        self.torrent_Proxy_Model.setSourceModel(self.TorrentListModel)
        
        self.torrents_Browser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.torrents_Browser.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.torrents_Browser.setModel(self.torrent_Proxy_Model)
        self.torrents_Browser.setRootIsDecorated(False)
        self.torrents_Browser.setAllColumnsShowFocus(True)
        self.torrents_Browser.setSortingEnabled(True)
        self.torrents_Browser.setColumnWidth(0,400)


    def Setup_Search_Ui(self):
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
        
        self.resultsBrowser.hideColumn(search.headers["hash"])
        self.resultsBrowser.hideColumn(search.headers["size_Mb"])
        self.resultsBrowser.hideColumn(search.headers["date"])

        self.combo_searchcateg.addItems(torrent.TorrentzEngine.categories)
        
        self.search_bar.returnPressed.connect(self.Init_Search)
        self.search_bar.setFocus()

        self.btn_search.clicked.connect(self.Init_Search)
        self.btn_add_search_as_filter.clicked.connect(self.Create_Filter_From_Search)
        self.btn_download.clicked.connect(self.Open_Download)
        self.btn_description.clicked.connect(self.Open_Desc)


    def Create_Filter(self):
        filter_Dialog = dialog.FilterDialog()
        result = filter_Dialog.exec_()
        
        if result == 1:
            self.Add_Filter(FilterDialog.filter_Obj)
        
    def Create_Filter_From_Search(self):
        import copy
        filter_Obj = copy.copy(query.Filter(search.TorrentzSearch.query_Obj))
        print(filter_Obj.search_String)
        #self.Add_Filter(filter_Obj)

    def Add_Filter(self, filter_Obj):
        row=self.TransferListModel.rowCount()
        self.TransferListModel.insertRow(row)
        
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["name"]), filter_Obj.search_String)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["categ"]), filter_Obj.category)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["min_Age"]), filter_Obj.min_Age)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["min_Seeds"]), filter_Obj.min_Seeds)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["max_Size"]), filter_Obj.max_Size)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["status"]), query.Filter.statuses_keywords[filter_Obj.status])
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["action"]), query.Filter.actions_keywords[filter_Obj.action])
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["added_On"]), str(filter_Obj.date_Added))


    def Reset_List(self):
        row = self.SearchListModel.rowCount()
        if row > 0:
            self.SearchListModel.removeRows(0, row)
        
    def Init_Search(self):
        self.status_label.setText("Status: Searching... ")

        search_Text = self.search_bar.text()
        category = self.combo_searchcateg.currentText()

        search.TorrentzSearch.query_Obj.search_String = search_Text
        search.TorrentzSearch.query_Obj.category = category
        
        self.proxyModel.enable_Filter = search.TorrentzSearch.query_Obj.safe_Search

        self.Reset_List()
        results = search.TorrentzSearch.Search_Now()
        self.Show_Results(results)
        
        self.resultsBrowser.sortByColumn(search.headers["peers"], Qt.DescendingOrder)
        self.btn_description.setEnabled(True)
        self.btn_download.setEnabled(True)
        self.btn_add_search_as_filter.setEnabled(True)
        
        status = "Status: {} Results Found. ".format(self.proxyModel.rowCount())
        if self.proxyModel.rowCount() == 0:
            status = "Status: No Results Found. Please Check if you correctly typed the query."
        
        self.status_label.setText(status)
        self.resultsBrowser.scrollToTop()
        
    def Show_Results(self,results):
        for tor_Obj in results:
            row=self.SearchListModel.rowCount()
            self.SearchListModel.insertRow(row)
            
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["hash"]), tor_Obj.thash)
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["name"]), tor_Obj.title)
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["size_Mb"]), tor_Obj.size_Mb)
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["seeds"]), tor_Obj.seeds)
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["peers"]), tor_Obj.peers)
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["categ"]), tor_Obj.categ)
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["date"]), str(tor_Obj.date))
            
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["size"]), self.Format_Size(tor_Obj))
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["age"]), self.Format_Age(tor_Obj))
            
            
    def Format_Size(self,torrent_Obj):
        size_Mb = torrent_Obj.size_Mb
        GB = 1024
        TB = 1024 * GB

        if (size_Mb > TB): 
            size = "{:.2f}".format(size_Mb/TB)
            size_Unit = "TB"
        elif (size_Mb > GB):
            size = "{:.2f}".format(size_Mb/GB)
            size_Unit = "GB"
        else:
            size = "{}".format(size_Mb)
            size_Unit = "MB"
        
        return "{} {}".format(size,size_Unit)
    
    def Format_Age(self,torrent_Obj):
        time_Duration = torrent.TorrentzEngine.Calc_Age(torrent_Obj)
        seconds = time_Duration.total_seconds()

        minute = 60
        hour = 60 * minute
        day = 24 * hour
        week = 7 * day
        month = 30 * day
        year = 365 * day
        
        if (seconds > year):
            age = seconds//year
            age_Unit = "years"
        elif (seconds > month):
            age = seconds//month
            age_Unit = "months"
        elif (seconds > week):
            age = seconds//week
            age_Unit = "weeks"
        elif (seconds > day):
            age = seconds//day
            age_Unit = "days"
        elif (seconds > hour):
            age = seconds//hour
            age_Unit = "hours"
        elif (seconds > minute):
            age = seconds//minute
            age_Unit = "minutes"
        
        if (age == 1):
            age_Unit = age_Unit[:-1]
        
        return "{} {}".format(int(age), age_Unit)

    def Open_Download(self):
        indexes=set(i.row() for i in self.resultsBrowser.selectedIndexes())
        for i_row in indexes:
            title = self.proxyModel.data(self.proxyModel.index(i_row, search.headers["name"]))
            thash = self.proxyModel.data(self.proxyModel.index(i_row, search.headers["hash"]))
            link = torrent.TorrentzEngine.Magnet_Link(title, thash)
            QDesktopServices.openUrl(QUrl(link))

    def Open_Desc(self):
        indexes=set(i.row() for i in self.resultsBrowser.selectedIndexes())
        for i_row in indexes:
            thash = self.proxyModel.data(self.proxyModel.index(i_row, search.headers["hash"]))
            link = torrent.TorrentzEngine.Desc_Link(thash)
            QDesktopServices.openUrl(QUrl(link))


app = QApplication(sys.argv)
myWindow = MyWindowClass(None)
myWindow.show()
sys.exit(app.exec_())

def return_object():
    return myWindow