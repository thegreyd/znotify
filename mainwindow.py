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
        self.Setup_Tray()
        self.Setup_Toolbar()
        self.Setup_Transfers_Ui()
        self.Setup_Search_Ui()
        self.Setup_Data()
        self.destroyed.connect(self.Save_Data)
        
    def Save_Data(self):    
        self.Save_Transfer_List()
        self.Save_Torrent_List()
        self.Stats_List()

    def Setup_Data(self):
        self.Setup_Transfer_List()
        self.Setup_Torrent_List()
        self.Stats_List()

    def Setup_Tray(self):
        self.trayMenu = QMenu()
        self.trayMenu.addAction(self.actionExit)

        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(QIcon("/home/sid/qbittorrent.png"))
        self.trayIcon.setContextMenu(self.trayMenu)

        self.trayIcon.show()
        
    def Notify(self):
        self.trayIcon.showMessage("Torrent Notifier", "Matching Torrents found for Filter!")
        #mail.Mail.Send_Email()

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
        self.actionDownload.triggered.connect(self.Open_Download_Transfer)
        self.actionDescription.triggered.connect(self.Open_Desc_Transfer)


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

        self.Setup_Filter_Menu()
        self.filters_Browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.filters_Browser.customContextMenuRequested.connect(self.Open_Filter_Menu)

        self.filter_select = self.filters_Browser.selectionModel()
        self.filter_select.selectionChanged.connect(self.Change_Torrent_View)
        
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
        self.torrents_Browser.sortByColumn(transfers.headers_torrents["peers"], Qt.DescendingOrder)
        self.torrents_Browser.setColumnWidth(transfers.headers_torrents["name"],400)

        self.torrents_Browser.hideColumn(transfers.headers_torrents["hash"])
        self.torrents_Browser.hideColumn(transfers.headers_torrents["size_Mb"])
        self.torrents_Browser.hideColumn(transfers.headers_torrents["date"])
        self.torrents_Browser.hideColumn(transfers.headers_torrents["fid"])

        self.Setup_Torrent_Menu()
        self.torrents_Browser.setContextMenuPolicy(Qt.CustomContextMenu)
        self.torrents_Browser.customContextMenuRequested.connect(self.Open_Torrent_Menu)

        self.btn_viewall.clicked.connect(self.View_All_Filters)
        self.btn_viewactive.clicked.connect(self.View_Active_Filters)
        self.btn_viewpaused.clicked.connect(self.View_Paused_Filters)
        self.btn_viewcompleted.clicked.connect(self.View_Completed_Filters)

    
    
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

        self.query_Obj = query.Query()

        self.btn_search.clicked.connect(self.Init_Search)
        self.btn_advancedsearch.clicked.connect(self.Advanced_Search)
        self.btn_add_search_as_filter.clicked.connect(self.Create_Filter_From_Search)
        self.btn_download.clicked.connect(self.Open_Download_Search)
        self.btn_description.clicked.connect(self.Open_Desc_Search)


    def Setup_Filter_Menu(self):
        self.filter_Menu = QMenu()
        self.filter_Menu.addAction(self.actionEdit)
        self.filter_Menu.addAction(self.actionMarkComplete)
        self.filter_Menu.addAction(self.actionStart)
        self.filter_Menu.addAction(self.actionPause)
        self.filter_Menu.addAction(self.actionDelete)

    def Open_Filter_Menu(self, position):
        indexes = set(i.row() for i in self.filters_Browser.selectedIndexes())
        if len(indexes) > 1:
            self.actionEdit.setVisible(False)
        self.filter_Menu.exec_(self.filters_Browser.viewport().mapToGlobal(position))

    def Setup_Torrent_Menu(self):
        self.torrent_Menu = QMenu()
        self.torrent_Menu.addAction(self.actionDownload)
        self.torrent_Menu.addAction(self.actionDescription)

    def Open_Torrent_Menu(self, position):
        self.torrent_Menu.exec_(self.torrents_Browser.viewport().mapToGlobal(position))
    

    def Change_Torrent_View(self):
        indexes = set(i.row() for i in self.filter_select.selectedRows())
        list_of_Id = []
        
        if not indexes:
            row = self.transfer_Proxy_Model.rowCount()
            indexes = range(row)
        
        for k in indexes:
            f_Id = self.transfer_Proxy_Model.data(self.transfer_Proxy_Model.index(k, transfers.headers_transfers["added_On"]))
            list_of_Id.append(f_Id)
        
        r = "hakunaMatata" if not indexes else "|".join(list_of_Id)

        #r = ".*" if not indexes else "|".join(list_of_Id)

        self.torrent_Proxy_Model.setFilterRegExp(QRegExp(r))            
        self.torrent_Proxy_Model.setFilterKeyColumn(transfers.headers_torrents["fid"])


    def View_X_Filters(self, x):
        self.transfer_Proxy_Model.setFilterFixedString(x)
        self.transfer_Proxy_Model.setFilterKeyColumn(transfers.headers_transfers["status"])
        self.Change_Torrent_View()
        
    def View_All_Filters(self):
        self.View_X_Filters("")
    
    def View_Active_Filters(self):
        self.View_X_Filters(query.Filter.statuses_keywords[query.Filter.statuses["active"]])

    def View_Paused_Filters(self):
        self.View_X_Filters(query.Filter.statuses_keywords[query.Filter.statuses["paused"]])

    def View_Completed_Filters(self):
        self.View_X_Filters(query.Filter.statuses_keywords[query.Filter.statuses["completed"]])

    def closeEvent(self, event):
        self.Save_Data()
        event.accept()

    def Create_Transfer_List(self):
        print("creating transfer list..")
        
        import pickle, collections
        with open("tb.pdict", "wb") as f:
            pickle.dump(collections.OrderedDict(), f)

    def Setup_Transfer_List(self):
        print("setting up transfer list..")
        
        import pickle 
        try:
            with open("tb.pdict", "rb") as f:
                self.transfers_Dict = pickle.load(f)
        except:
            self.Create_Transfer_List()
            self.Setup_Transfer_List()
        
        for filter_Obj in self.transfers_Dict.values():
            self.Add_Filter(filter_Obj)

    def Save_Transfer_List(self):
        print("saving transfer list..")
        
        import pickle
        with open("tb.pdict", "wb") as f:
            pickle.dump(self.transfers_Dict, f)

    
    def Setup_Torrent_List(self):
        print("setting up torrent list..")
        
        import pickle 
        try:
            with open("tbresults.pdict", "rb") as f:
                self.torrents_Dict = pickle.load(f)
        except:
            self.Create_Torrent_List()
            self.Setup_Torrent_List()
        
        for fid,results in self.torrents_Dict.items():
            self.Show_Filter_Results(fid, results)

    def Refresh_Torrent_List(self):
        print("refreshing torrent list...")
        
        self.Reset_List(self.torrent_Proxy_Model)
        for fid,results in self.torrents_Dict.items():
            self.Show_Filter_Results(fid, results)

    def Save_Torrent_List(self):
        print("saving torrent list..")
        
        import pickle
        with open("tbresults.pdict", "wb") as f:
            pickle.dump(self.torrents_Dict, f)

    def Create_Torrent_List(self):
        print("creating torrent list..")
        
        import pickle, collections
        with open("tbresults.pdict", "wb") as f:
            pickle.dump(collections.OrderedDict(), f)

    def Stats_Torrent_List(self):
        print("stats torrent list - no.of.filters",len(self.torrents_Dict))
        for fid,results in self.torrents_Dict.items():
            print("fid: {} no.of.torrents {}".format(fid,len(results)))

    def Stats_Transfer_List(self):
        print("stats transfer list - no.of.filters",len(self.transfers_Dict))

    def Stats_List(self):
        self.Stats_Transfer_List()
        self.Stats_Torrent_List()
        
    def Create_Filter(self):
        print("creating filter..")

        filter_Obj = query.Filter()
        filter_Dialog = dialog.FilterDialog(filter_Obj)
        result = filter_Dialog.exec_()
        
        if result == 1:
            self.Add_Filter(filter_Dialog.filter_Obj)
            self.Init_Filter_Search(filter_Obj)
            self.Refresh_Torrent_List()
            
            row = self.TransferListModel.rowCount()
            #self.Change_Torrent_View()
            
            
    def Create_Filter_From_Search(self):
        print("creating filter from search query..")

        filter_Obj = query.Filter(self.query_Obj)
        self.Add_Filter(filter_Obj)
        self.Init_Filter_Search(filter_Obj)
        self.Refresh_Torrent_List()
        

    def Add_Filter(self,filter_Obj):
        self.transfers_Dict[str(filter_Obj.date_Added)] = filter_Obj
        self.Show_Filter(filter_Obj)
        #self.Init_Filter_Search(filter_Obj)

    def Show_Filter(self, filter_Obj):
        row=self.TransferListModel.rowCount()
        self.TransferListModel.insertRow(row)
        
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["name"]), filter_Obj.search_String)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["categ"]), filter_Obj.category)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["max_Age"]), query.Filter.Format_Age(filter_Obj))
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["min_Seeds"]), filter_Obj.min_Seeds)
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["max_Size"]), query.Filter.Format_Size(filter_Obj))
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["status"]), query.Filter.statuses_keywords[filter_Obj.status])
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["action"]), query.Filter.actions_keywords[filter_Obj.action])
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["added_On"]), str(filter_Obj.date_Added))


    def Delete_Filters(self):
        print("deleting filters..")

        indexes=sorted(list(set(i.row() for i in self.filters_Browser.selectedIndexes())), reverse = True)
        for i in indexes:
            f_Date = self.transfer_Proxy_Model.data(self.transfer_Proxy_Model.index(i, transfers.headers_transfers["added_On"]))
            self.TransferListModel.removeRow(i)
            del self.transfers_Dict[f_Date]
            del self.torrents_Dict[f_Date]
        
            l=0
            for j in range(0, self.TorrentListModel.rowCount()):
                if self.TorrentListModel.data(self.TorrentListModel.index(j-l, transfers.headers_torrents["fid"])) == f_Date:
                    self.TorrentListModel.removeRow(j-l)
                    l+=1
        
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
        options_Dialog = dialog.OptionsDialog()
        result = options_Dialog.exec_()

    def Edit_Filter(self):
        pass

    def Advanced_Search(self):
        as_Dialog = dialog.AdvancedSearchDialog(self.query_Obj)
        result = as_Dialog.exec_()        

    def Reset_List(self, model):
        print("resetting list..")

        row = model.rowCount()
        if row > 0:
            model.removeRows(0, row)
        
    def Init_Filter_Search(self, filter_Obj):
        print("Initialising Filter Search...")

        results = search.TorrentzSearch.Search_Now(filter_Obj, limit = 10)
        filter_Obj.torrents_Found = len(results)
        self.torrents_Dict[str(filter_Obj.date_Added)] = results
        self.Show_Filter_Results(filter_Obj.date_Added, results)

    def Init_Search(self):
        print("Initialising Search...")
        self.status_label.setText("Status: Searching... ")

        search_Text = self.search_bar.text()
        category = self.combo_searchcateg.currentText()
        self.query_Obj.search_String = search_Text
        self.query_Obj.category = category
        self.Reset_List(self.SearchListModel)
        
        results = search.TorrentzSearch.Search_Now(self.query_Obj)
        self.Show_Search_Results(results)
        
        self.btn_description.setEnabled(True)
        self.btn_download.setEnabled(True)
        self.btn_add_search_as_filter.setEnabled(True)
        
        status = "Status: "
        r = self.proxyModel.rowCount()
        if r == 0:
            status += "No Results Found. Check your query for errors."
        elif r == 100:
            status += "Top 100 Results."
        else:
            status += "{} Results.".format(r)
        
        self.status_label.setText(status)
        self.advanced_label.setText("Advanced: {}".format(search.TorrentzSearch.gen_adv))
        self.resultsBrowser.scrollToTop()
        
    def Show_Result(self, model, tor_Obj, headers):
        row = model.rowCount()
        model.insertRow(row)
        model.setData(model.index(row, headers["hash"]), tor_Obj.thash)
        model.setData(model.index(row, headers["name"]), tor_Obj.title)
        model.setData(model.index(row, headers["size_Mb"]), tor_Obj.size_Mb)
        model.setData(model.index(row, headers["seeds"]), tor_Obj.seeds)
        model.setData(model.index(row, headers["peers"]), tor_Obj.peers)
        model.setData(model.index(row, headers["categ"]), tor_Obj.categ)
        model.setData(model.index(row, headers["date"]), str(tor_Obj.date))
        model.setData(model.index(row, headers["size"]), torrent.Torrent.Format_Size(tor_Obj))
        model.setData(model.index(row, headers["age"]), torrent.Torrent.Format_Age(tor_Obj))

    def Show_Search_Results(self, results):
        print("displaying search results...")

        for tor_Obj in results:
            self.Show_Result(self.SearchListModel, tor_Obj, search.headers)
            
            
    def Show_Filter_Results(self, fid, results):
        
        row = self.TransferListModel.rowCount() - 1
        self.TransferListModel.setData(self.TransferListModel.index(row, transfers.headers_transfers["torrents_Found"]), len(results))

        for tor_Obj in results:
            self.Show_Result(self.TorrentListModel, tor_Obj, transfers.headers_torrents)
            row = self.TorrentListModel.rowCount() - 1
            self.TorrentListModel.setData(self.TorrentListModel.index(row, transfers.headers_torrents["fid"]), fid)
            
            
            
    def Open_Download(self, tv):
        print("redirecting torrent for download...")

        indexes=set(i.row() for i in tv.selectedIndexes())
        for i_row in indexes:
            title = tv.model().data(tv.model().index(i_row, search.headers["name"]))
            thash = tv.model().data(tv.model().index(i_row, search.headers["hash"]))
            link = torrent.TorrentzEngine.Magnet_Link(title, thash)
            QDesktopServices.openUrl(QUrl(link))

    def Open_Desc(self, tv):
        print("opening description...")

        indexes=set(i.row() for i in tv.selectedIndexes())
        for i_row in indexes:
            thash = tv.model().data(tv.model().index(i_row, search.headers["hash"]))
            link = torrent.TorrentzEngine.Desc_Link(thash)
            QDesktopServices.openUrl(QUrl(link))

    def Open_Download_Transfer(self):
        self.Open_Download(self.torrents_Browser)

    def Open_Desc_Transfer(self):
        self.Open_Desc(self.torrents_Browser)        

    def Open_Download_Search(self):
        self.Open_Download(self.resultsBrowser)

    def Open_Desc_Search(self):
        self.Open_Desc(self.resultsBrowser)        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    myWindow = MyWindowClass(None)
    myWindow.show()
    sys.exit(app.exec_())