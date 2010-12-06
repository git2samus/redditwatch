#!/usr/bin/env python
import os
from datetime import datetime, timedelta

from models import PingResultModel, AverageResultModel

def main():
    timestamp = datetime.utcnow()
    interval = int(os.environ['PATH_INFO'][12:])

    minute = timestamp.minute - timestamp.minute % interval
    end = timestamp.replace(minute=minute, second=0, microsecond=0)
    start = end - timedelta(minutes=interval)

    query = PingResultModel.gql('WHERE timestamp >= :start AND timestamp < :end', start=start, end=end)
    samples = query.count()

    average_result = AverageResultModel(
        start    = start,
        interval = interval,
        samples  = samples,
    )

    if samples:
        average_result.min_delay = min(ping.duration for ping in query)
        average_result.max_delay = max(ping.duration for ping in query)
        average_result.avg_delay = sum(ping.duration for ping in query) / samples

        for ping in query:
            if hasattr(ping, 'status_code'):
                status_count = getattr(average_result, 'status_%d' % ping.status_code, 0)
                setattr(average_result, 'status_%d' % ping.status_code, status_count + 1)

    average_result.put()


if __name__ == '__main__':
    main()

