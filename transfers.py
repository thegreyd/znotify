from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

headers_transfers_keywords = ("Name", "Category", "Max.Age", "Min.Seeds" ,"Max.Size", "AddedOn","Status", "Action")

headers_transfers = {"name":0, 
                    "categ":1, 
                    "max_Age":2 ,
                    "min_Seeds":3, 
                    "max_Size":4,
                    "status":6, 
                    "action":7,
                    "added_On":5
                    }


headers_torrents = {"name":0,"age":1,"date":2,"size":3,"size_Mb":4,"seeds":5,"peers":6,"categ":7,"hash":8, "fid":9}

headers_torrents_keywords = ("Name","Age","Date","Size","SizeMB","Seeders","Peers","Category","Hash", "FilterId")