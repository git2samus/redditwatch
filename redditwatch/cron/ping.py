#!/usr/bin/env python
import traceback, re
from datetime import datetime
from google.appengine.ext import db
from google.appengine.api import urlfetch

from models import PingResultModel

url = 'http://reddit.com/' # url to ping
deadline = 10              # timeout in secs (max 10)
# http://code.google.com/p/googleappengine/issues/detail?id=739
headers = {
    'Cache-Control': 'max-age=0',
}

charset_re = re.compile('charset=(.*)')

def main():
    timestamp = datetime.utcnow()

    try:
        result = urlfetch.fetch(url, headers=headers, deadline=deadline)
    except urlfetch.Error:
        ping_result = PingResultModel(
            timestamp   = timestamp,
            duration    = float(deadline),
            status_code = -1,
            content     = db.Text(traceback.format_exc()),
        )
    else:
        delta = datetime.utcnow() - timestamp

        encoding = 'UTF-8'
        if 'content-type' in result.headers:
            match = charset_re.search(result.headers['content-type'])
            if match:
                encoding = match.group(1)

        ping_result = PingResultModel(
            timestamp   = timestamp,
            duration    = delta.seconds + delta.microseconds / (1000.0 ** 2),
            status_code = result.status_code,
            content     = db.Text(result.content, encoding),
        )

        for header, value in result.headers.items():
            setattr(ping_result, 'header-%s' % header, value)

    ping_result.put()


if __name__ == '__main__':
    main()

