import datetime
import json

def isLesson(minStart, minEnd, inMin):
    if minStart <= inMin and minEnd >= inMin:
        return True
    else:
        return False

def getNumLesson(tables, min):
    Lesson = 0
    if not min < tables[0]["StartMinL"]:
        for table in tables:
            if isLesson(table["StartMinL"], table["EndMinL"] , min):
                break
            else:
                Lesson += 1

    return {"count": len(tables), "num": Lesson}
          
tables = [
    {"StartMinL": 510, "EndMinL": 555},
    {"StartMinL": 570, "EndMinL": 615},
    {"StartMinL": 630, "EndMinL": 655},
    {"StartMinL": 670, "EndMinL": 715},
    {"StartMinL": 730, "EndMinL": 755},
    {"StartMinL": 770, "EndMinL": 815},
    {"StartMinL": 830, "EndMinL": 855},
]


now = datetime.datetime.now()

Lesson1 = getNumLesson(tables, now.hour*60+now.minute)

print(Lesson1)

if Lesson1["num"] == 0:
    mess = json.dumps({"Lesson": "not started"})
elif Lesson1["num"] == Lesson1["count"]:
    mess = json.dumps({"Lesson": "endel"})
else:
    mess = "hui"

print(mess)