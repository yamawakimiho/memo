from datetime import datetime

def convert_timestamp(time):
    return datetime.astimezone(time).strftime("%Y-%m-%d %H:%M:%S")
