def getNumLesson(tadle, hour, min):
    if tadle[0]["stLessHour"] >= hour and tadle[0]["stLessMin"] > min:
        return 0
    elif hour >= tadle[0]["stLessHour"] and min >= tadle[0]["stLessMin"] and hour <= tadle[0]["endLessHour"]:
        if hour == tadle[0]["endLessHour"] and min <= tadle[0]["endLessMin"]:
            return 1
    return 8


tables = [
  {"stLessHour": 8, "stLessMin": 30, "endLessHour": 9, "endLessMin": 15},
  {"stLessHour": 9, "stLessMin": 30, "endLessHour": 10, "endLessMin": 15},
  {"stLessHour": 10, "stLessMin": 30, "endLessHour": 11, "endLessMin": 15},
  {"stLessHour": 11, "stLessMin": 30, "endLessHour": 12, "endLessMin": 15},
  {"stLessHour": 12, "stLessMin": 30, "endLessHour": 13, "endLessMin": 15},
  {"stLessHour": 13, "stLessMin": 30, "endLessHour": 14, "endLessMin": 15},
  {"stLessHour": 14, "stLessMin": 30, "endLessHour": 15, "endLessMin": 15}
]

print(getNumLesson(tables, 9, 10))