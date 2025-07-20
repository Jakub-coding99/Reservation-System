import datetime

time = (datetime.time(3, 7))
new_time = time.strftime("%H:%M")
print(new_time)
print(type(new_time))