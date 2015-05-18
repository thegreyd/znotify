#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
        self.Setup_Toolbar()
        self.Setup_Transfers_Ui()
        self.Setup_Search_Ui()
        self.destroyed.connect(self.Save_Transfer_List)
        
        
    def Setup_Toolbar(self):
        self.actionNew.triggered.connect(self.Create_Filter)
        self.actionDelete.triggered.connect(self.Delete_Filters)
        self.actionStart.triggered.connect(self.Start_Filters)
        self.actionPause.triggered.connect(self.Pause_Filters)
        self.actionOptions.triggered.connect(self.Open_Options)
        self.actionStartAll.triggered.connect(self.Start_All_Filters)
        self.actionPauseAll.triggered.connect(self.Pause_All_Filters)
        self.actionExit.triggered.connect(self.close)
        self.actionEdit.triggered.connect(self.Edit_Filter)
        self.actionMarkComplete.triggered.connect(self.Mark_Complete_Filter)


    def Setup_Transfers_Ui(self):
        #setting up transfer tab filters_Browsers

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
        self.filters_Browser.setColumnWidth(transfers.headers_transfers["name"],300)
        self.filters_Browser.sortByColumn(transfers.headers_transfers["added_On"], Qt.AscendingOrder)

        self.Setup_Menu()
        self.filters_Browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.filters_Browser.customContextMenuRequested.connect(self.Open_Filter_Menu)
        
        self.Setup_Transfer_List()

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
        self.torrents_Browser.setColumnWidth(transfers.headers_torrents["name"],400)

        #setting different status views

        self.btn_viewall.clicked.connect(self.View_All_Filters)
        self.btn_viewactive.clicked.connect(self.View_Active_Filters)
        self.btn_viewpaused.clicked.connect(self.View_Paused_Filters)
        self.btn_viewcompleted.clicked.connect(self.View_Completed_Filters)

    def Setup_Menu(self):
        self.menu = QMenu()
        self.menu.addAction(self.actionEdit)
        self.menu.addAction(self.actionMarkComplete)

    def Open_Filter_Menu(self, position):
        indexes = set(i.row() for i in self.filters_Browser.selectedIndexes())
        if len(indexes) == 1:
            self.menu.exec_(self.filters_Browser.viewport().mapToGlobal(position))
    

    def View_X_Filters(self, x):
        self.transfer_Proxy_Model.setFilterFixedString(x)
        self.transfer_Proxy_Model.setFilterKeyColumn(transfers.headers_transfers["status"])
        
    def View_All_Filters(self):
        self.View_X_Filters("")
    
    def View_Active_Filters(self):
        self.View_X_Filters(query.Filter.statuses_keywords[query.Filter.statuses["active"]])

    def View_Paused_Filters(self):
        self.View_X_Filters(query.Filter.statuses_keywords[query.Filter.statuses["paused"]])

    def View_Completed_Filters(self):
        self.View_X_Filters(query.Filter.statuses_keywords[query.Filter.statuses["completed"]])
    
    def Setup_Search_Ui(self):
        #setting up search tab filters_Browser 
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
        self.resultsBrowser.sortByColumn(search.headers["peers"], Qt.DescendingOrder)
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


    def closeEvent(self, event):
        self.Save_Transfer_List()
        event.accept()

    def Create_Transfer_List(self):
        import pickle, collections
        with open("tb.pdict", "wb") as f:
            pickle.dump(collections.OrderedDict(), f)

    def Setup_Transfer_List(self):
        import pickle 
        with open("tb.pdict", "rb") as f:
            try:
                self.transfers_Dict = pickle.load(f)
            except:
                self.Create_Transfer_List()
                self.transfers_Dict = pickle.load(f)

        for filter_Obj in self.transfers_Dict.values():
            self.Add_Filter(filter_Obj)

    def Save_Transfer_List(self):
        import pickle
        with open("tb.pdict", "wb") as f:
            pickle.dump(self.transfers_Dict, f)

    def Create_Filter(self):
        filter_Obj = query.Filter()
        filter_Dialog = dialog.FilterDialog(filter_Obj)
        result = filter_Dialog.exec_()
        
        if result == 1:
            self.Add_Filter(filter_Dialog.filter_Obj)
        
    def Create_Filter_From_Search(self):
        filter_Obj = query.Filter(search.TorrentzSearch.query_Obj)
        self.Add_Filter(filter_Obj)

    def Add_Filter(self, filter_Obj):
        row=self.TransferListModel.rowCount()
        self.TransferListModel.insertRow(row)
        self.transfers_Dict[str(filter_Obj.date_Added)] = filter_Obj
        
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["name"]), filter_Obj.search_String)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["categ"]), filter_Obj.category)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["max_Age"]), query.Filter.Format_Age(filter_Obj))
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["min_Seeds"]), filter_Obj.min_Seeds)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["max_Size"]), query.Filter.Format_Size(filter_Obj))
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["status"]), query.Filter.statuses_keywords[filter_Obj.status])
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["action"]), query.Filter.actions_keywords[filter_Obj.action])
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["added_On"]), str(filter_Obj.date_Added))


    def Delete_Filters(self):
        indexes=sorted(list(set(i.row() for i in self.filters_Browser.selectedIndexes())), reverse = True)
        for i in indexes:
            f_Date = self.transfer_Proxy_Model.data(self.transfer_Proxy_Model.index(i, transfers.headers_transfers["added_On"]))
            print("i is ",i)
            self.TransferListModel.removeRow(i)
            del self.transfers_Dict[f_Date]


    def Set_Status(self, st, indexes):
        for i in indexes:
            f_Date = self.transfer_Proxy_Model.data(self.transfer_Proxy_Model.index(i, transfers.headers_transfers["added_On"]))
            f = self.transfers_Dict[f_Date]
            f.status = st
            self.TransferListModel.setData(self.TransferListModel.index(i, transfers.headers_transfers["status"]), query.Filter.statuses_keywords[f.status])
            

    def Start_Filters(self):
        indexes = set(i.row() for i in self.filters_Browser.selectedIndexes())
        self.Set_Status(query.Filter.statuses["active"], indexes)

    def Pause_Filters(self):
        indexes = set(i.row() for i in self.filters_Browser.selectedIndexes())
        self.Set_Status(query.Filter.statuses["paused"], indexes)

    def Start_All_Filters(self):
        indexes = range(0, self.TransferListModel.rowCount())
        self.Set_Status(query.Filter.statuses["active"], indexes)

    def Pause_All_Filters(self):
        indexes = range(0, self.TransferListModel.rowCount())
        self.Set_Status(query.Filter.statuses["paused"], indexes)

    def Mark_Complete_Filter(self):
        indexes = set(i.row() for i in self.filters_Browser.selectedIndexes())
        self.Set_Status(query.Filter.statuses["completed"], indexes)        

    def Open_Options(self):
        pass

    def Edit_Filter(self):
        pass

    def Reset_List(self, std_Item_Model):
        row = std_Item_Model.rowCount()
        if row > 0:
            std_Item_Model.removeRows(0, row)
        
    def Init_Search(self):
        self.status_label.setText("Status: Searching... ")

        search_Text = self.search_bar.text()
        category = self.combo_searchcateg.currentText()

        search.TorrentzSearch.query_Obj.search_String = search_Text
        search.TorrentzSearch.query_Obj.category = category
        
        self.proxyModel.enable_Age_Filter = search.TorrentzSearch.query_Obj.safe_Search

        self.Reset_List(self.SearchListModel)
        results = search.TorrentzSearch.Search_Now()
        self.Show_Results(results)
        
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
            
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["size"]), torrent.Torrent.Format_Size(tor_Obj))
            self.SearchListModel.setData(self.SearchListModel.index(row, search.headers["age"]), torrent.Torrent.Format_Age(tor_Obj))
            
            
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

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    sys.exit(app.exec_())