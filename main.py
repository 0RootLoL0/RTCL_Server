import time
import json
import sqlite3
import secrets
import datetime
from flask import Flask, request, g
app = Flask(__name__)

def connect_db():
    rv = sqlite3.connect("test_db_sqlite.db")
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def isLesson(minStart, minEnd, inMin):
    if minStart <= inMin and minEnd >= inMin:
        return True
    else:
        return False

def getNumLesson(tables, min):
    Lesson = 0
    if min < tables[0]["StartMinL"]:
        return Lesson
    elif min > tables[len(tables)-1]["StartMinL"]:
        return len(tables)+1

    for table in tables:
        if isLesson(table["StartMinL"], table["EndMinL"] , min):
            break
        else:
            Lesson += 1

    return Lesson

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getTime')
def getTime():
    return str(int(time.time()))

@app.route('/getLesson')
def getLesson():
    token = request.args.get("token")
    if token == "":
        return "{\"status\": \"hui\"}"
    
    mess = ""
    db = get_db()
    cur = db.execute('SELECT * FROM "main"."users_rootlolhui" WHERE "token_clock"=\''+token+'\';')
    entries = cur.fetchall()
    if len(entries) == 1:
        now = datetime.datetime.now()
        Lesson = getNumLesson(json.loads(entries[0]["schedule_calls"]), now.hour*60+now.minute)
        print(Lesson)
        if Lesson == 0:
            mess = json.dumps({"Lesson": "не начились"})
        elif Lesson == 8:
            mess = json.dumps({"Lesson": "кончились"})
        else:
            mess = json.loads(entries[0]["lessons_monday"])[Lesson]["Lesson"]
    return mess

if __name__ == '__main__':
    app.run()