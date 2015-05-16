import urllib.parse

class Torrent():
    
    def __init__(self,thash,title,date,categ,size_Mb,seeds,peers):
        self.thash = thash
        self.title = title
        self.date = date
        self.categ = categ
        self.size_Mb = size_Mb
        self.seeds = seeds
        self.peers = int(peers) + int(seeds)


class TorrentzEngine():
    base_Url = "http://torrentz.in"
    base_Url_Alt = "http://torrentz.eu"

    trackers = """&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce
                &tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969
                &tr=udp%3A%2F%2Fexodus.desync.com%3A6969
                &tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969
                &tr=udp%3A%2F%2F9.rarbg.com%3A2710%2Fannounce"""

    categories = ("Any","Anime","Application","Books","Games","Movies","Music","TV")

    categories_Keywords = { "Anime" : ["anime"],
                        "Application" : ["app","software"],
                        "Books" : ["book","comic"],
                        "Games" : ["game"],
                        "Movies" : ["movie",],
                        "Music" : ["music","audio"],
                        "TV" : ["tv","show"],
                        "Adult" : ["xxx","porn"],
                        "Any" : [""]
                    }
    @classmethod
    def Feed_Url(cls, query, page=1):
        
        url = "{}/feed?q={}&p={}".format(cls.base_Url, query, page)
        return url
    
    @classmethod        
    def Magnet_Link(cls, title, thash):
        name = "&{}".format(urllib.parse.urlencode({'dn':title}))
        link = "magnet:?xt=urn:btih:{}{}{}".format(thash, name, cls.trackers)
        return link

    @classmethod
    def Desc_Link(cls, thash):
        link = "{}/{}".format(cls.base_Url, thash)
        return link

    @classmethod
    def Calc_Age(cls, tor_Obj):
        time_Duration = tor_Obj.date.utcnow() - tor_Obj.date
        return time_Duration

    @classmethod
    def Is_Safe(cls, categ_String):
        if categ_String:
            for i in cls.categories_Keywords["Adult"]:
                if i in categ_String:
                    return False
            return True
        return False

