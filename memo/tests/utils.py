import datetime


def convertTimeStamp(time):
    return datetime.datetime.astimezone(time).strftime("%Y-%m-%d %H:%M:%S")
