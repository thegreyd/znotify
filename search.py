from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import urllib.request
from bs4 import BeautifulSoup
from torrent import Torrent, TorrentzEngine
from parser import MyParser

headers={"name":0,"age":1,"date":2,"size":3,"size_Mb":4,"seeds":5,"peers":6,"categ":7,"hash":8}

header_data=("Name","Age","Date","Size","SizeMB","Seeders","Peers","Category","Hash")

class searchSortModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
        self.enable_Filter = True

    def sort(self, column, order):
        if (column == headers["age"]):
            return QSortFilterProxyModel.sort(self, headers["date"], order)
        elif (column == headers["size"]):
            return QSortFilterProxyModel.sort(self, headers["size_Mb"], order)
        
        QSortFilterProxyModel.sort(self, column, order)

    def filterAcceptsRow(self, source_Row, source_Parent):
        if self.enable_Filter:
            index = self.sourceModel().index(source_Row, headers["categ"])
            categ = self.sourceModel().data(index)
            return TorrentzEngine.Is_Safe(categ)
        return True
        

    
class TorrentzSearch():

    @classmethod
    def Search_Now(cls,query_Obj):
        query = urllib.parse.quote(query_Obj.search_String)
        pages = 1
        
        full_results = list()
        for page_no in range(pages):
            full_url = TorrentzEngine.Feed_Url(query, page_no)
            req = urllib.request.Request(full_url,headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            parsed_results = MyParser.Parse_Page(response)
            full_results.extend(parsed_results)
        return tuple(full_results)

    #used for demo purpose when internet connection not available
    @classmethod
    def Search_Static(cls, query_Obj):
        query = urllib.parse.quote(query_Obj.search_String)
        pages = 1
        full_results = list()
        for page_no in range(pages):
            static=open("static.xml","r")
            page_xml_obj=BeautifulSoup(static.read(),"xml")
            parsed_results = MyParser.Parse_Page(response)
        full_results.extend(parsed_results)

    def Generate_Query(cls, query_Obj):
        pass