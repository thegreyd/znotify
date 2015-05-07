import urllib.parse

class Torrent():
    def __init__(self,thash,title,age,pub_Date,categ,size,seeds,peers):
        self.thash = thash
        self.title = title
        self.pub_Date = pub_Date
        self.categ = categ
        self.size = size
        self.seeds = seeds
        self.peers = int(peers) + int(seeds)
        self.age = age
        self.desc_Link = TorrentzEngine.Desc_Link(thash)
        self.mag_Link = TorrentzEngine.Magnet_Link(thash, title)

class TorrentzEngine():
    base_Url = "http://torrentz.in"
    base_Url_Alt = "http://torrentz.eu"

    trackers = """&tr=udp%3A%2F%2Fopen.demonii.com%3A1337%2Fannounce
                &tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969
                &tr=udp%3A%2F%2Fexodus.desync.com%3A6969
                &tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969
                &tr=udp%3A%2F%2F9.rarbg.com%3A2710%2Fannounce"""

    categories = ("Any","Anime","Application","Books","Games","Movies","Music","TV")

    categories_Keywords = { "Anime" : ("anime"),
                        "Application" : ("app","software"),
                        "Books" : ("book","comic"),
                        "Games" : ("game"),
                        "Movies" : ("movie",),
                        "Music" : ("music","audio"),
                        "TV" : ("tv","show")
                    }
    @classmethod
    def Feed_Url(cls, query, page=1):
        url = "{}/feed?q={}&p={}".format(cls.base_Url, query, page)
        return url
    
    @classmethod        
    def Magnet_Link(cls, thash, title):
        name = "&{}".format(urllib.parse.urlencode({'dn':title}))
        link = "magnet:?xt=urn:btih:{}{}{}".format(thash, name, cls.trackers)
        return link

    @classmethod
    def Desc_Link(cls, thash):
        link = "{}/{}".format(cls.base_Url, thash)
        return link


