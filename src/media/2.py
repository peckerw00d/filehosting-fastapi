next_day = "После 28 февраля будет "
year = 2017

next_day += "29 февраля." if year % 4 == 0 else "1 марта"
print(next_day)
