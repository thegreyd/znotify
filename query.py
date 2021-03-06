class Query():
    size_units_keywords = ("MB","GB")
    size_units = {"mb": 0, "gb": 1,"m":0,"g":1}
    size_search_units_keywords = ("m","g")
    

    age_units_keywords = ("days","months","years")
    age_units = {"days":0,"months":1,"years":2,"d":0,"m":1,"y":2}
    age_search_units_keywords = ("d","m","y")

    def __init__(self):
        self.search_String = None
        self.category = "Any"
        self.safe_Search = True
        self.min_Seeds = 0
        self.max_Age = 0
        self.max_Age_Unit = Query.age_search_units_keywords[Query.age_units["days"]]
        self.max_Size = 0
        self.max_Size_Unit = Query.size_search_units_keywords[Query.size_units["mb"]]
        
class Filter(Query):
    
    actions_keywords = ("Notify", "Ignore" , "NotifyAndDownload" , "Download")
    actions = { "notify" : 0,
                "ignore" : 1,
                "notifyanddownload" : 2,
                "download" : 3
    }

    
    statuses_keywords = ("Active", "Paused", "Completed")
    statuses = { "active" :0,
              "paused" : 1,
              "completed" : 2
    }

    def __init__(self, query_Obj = None):
        import datetime
        Query.__init__(self)
        
        self.status = Filter.statuses["active"]
        self.rate_Minute = 1.0
        self.action = Filter.actions["notify"]
        self.email_Notify = True
        self.date_Added = datetime.datetime.now()
        self.torrents_Found = 0

        if query_Obj != None:
            self.search_String = query_Obj.search_String
            self.category = query_Obj.category
            self.safe_Search = query_Obj.safe_Search
            self.min_Seeds = query_Obj.min_Seeds
            self.max_Age = query_Obj.max_Age
            self.max_Age_Unit = query_Obj.max_Age_Unit
            self.max_Size = query_Obj.max_Size
            self.max_Size_Unit = query_Obj.max_Size_Unit

    @classmethod
    def Format_Size(cls, f):
        return "{} {}".format(f.max_Size, Query.size_units_keywords[Query.size_units[f.max_Size_Unit]]) 

    @classmethod
    def Format_Age(cls, f):
        return "{} {}".format(f.max_Age, Query.age_units_keywords[Query.age_units[f.max_Age_Unit]])