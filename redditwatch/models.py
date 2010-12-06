from google.appengine.ext import db

class PingResultModel(db.Expando):
    timestamp   = db.DateTimeProperty(required=True)
    duration    = db.FloatProperty()
    status_code = db.IntegerProperty()
    content     = db.TextProperty()

    def get_headers(self):
        headers = {}
        for attr_name in dir(self):
            if attr_name.startswith('header-'):
                headers[attr_name[7:]] = getattr(self, attr_name)
        return headers


class AverageResultModel(db.Expando):
    start    = db.DateTimeProperty(required=True)
    interval = db.IntegerProperty(required=True)
    samples  = db.IntegerProperty(required=True)

    min_delay = db.FloatProperty()
    max_delay = db.FloatProperty()
    avg_delay = db.FloatProperty()

    def get_status_counts(self):
        status_counts = {}
        for attr_name in dir(self):
            if attr_name.startswith('status_'):
                status_counts[attr_name[7:]] = getattr(self, attr_name)
        return status_counts

