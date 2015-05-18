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

    @classmethod
    def Format_Size(cls, torrent_Obj):
        size_Mb = torrent_Obj.size_Mb
        GB = 1024
        TB = 1024 * GB

        if (size_Mb > TB): 
            size = "{:.2f}".format(size_Mb/TB)
            size_Unit = "TB"
        elif (size_Mb > GB):
            size = "{:.2f}".format(size_Mb/GB)
            size_Unit = "GB"
        else:
            size = "{}".format(size_Mb)
            size_Unit = "MB"
        
        return "{} {}".format(size,size_Unit)
    
    @classmethod
    def Format_Age(cls, torrent_Obj):
        time_Duration = TorrentzEngine.Calc_Age(torrent_Obj)
        seconds = time_Duration.total_seconds()

        minute = 60
        hour = 60 * minute
        day = 24 * hour
        week = 7 * day
        month = 30 * day
        year = 365 * day
        
        if (seconds > year):
            age = seconds//year
            age_Unit = "years"
        elif (seconds > month):
            age = seconds//month
            age_Unit = "months"
        elif (seconds > week):
            age = seconds//week
            age_Unit = "weeks"
        elif (seconds > day):
            age = seconds//day
            age_Unit = "days"
        elif (seconds > hour):
            age = seconds//hour
            age_Unit = "hours"
        elif (seconds > minute):
            age = seconds//minute
            age_Unit = "minutes"
        
        if (age == 1):
            age_Unit = age_Unit[:-1]
        
        return "{} {}".format(int(age), age_Unit)


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

