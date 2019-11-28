import datetime
def isLesson(minStart, minEnd, inMin):
    if minStart <= inMin and minEnd >= inMin:
        return True
    else:
        return False

def getNumLesson(tables, min):
    Lesson = 0
    if min < tables[0]["StartMinL"]:
        return Lesson

    for table in tables:
        if isLesson(table["StartMinL"], table["EndMinL"] , min):
            Lesson += 1
            break
        else:
            Lesson += 1

    return Lesson
          
tables = [
    {"StartMinL": 510, "EndMinL": 555},
    {"StartMinL": 570, "EndMinL": 615},
    {"StartMinL": 510, "EndMinL": 555},
    {"StartMinL": 510, "EndMinL": 555},
    {"StartMinL": 510, "EndMinL": 555},
    {"StartMinL": 510, "EndMinL": 555},
    {"StartMinL": 510, "EndMinL": 555},
]
now = datetime.datetime.now()
print(getNumLesson(tables, now.hour*60+now.minute))