from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import urllib.request
from bs4 import BeautifulSoup
import torrent,query
from parser import MyParser

headers={"name":0,"age":1,"date":2,"size":3,"size_Mb":4,"seeds":5,"peers":6,"categ":7,"hash":8}

header_data=("Name","Age","Date","Size","SizeMB","Seeders","Peers","Category","Hash")

class searchSortModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        QSortFilterProxyModel.__init__(self, parent)

    def sort(self, column, order):
        if (column == headers["age"]):
            return QSortFilterProxyModel.sort(self, headers["date"], order)
        elif (column == headers["size"]):
            return QSortFilterProxyModel.sort(self, headers["size_Mb"], order)
        
        QSortFilterProxyModel.sort(self, column, order)
    
class TorrentzSearch():
    gen_adv = ""
    
    @classmethod
    def Search_Now(cls, query_Obj, limit = 100):
        print("searchingnow...")
        format_Query = cls.Generate_Query(query_Obj)
        pages = 1
        
        full_Results = list()
        for page_No in range(pages):
            full_Url = torrent.TorrentzEngine.Feed_Url(format_Query, page_No)
            req = urllib.request.Request(full_Url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            parsed_Results = MyParser.Parse_Page(response, limit = limit)
            full_Results.extend(parsed_Results)
        print("search results found {}".format(len(full_Results)))
        return tuple(full_Results)

    #used for demo purpose when internet connection not available
    @classmethod
    def Search_Static(cls, query_Obj):
        format_Query = cls.Generate_Query(query_Obj)
        pages = 1
        
        full_Results = list()
        for page_No in range(pages):
            static=open("static.xml","r")
            parsed_Results = MyParser.Parse_Page(static.read())
            full_Results.extend(parsed_Results)
        return tuple(full_Results)
    
    @classmethod
    def Generate_Query(cls, query_Obj):
        search_String = query_Obj.search_String
        categ = torrent.TorrentzEngine.categories_Keywords[query_Obj.category][0]
        min_Seeds = query_Obj.min_Seeds
        max_Age = query_Obj.max_Age
        max_Age_Unit = query_Obj.max_Age_Unit
        max_Size = query_Obj.max_Size
        max_Size_Unit = query_Obj.max_Size_Unit
        
        mature_filter,seed_filter, size_filter, age_filter = "","","",""

        if query_Obj.safe_Search and (search_String.split() or categ):
            mature_filter =  " ".join(torrent.TorrentzEngine.categories_Keywords["Adult"])

        if min_Seeds > 0:
            seed_filter = "seed > {}".format(min_Seeds)
        if max_Size > 0:
            size_filter = "size < {}{}".format(max_Size, max_Size_Unit)
        if max_Age > 0:
            age_filter = "added < {}{}".format(max_Age, max_Age_Unit)
        
        adv = [x for x in (seed_filter, size_filter, age_filter) if x!=""]
        TorrentzSearch.gen_adv = " ".join(adv) if adv else "None"

        l = [x for x in (search_String, categ, mature_filter, seed_filter, size_filter, age_filter) if x!=""]
        gen_query = " ".join(l)
        print(gen_query)
        return urllib.parse.quote(gen_query)