from datetime import datetime, timedelta

now = datetime.now()

td = timedelta(hours=24)

yesterday = now - td

val = datetime(now.year, now.month, 25, now.hour, minute=10)
if val >= yesterday:
    rep = True
else:
    rep = False

print(f'Bool: {rep}')

print(now)
print(val.second)

