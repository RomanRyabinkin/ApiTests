import datetime
import calendar
dt = datetime.datetime.now()
def dt2ts(data):
    return calendar.timegm(data.utctimetuple())
func_result = dt2ts(data=dt)
utc_mark = func_result - 100000



