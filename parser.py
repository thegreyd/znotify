from bs4 import BeautifulSoup
from torrent import Torrent

months={"Jan":"01",
        "Feb":"02",
        "Mar":"03",
        "Apr":"04",
        "May":"05",
        "Jun":"06",
        "Jul":"07",
        "Aug":"08",
        "Sep":"09",
        "Oct":"10",
        "Nov":"11",
        "Dec":"12"
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
            year = pub_Date[3]
            month = months[pub_Date[2]]
            day = pub_Date[1]
            day = "0" + day if int(day) < 10 else day
            time = pub_Date[4]
            re_Date = "{}/{}/{} {}".format(year,month,day,time)
            
            desc = str(it.description.string).split()
            size = "{} {}".format(desc[1],desc[2])
            seeds = int(desc[4].replace(",",""))
            peers = int(desc[6].replace(",",""))
            thash = desc[8]
            
            a_Torrent = Torrent(thash,title,re_Date,categ,size,seeds,peers)
            torrents_List.append(a_Torrent)

        return torrents_List        
