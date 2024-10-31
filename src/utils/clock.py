from datetime import datetime


def delta_time(time_init: datetime):
    delta = datetime.now() - time_init
    return delta.total_seconds()
