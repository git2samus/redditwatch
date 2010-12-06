from google.appengine.ext import db

class PingResultModel(db.Expando):
    timestamp   = db.DateTimeProperty()
    duration    = db.FloatProperty()
    status_code = db.IntegerProperty()
    content     = db.TextProperty()


class AverageResultModel(db.Expando):
    start    = db.DateTimeProperty()
    interval = db.IntegerProperty()
    samples  = db.IntegerProperty()

    min_delay = db.FloatProperty()
    max_delay = db.FloatProperty()
    avg_delay = db.FloatProperty()

