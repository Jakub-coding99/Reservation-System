from datetime import datetime
time_now = datetime.now()
formated_time = time_now.strftime("%d-%m-%Y, %H:%M:%S")

dt_obj = datetime.strptime(formated_time,"%d-%m-%Y, %H:%M:%S")
print(dt_obj)
print(type(dt_obj))


