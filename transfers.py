from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

headers_transfers_keywords = ("Name", "Category","TorrentsFound","Max.Age", "Min.Seeds" ,"Max.Size","Status", "Action","AddedOn")

headers_transfers = {"name":0, 
                    "categ":1, 
                    "max_Age":3 ,
                    "min_Seeds":4, 
                    "max_Size":5,
                    "status":6, 
                    "action":7,
                    "added_On":8,
                    "torrents_Found":2
                    }


headers_torrents = {"name":0,"age":1,"date":2,"size":3,"size_Mb":4,"seeds":5,"peers":6,"categ":7,"hash":8, "fid":9}

headers_torrents_keywords = ("Name","Age","Date","Size","SizeMB","Seeders","Peers","Category","Hash", "FilterId")