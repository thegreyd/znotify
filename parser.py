from bs4 import BeautifulSoup
from datetime import datetime
from torrent import Torrent

months={"Jan":1,
        "Feb":2,
        "Mar":3,
        "Apr":4,
        "May":5,
        "Jun":6,
        "Jul":7,
        "Aug":8,
        "Sep":9,
        "Oct":10,
        "Nov":11,
        "Dec":12
    }

class MyParser():
    
    @classmethod
    def Parse_Page(cls, request_Obj):
        
        bs_Obj=BeautifulSoup(request_Obj,"xml")
        torrents_List = list()
        
        for it in bs_Obj.find_all("item"):
            title = str(it.title.string)
            categ=str(it.category.string)
            
            pub_Date = str(it.pubDate.string).split()
            day = int(pub_Date[1])
            mon = months[pub_Date[2]]
            year = int(pub_Date[3])
            time = pub_Date[4].split(":")
            hours = int(time[0])
            minutes = int(time[1])
            seconds = int(time[2])

            date_Time_Obj = datetime(year, mon, day, hours, minutes, seconds)
            
            desc = str(it.description.string).split()
            size_Mb = int(desc[1])
            seeds = int(desc[4].replace(",",""))
            peers = int(desc[6].replace(",",""))
            thash = desc[8]
            
            a_Torrent = Torrent(thash=thash,title=title,date=date_Time_Obj,categ=categ,size_Mb=size_Mb,seeds=seeds,peers=peers)
            torrents_List.append(a_Torrent)

        return torrents_List        
