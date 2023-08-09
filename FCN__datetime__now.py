import datetime

def now():
    # Get the current time as an array on 24 HR TIME [YYYY, MM, DD, HH, MM, SS, sss] where "sss" is milliseconds.
    # Now formatting the time to include leading zeroes where necessary
    now = datetime.datetime.now()
    formatted_time = ['{:04d}'.format(now.year), '{:02d}'.format(now.month), '{:02d}'.format(now.day), '{:02d}'.format(now.hour), '{:02d}'.format(now.minute), '{:02d}'.format(now.second), '{:03d}'.format(now.microsecond // 1000)]
    
    # Joining the list elements into a string
    return ''.join(formatted_time[:3]) + '-' + ''.join(formatted_time[3:6])

# print(now())