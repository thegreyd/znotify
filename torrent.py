from torrentz import TorrentzEngine

class Torrent():
    
    def __init__(self,thash,title,pub_Date,categ,size,seeds,peers):
        self.thash = thash
        self.title = title
        self.pub_Date = pub_Date
        self.categ = categ
        self.size = size
        self.seeds = seeds
        self.peers = peers
        self.desc_Link = TorrentzEngine.Desc_Link(thash)
        self.mag_Link = TorrentzEngine.Desc_Link(thash, title)