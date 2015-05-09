from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import urllib.request
from bs4 import BeautifulSoup
from torrent import Torrent, TorrentzEngine
from parser import MyParser

headers={"name":0,"age":1,"date":2,"size":3,"size_Mb":4,"seeds":5,"peers":6,"categ":7,"hash":8}

header_data=("Name","Age","Date","Size","SizeMB","Seeders","Peers","Category","Hash")




categories = ("Any","Anime","Application","Books","Games","Movies","Music","TV")

categories_keywords = { "Anime" : ("anime"),
                        "Application" : ("app","software"),
                        "Books" : ("book","comic"),
                        "Games" : ("game"),
                        "Movies" : ("movie",),
                        "Music" : ("music","audio"),
                        "TV" : ("tv","show"),
                        "Adult" : ("xxx","porn")
                    }


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

    def __init__(self):
        pass
        
    def search_now(self,query_Obj):
        query = urllib.parse.quote(query_Obj.search_String)
        pages = 1
        
        full_results = list()
        for page_no in range(pages):
            #"""
            full_url = TorrentzEngine.Feed_Url(query, page_no)
            
            req = urllib.request.Request(full_url,headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            
            """
            static=open("static.xml","r")
            page_xml_obj=BeautifulSoup(static.read(),"xml")
            #"""
            
            parsed_results = MyParser.Parse_Page(response)
            filtered_results = parsed_results
            #filtered_results = self.filter_categories(parsed_results,categ)
            full_results.extend(filtered_results)
            
        return tuple(full_results)

    def filter_categories(self,results,categ):
        if categ == "Any" : 
            return results
        else:
            new_results = list()
            index=headers["Category"]
            for i in results : 
                cat=i[index]
                for keyword in categories_keywords[categ] : 
                    if keyword in cat :
                        new_results.append(i)
                        break
            return new_results
