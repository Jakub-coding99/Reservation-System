import datetime

d = datetime.date(2025, 8, 23)
t = datetime.time(hour=10,minute=10)
print(t)
print(d)

combine = datetime.datetime.combine(d,t)
iso = combine.isoformat()

print(iso)


now = datetime.datetime.now()
new_iso = now.isoformat()
print(new_iso)
"Thu Aug 21 2025 20:22:00 GMT+0200 (středoevropský letní čas)"
# let datetime = "Thu Aug 21 2025 20:22:00 GMT+0200 (středoevropský letní čas)"
# let divided = datetime.split("T")
# let date = divided[0]
# let timeToFormate = divided[1]
# time = timeToFormate.slice("0",5)