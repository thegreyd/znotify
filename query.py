class Query():
    def __init__(self,search_String,category="Any",seed_Lower_Limit=0,size_Lower_Limit=0,size_Lower_Limit_unit="m",size_Upper_Limit=None,size_Upper_Limit_unit=None,date_Lower_Limit=None,date_Lower_Limit_unit=None,safe_Search=True):
        self.search_String = search_String
        self.category = category
        self.safe_Search = safe_Search

        self.seed_Lower_Limit = seed_Lower_Limit

        self.date_Lower_Limit = date_Lower_Limit
        self.date_Lower_Limit_unit = date_Lower_Limit_unit

        self.size_Upper_Limit = size_Upper_Limit
        self.size_Upper_Limit_unit = size_Upper_Limit_unit
        self.size_Lower_Limit = size_Lower_Limit
        self.size_Lower_Limit_unit = size_Lower_Limit_unit
        
class Filter(Query):
    def __init__():
        pass      