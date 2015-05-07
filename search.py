from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import urllib.request,urllib.parse
from bs4 import BeautifulSoup

headers={"Name":0,"Size":1,"Seeders":2,"Peers":3,"Date":4,"Category":5,"Download":6,"Description":7}

header_data=("Name","Size","Seeders","Peers","Date (yy/mm/dd tt)","Category","Download","Description")

trackers_list = ['udp://open.demonii.com:1337/announce',
                'udp://tracker.leechers-paradise.org:6969',
                'udp://exodus.desync.com:6969',
                'udp://tracker.coppersurfer.tk:6969',
                'udp://9.rarbg.com:2710/announce']

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

categories = ("Any","Anime","Application","Books","Games","Movies","Music","TV")

categories_keywords = { "Anime" : ("anime"),
                        "Application" : ("app","software"),
                        "Books" : ("book","comic"),
                        "Games" : ("game"),
                        "Movies" : ("movie",),
                        "Music" : ("music","audio"),
                        "TV" : ("tv","show")
                    }


class searchSortModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        QSortFilterProxyModel.__init__(self, parent)
    
    
    
class torrentz_Search():

    def __init__(self):
        self.trackers = '&' + '&'.join(urllib.parse.urlencode({'tr' : tracker}) for tracker in trackers_list)
        
    def search_now(self,search_query,categ):
        query=urllib.parse.quote(search_query)
        pages=1
        full_results=list()
        for page_no in range(pages):
            #"""
            full_url="http://torrentz.in/feed?q={}&p={}".format(query,page_no)
            req = urllib.request.Request(full_url,headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req)
            page_xml_obj=BeautifulSoup(response,"xml")
            """
            static=open("static.xml","r")
            page_xml_obj=BeautifulSoup(static.read(),"xml")
            #"""
            parsed_results = self.parse_page(page_xml_obj)
            filtered_results = self.filter_categories(parsed_results,categ)
            full_results.extend(filtered_results)
            

        return full_results

    """def filter_categories(self,results,categ):
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
"""
            
    
    def parse_page(self,page_obj):
        data_file = list()
        for it in page_obj.find_all("item"):
            title = str(it.title.string)
            desc_link = str(it.link.string)
            categ=str(it.category.string)
            
            pubDate = str(it.pubDate.string).split()
            year = pubDate[3]
            month = months[pubDate[2]]
            day = pubDate[1]
            day = "0" + day if int(day) < 10 else day
            time = pubDate[4]
            re_date = "{}/{}/{} {}".format(year,month,day,time)
            
            desc = str(it.description.string).split()
            size = "{} {}".format(desc[1],desc[2])
            seeds = int(desc[4].replace(",",""))
            peers = int(desc[6].replace(",",""))
            thash = desc[8]
            name = "&{}".format(urllib.parse.urlencode({'dn':title}))
            mag_link = "magnet:?xt=urn:btih:{}{}{}".format(thash,name,self.trackers)
            data_file.append((title,size,seeds,peers,re_date,categ,mag_link,desc_link))

        return data_file        