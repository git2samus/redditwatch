from google.appengine.ext import db

class PingResultModel(db.Expando):
    timestamp   = db.DateTimeProperty()
    duration    = db.FloatProperty()
    status_code = db.IntegerProperty()
    content     = db.TextProperty()

