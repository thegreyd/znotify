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
        format_Query = cls.Generate_Query(query_Obj)
        pages = 1
        
        full_Results = list()
        for page_No in range(pages):
            full_Url = TorrentzEngine.Feed_Url(format_Query, page_No)
            req = urllib.request.Request(full_Url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            parsed_Results = MyParser.Parse_Page(response)
            full_Results.extend(parsed_Results)
        return tuple(full_Results)

    #used for demo purpose when internet connection not available
    @classmethod
    def Search_Static(cls, query_Obj):
        format_Query = cls.Generate_Query(query_Obj)
        pages = 1
        
        full_Results = list()
        for page_No in range(pages):
            static=open("static.xml","r")
            page_Xml_Obj=BeautifulSoup(static.read(),"xml")
            parsed_Results = MyParser.Parse_Page(response)
            full_Results.extend(parsed_Results)
        return tuple(full_Results)
    
    @classmethod
    def Generate_Query(cls, query_Obj):
        search_String = query_Obj.search_String
        categ = TorrentzEngine.categories_Keywords[query_Obj.category][0]
        query = "{} {}".format(search_String, categ)
        return urllib.parse.quote(query)