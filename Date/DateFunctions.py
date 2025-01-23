import datetime
import time
from typing import Optional


class Date:
    def __init__(self, days: Optional[int] = None):
        if days is None:
            self.days = 1
        self.current_data = datetime.datetime.now()
        self.current_year = datetime.datetime.now().year
        self.current_month = datetime.datetime.now().month
        self.current_day = datetime.datetime.now().day
        self.current_unix_timestamp = int(time.time())

