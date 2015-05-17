class Query():
    size_units_keywords = ("MB","GB")
    size_units = { "mb" : 0,
                   "gb" : 1
    }

    age_units_keywords = ("days","months","years")
    age_units = { "days" : 0,
                  "months" : 1,
                  "years" : 2
    }

    def __init__(self):
        self.search_String = None
        self.category = "Any"
        self.safe_Search = True
        self.min_Seeds = 0
        self.min_Age = 0
        self.min_Age_Unit = size_units["days"]
        self.max_Size = 1000
        self.max_Size_unit = size_units["gb"]
        
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

    def __init__(self, orig = None):
        import datetime
        
        Query.__init__(self)
        
        self.status = statuses["active"]
        self.rate_Minute = 1.0
        self.action = actions["notify"]
        self.email_Notify = True
        self.date_Added = datetime.datetime.now()

    def copy_const(self,orig):
        pass

    def non_copy_const(self):
        pass
