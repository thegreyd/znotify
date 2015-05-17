from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

headers_transfers_keywords = ("Name", "Category", "Min.Age", "Min.Seeds" ,"Max.Size", "AddedOn","Status", "Action")

headers_transfers = {"name":0, 
                    "categ":1, 
                    "min_Age":2 ,
                    "min_Seeds":3, 
                    "max_Size":4,
                    "status":6, 
                    "action":7,
                    "added_On":5
                    }



headers_torrents_keywords = ("Name", "Category","Age","Size","Seeders","Peers")

headers_torrents = {"name":0, 
                    "size":3, 
                    "seeders":4, 
                    "peers":5, 
                    "age":2, 
                    "categ":1
                    }
    