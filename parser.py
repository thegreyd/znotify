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
            year = int(pub_Date[3])
            nmon = months[pub_Date[2]]
            nday = int(pub_Date[1])
            
            month = "0" + str(nmon) if nmon < 10 else str(nmon)
            day = "0" + str(nday) if nday < 10 else str(nday)

            time = pub_Date[4]
            time_S = time.split(":")
            hours = int(time_S[0])
            minutes = int(time_S[1])
            seconds = int(time_S[2])

            re_Date = "{}/{}/{} {}".format(year,month,day,time)

            date_Time_Obj = datetime(year, nmon, nday, hours, minutes, seconds )
            time_Duration = str(date_Time_Obj.utcnow() - date_Time_Obj)

            desc = str(it.description.string).split()
            size = "{} {}".format(desc[1],desc[2])
            seeds = int(desc[4].replace(",",""))
            peers = int(desc[6].replace(",",""))
            thash = desc[8]
            
            a_Torrent = Torrent(thash=thash,title=title,pub_Date=re_Date,categ=categ,size=size,seeds=seeds,peers=peers,age=time_Duration)
            torrents_List.append(a_Torrent)

        return torrents_List        
