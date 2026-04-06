class Levels:
    def __init__(self, 
                 curpage: int, 
                 offset: int, 
                 limit: int, 
                 hasmore: bool,
                 total: int
                 ):
        self.page = curpage
        self.offset = offset
        self.limit = limit
        self.more = hasmore
        self.total = total